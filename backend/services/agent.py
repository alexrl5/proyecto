"""Orquestación del agente Profesor Digital."""

from __future__ import annotations

import inspect
import json
from typing import Any, Dict, List, Optional

from agents import Agent, Runner, function_tool

from ..schemas import ChatMessage, ChatResponse
from . import store


@function_tool
def launch_game(spec_json: str) -> str:
    """Eco para que el modelo pueda devolver GameSpec como JSON."""
    try:
        spec = json.loads(spec_json)
    except Exception:
        spec = {"error": "spec_json no es JSON valido"}
    return json.dumps(spec, ensure_ascii=False)


SYSTEM_PROMPT = (
    "Actuas como profesor de Electronica Digital. "
    "Responde siempre en espanol, claro y conciso. "
    "Si el estudiante pide practicar (quiz/tabla de verdad), construye un GameSpec y "
    "LLAMA a launch_game pasando el objeto como string JSON en spec_json.\n\n"
    "GameSpec { type: 'quiz'|'truth_table', title, topic, difficulty, professor_note, "
    "payload }.\n"
    "Quiz payload: {questions:[{id,prompt,choices[],correctIndex,explanation}]}\n"
    "Truth table payload: {headers, rows:[{A,B}], solution:[{A,B,F}]}\n"
    "Si solo piden teoria, responde sin herramientas."
)

prof_agent = Agent(
    name="Profesor Digital",
    instructions=SYSTEM_PROMPT,
    tools=[launch_game],
)

# --- Capabilidades del SDK ---
HAS_CREATE_THREAD = hasattr(Runner, "create_thread")
HAS_ADD_MESSAGE = hasattr(Runner, "add_message")
HAS_DELETE_THREAD = hasattr(Runner, "delete_thread")

try:
    RUN_SIG = inspect.signature(Runner.run)
    RUN_PARAMS = tuple(RUN_SIG.parameters.keys())
except Exception:
    RUN_PARAMS = tuple()

ACCEPTS_THREAD_ID = "thread_id" in RUN_PARAMS
ACCEPTS_MESSAGES = "messages" in RUN_PARAMS
INPUT_PARAM = next((p for p in ("input", "text", "prompt") if p in RUN_PARAMS), None)
ACCEPTS_INPUT = INPUT_PARAM is not None

THREAD_MODE = HAS_CREATE_THREAD and HAS_ADD_MESSAGE and ACCEPTS_THREAD_ID

if not (THREAD_MODE or ACCEPTS_MESSAGES or ACCEPTS_INPUT):
    raise RuntimeError(
        "Tu build de 'agents' no soporta threads, messages ni input manual. "
        "Actualiza el SDK para continuar."
    )


def get_agent_mode() -> str:
    if THREAD_MODE:
        return "threads"
    if ACCEPTS_MESSAGES:
        return "messages"
    if ACCEPTS_INPUT:
        return f"input:{INPUT_PARAM}"
    return "unknown"


def _ensure_history(trace_id: str) -> List[Dict[str, str]]:
    history = list(store.get_history(trace_id))
    if not history or history[0].get("role") != "system":
        history.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
    return history


def _looks_like_gamespec(obj: Any) -> bool:
    return (
        isinstance(obj, dict)
        and obj.get("type") in ("quiz", "truth_table")
        and "payload" in obj
        and "title" in obj
    )


def _extract_gamespec(result: Any) -> Optional[dict]:
    for attr in ("new_items", "tool_outputs", "items", "steps"):
        seq = getattr(result, attr, None)
        if not seq and isinstance(result, dict):
            seq = result.get(attr)
        if not seq:
            continue
        for item in seq:
            out = None
            if isinstance(item, dict):
                out = item.get("output") or item.get("content") or item.get("arguments")
            else:
                out = getattr(item, "output", None) or getattr(item, "content", None) or getattr(item, "arguments", None)
            if not out:
                continue
            try:
                data = json.loads(out) if isinstance(out, str) else out
                if _looks_like_gamespec(data):
                    return data
            except Exception:
                continue
    if isinstance(result, dict) and _looks_like_gamespec(result):
        return result
    return None


def _extract_text(result: Any) -> str:
    for attr in ("final_output", "content", "text", "output", "message"):
        value = getattr(result, attr, None)
        if isinstance(value, str) and value.strip():
            return value.strip()
    if isinstance(result, dict):
        for key in ("final_output", "content", "text", "output", "message"):
            value = result.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return "(Sin respuesta)"


async def process_chat(trace_id: str, messages: List[ChatMessage]) -> ChatResponse:
    user_text = ""
    for msg in reversed(messages):
        if msg.role == "user":
            user_text = (msg.content or "").strip()
            break
    user_text = user_text or "(entrada vacia)"
    history: Optional[List[Dict[str, str]]] = None

    if THREAD_MODE:
        thread_id = store.get_thread(trace_id)
        if not thread_id:
            thread = Runner.create_thread(
                name=f"trace-{trace_id}",
                metadata={"trace": trace_id, "app": "profesor-digital"},
            )
            thread_id = getattr(thread, "id", thread)
            store.set_thread(trace_id, thread_id)
            try:
                await Runner.add_message(thread_id=thread_id, role="system", content=SYSTEM_PROMPT)
            except Exception:
                pass
        await Runner.add_message(thread_id=thread_id, role="user", content=user_text)
        result = await Runner.run(prof_agent, thread_id=thread_id)
    elif ACCEPTS_MESSAGES:
        history = _ensure_history(trace_id)
        history.append({"role": "user", "content": user_text})
        store.set_history(trace_id, history)
        result = await Runner.run(prof_agent, messages=history)
    else:
        history = _ensure_history(trace_id)
        history.append({"role": "user", "content": user_text})
        store.set_history(trace_id, history)
        transcript = "\n".join(f"{entry['role'].upper()}: {entry['content']}" for entry in history)
        result = await Runner.run(prof_agent, **{INPUT_PARAM: transcript})

    spec = _extract_gamespec(result)
    if spec:
        response = ChatResponse(kind="game_spec", spec=spec, trace=trace_id)
    else:
        text = _extract_text(result)
        response = ChatResponse(kind="assistant", content=text, trace=trace_id)

    if not THREAD_MODE and history is not None:
        assistant_msg = (
            f"GameSpec generado: {json.dumps(spec, ensure_ascii=False)}"
            if spec
            else (response.content or "(sin texto)")
        )
        history.append({"role": "assistant", "content": assistant_msg})
        store.set_history(trace_id, history)

    return response


def reset_trace(trace_id: str) -> None:
    thread_id = store.get_thread(trace_id)
    store.clear_thread(trace_id)
    store.clear_history(trace_id)
    if THREAD_MODE and HAS_DELETE_THREAD and thread_id:
        try:
            Runner.delete_thread(thread_id=thread_id)
        except Exception:
            pass

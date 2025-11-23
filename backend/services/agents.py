"""Servicios relacionados con el agente y la conversación."""

from __future__ import annotations

import inspect
import json
from typing import Any, Dict, List, Optional

from agents import Agent, Runner, function_tool

from core import store
from schemas import ChatMessage, ChatResponse

# ---------- Tool y agente ----------


@function_tool
def launch_game(spec_json: str) -> str:
    """Eco del GameSpec devuelto por el modelo."""
    try:
        spec = json.loads(spec_json)
    except Exception:
        spec = {"error": "spec_json no es JSON valido"}
    return json.dumps(spec, ensure_ascii=False)


PROF_SYSTEM_MESSAGE = (
    "Responde SIEMPRE en espanol, claro y breve. "
    "Si el usuario pide practicar (quiz o tabla de verdad), construye un GameSpec y "
    "LLAMA a 'launch_game' pasando el objeto como string JSON en 'spec_json'.\n\n"
    "GameSpec:\n"
    "- type: 'quiz'|'truth_table'\n"
    "- title, topic, difficulty('easy'|'medium'|'hard'), professor_note\n"
    "- payload: quiz -> {questions:[{id,prompt,choices[],correctIndex,explanation}]}\n"
    "          truth_table -> {headers,rows:[{A,B}],solution:[{A,B,F}]}\n"
    "Si solo piden teoria, responde sin herramientas."
)

prof_agent = Agent(
    name="Profesor de Electronica Digital",
    instructions=PROF_SYSTEM_MESSAGE,
    tools=[launch_game],
)

# ---------- Capacidades del SDK ----------

HAS_CREATE_THREAD = hasattr(Runner, "create_thread")
HAS_ADD_MESSAGE = hasattr(Runner, "add_message")
HAS_DELETE_THREAD = hasattr(Runner, "delete_thread")

try:
    RUN_SIG = inspect.signature(Runner.run)
    ACCEPTS_THREAD_ID = "thread_id" in RUN_SIG.parameters
    ACCEPTS_MESSAGES = "messages" in RUN_SIG.parameters
except Exception:
    ACCEPTS_THREAD_ID = False
    ACCEPTS_MESSAGES = False

THREADS_AVAILABLE = HAS_CREATE_THREAD and HAS_ADD_MESSAGE and ACCEPTS_THREAD_ID

if not (THREADS_AVAILABLE or ACCEPTS_MESSAGES):
    raise RuntimeError(
        "Tu build de 'agents' no soporta Threads ni parametro 'messages'. "
        "Actualiza el SDK para usar memoria nativa o permitir mensajes completos."
    )


def get_mode() -> str:
    """Modo operativo que se expone en /health."""
    return "threads" if THREADS_AVAILABLE else "messages"


def last_user_text(messages: List[ChatMessage]) -> str:
    for message in reversed(messages):
        if message.role == "user":
            return (message.content or "").strip()
    return "(entrada vacia)"


def looks_like_gamespec(obj: Any) -> bool:
    return (
        isinstance(obj, dict)
        and obj.get("type") in ("quiz", "truth_table")
        and "payload" in obj
        and "title" in obj
    )


def extract_gamespec(result: Any) -> Optional[dict]:
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
                if looks_like_gamespec(data):
                    return data
            except Exception:
                continue
    if isinstance(result, dict) and looks_like_gamespec(result):
        return result
    return None


def extract_text(result: Any) -> str:
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


def init_history(trace_id: str) -> List[Dict[str, str]]:
    history = list(store.get_history(trace_id))
    if not history or history[0].get("role") != "system":
        history.insert(0, {"role": "system", "content": PROF_SYSTEM_MESSAGE})
    return history


async def process_chat(trace_id: str, messages: List[ChatMessage]) -> ChatResponse:
    """Core de la llamada /api/chat."""
    user_text = last_user_text(messages) or "(entrada vacia)"
    history: Optional[List[Dict[str, str]]] = None

    if THREADS_AVAILABLE:
        thread_id = store.get_thread_id(trace_id)
        if not thread_id:
            thread = Runner.create_thread(
                name=f"conv-{trace_id}",
                metadata={"trace": trace_id, "app": "profedigi"},
            )
            thread_id = getattr(thread, "id", thread)
            store.set_thread_id(trace_id, thread_id)
            try:
                await Runner.add_message(thread_id=thread_id, role="system", content=PROF_SYSTEM_MESSAGE)
            except Exception:
                pass

        await Runner.add_message(thread_id=thread_id, role="user", content=user_text)
        result = await Runner.run(prof_agent, thread_id=thread_id)
    else:
        history = init_history(trace_id)
        history.append({"role": "user", "content": user_text})
        store.set_history(trace_id, history)
        result = await Runner.run(prof_agent, messages=history)

    spec = extract_gamespec(result)
    if spec is not None:
        response = ChatResponse(kind="game_spec", spec=spec, trace=trace_id)
    else:
        text = extract_text(result)
        response = ChatResponse(kind="assistant", content=text, trace=trace_id)

    if not THREADS_AVAILABLE and history is not None:
        assistant_message = (
            f"Se ha generado el siguiente GameSpec: {json.dumps(spec, ensure_ascii=False)}"
            if spec is not None
            else (response.content or "(sin texto)")
        )
        history.append({"role": "assistant", "content": assistant_message})
        store.set_history(trace_id, history)

    return response


def safe_delete_thread(thread_id: Optional[str]) -> None:
    if not (THREADS_AVAILABLE and HAS_DELETE_THREAD and thread_id):
        return
    try:
        Runner.delete_thread(thread_id=thread_id)
    except Exception:
        pass

"\"\"\"Persistencia para threads e historiales de chat.\"\"\""

from __future__ import annotations

import json
import os
import threading
from typing import Dict, List, Optional

from .settings import STORE_PATH

_lock = threading.Lock()


def _load_store() -> Dict[str, Dict[str, List[Dict[str, str]]]]:
    if not os.path.exists(STORE_PATH):
        return {"trace_to_thread": {}, "trace_histories": {}}
    try:
        with open(STORE_PATH, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            raise ValueError
    except Exception:
        data = {}
    data.setdefault("trace_to_thread", {})
    data.setdefault("trace_histories", {})
    return data


def _save_store(data: Dict[str, Dict[str, List[Dict[str, str]]]]) -> None:
    with _lock:
        tmp = STORE_PATH + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        os.replace(tmp, STORE_PATH)


def get_thread_id(trace_id: str) -> Optional[str]:
    return _load_store().get("trace_to_thread", {}).get(trace_id)


def set_thread_id(trace_id: str, thread_id: str) -> None:
    data = _load_store()
    data["trace_to_thread"][trace_id] = thread_id
    _save_store(data)


def clear_thread_id(trace_id: str) -> None:
    data = _load_store()
    data["trace_to_thread"].pop(trace_id, None)
    _save_store(data)


def get_history(trace_id: str) -> List[Dict[str, str]]:
    history = _load_store().get("trace_histories", {}).get(trace_id, [])
    return history if isinstance(history, list) else []


def set_history(trace_id: str, history: List[Dict[str, str]]) -> None:
    data = _load_store()
    data["trace_histories"][trace_id] = history
    _save_store(data)


def clear_history(trace_id: str) -> None:
    data = _load_store()
    data["trace_histories"].pop(trace_id, None)
    _save_store(data)

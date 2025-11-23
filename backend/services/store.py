"""Persistencia ligera en disco para threads e historiales."""

from __future__ import annotations

import json
import os
import threading
from typing import Dict, List, Optional

from ..app.config import get_settings

_lock = threading.Lock()


def _path() -> str:
    return get_settings()["STORE_PATH"]


def _load() -> Dict[str, Dict[str, List[Dict[str, str]]]]:
    path = _path()
    if not os.path.exists(path):
        return {"threads": {}, "histories": {}}
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            raise ValueError
    except Exception:
        data = {}
    data.setdefault("threads", {})
    data.setdefault("histories", {})
    return data


def _save(data: Dict[str, Dict[str, List[Dict[str, str]]]]) -> None:
    path = _path()
    tmp = f"{path}.tmp"
    with _lock:
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        os.replace(tmp, path)


def get_thread(trace_id: str) -> Optional[str]:
    return _load().get("threads", {}).get(trace_id)


def set_thread(trace_id: str, thread_id: str) -> None:
    data = _load()
    data["threads"][trace_id] = thread_id
    _save(data)


def clear_thread(trace_id: str) -> None:
    data = _load()
    data["threads"].pop(trace_id, None)
    _save(data)


def get_history(trace_id: str) -> List[Dict[str, str]]:
    history = _load().get("histories", {}).get(trace_id, [])
    return history if isinstance(history, list) else []


def set_history(trace_id: str, history: List[Dict[str, str]]) -> None:
    data = _load()
    data["histories"][trace_id] = history
    _save(data)


def clear_history(trace_id: str) -> None:
    data = _load()
    data["histories"].pop(trace_id, None)
    _save(data)

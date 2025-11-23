"""Endpoints de salud y utilidades del sistema."""

from typing import Optional

from fastapi import APIRouter

from core import store
from core.settings import STORE_PATH
from services.agents import get_mode, safe_delete_thread

router = APIRouter(tags=["system"])


@router.get("/health")
def health():
    return {
        "ok": True,
        "mode": get_mode(),
        "store_path": STORE_PATH,
    }


@router.post("/reset")
def reset(trace: Optional[str] = None):
    if not trace:
        return {"ok": True, "trace": None}

    thread_id = store.get_thread_id(trace)
    store.clear_thread_id(trace)
    store.clear_history(trace)
    safe_delete_thread(thread_id)

    return {"ok": True, "trace": trace}

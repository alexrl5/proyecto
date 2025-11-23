"""Endpoints de sistema (salud + reset)."""

from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from ...app.config import get_settings
from ...services.agent import get_agent_mode, reset_trace

router = APIRouter(tags=["system"])


class ResetPayload(BaseModel):
    trace: Optional[str] = None


@router.get("/health")
def health():
    settings = get_settings()
    return {
        "ok": True,
        "mode": get_agent_mode(),
        "store_path": settings["STORE_PATH"],
    }


@router.post("/reset")
def reset(payload: Optional[ResetPayload] = None, trace: Optional[str] = None):
    target = trace or (payload.trace if payload else None)
    if target:
        reset_trace(target)
    return {"ok": True, "trace": target}

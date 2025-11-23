"""Endpoint principal del chat."""

import uuid

from fastapi import APIRouter

from ...schemas import ChatRequest, ChatResponse
from ...services.agent import process_chat

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    trace_id = req.trace or str(uuid.uuid4())
    return await process_chat(trace_id, req.messages)

"""Pydantic schemas compartidas entre las llamadas de la API."""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class ChatRequest(BaseModel):
    trace: Optional[str] = None  # id de conversacion proporcionado por el front
    messages: List[ChatMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    kind: Literal["assistant", "game_spec"]
    content: Optional[str] = None
    spec: Optional[dict] = None
    trace: str

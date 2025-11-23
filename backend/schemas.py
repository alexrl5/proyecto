"""Esquemas Pydantic compartidos."""

from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class ChatRequest(BaseModel):
    trace: Optional[str] = None
    messages: List[ChatMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    kind: Literal["assistant", "game_spec"]
    content: Optional[str] = None
    spec: Optional[dict] = None
    trace: str

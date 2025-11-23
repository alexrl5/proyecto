"""Punto de entrada FastAPI."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_app_kwargs
from ..api.routes import chat, system

app = FastAPI(**get_app_kwargs())
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(system.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

"""Punto de entrada FastAPI estructurado por llamadas."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.settings import get_app_kwargs
from routes import chat, system

app = FastAPI(**get_app_kwargs())
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(system.router)
app.include_router(chat.router)

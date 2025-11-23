"""Configuración central de la API."""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Any, Dict

from dotenv import load_dotenv

load_dotenv()


def _require_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        raise RuntimeError(f"Falta la variable de entorno {var_name!r}")
    return value


@lru_cache(maxsize=1)
def get_app_kwargs() -> Dict[str, Any]:
    """Parámetros para FastAPI (se cachean para tests y hot reload)."""
    return {
        "title": "Profesor Digital - API",
        "description": "Backend para chat + juegos con soporte Threads/Messages/Input.",
        "version": "3.0.0",
        "docs_url": "/swagger",
        "redoc_url": "/docs",
    }


@lru_cache(maxsize=1)
def get_settings() -> Dict[str, Any]:
    """Valores básicos que usa el resto del backend."""
    openai_api_key = _require_env("OPENAI_API_KEY")
    store_path = os.getenv("STORE_PATH", "store.json")
    return {"OPENAI_API_KEY": openai_api_key, "STORE_PATH": store_path}

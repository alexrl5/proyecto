"""Configuracion comun para el backend."""

import os
from functools import lru_cache
from typing import Dict, Any

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Falta OPENAI_API_KEY en .env")

STORE_PATH = os.environ.get("STORE_PATH", "store.json")


@lru_cache(maxsize=1)
def get_app_kwargs() -> Dict[str, Any]:
    """Parametros para instanciar FastAPI de forma consistente."""
    return {
        "title": "Profesor Electronica Digital - OpenAI Threads",
        "description": (
            "API del profesor digital con soporte para juegos, traces y modo fallback sin threads. "
            "Explora y prueba los endpoints con Swagger en /swagger."
        ),
        "version": "2.0.0",
        "docs_url": "/swagger",
        "redoc_url": "/docs",
    }

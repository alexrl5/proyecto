"""Carga y consulta de documentos locales para el agente."""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from typing import Dict, List

BASE_DIR = Path(__file__).resolve().parents[1]
DOCS_DIR = BASE_DIR / "documentos"
ALLOWED_EXTENSIONS = {".md", ".mdx", ".txt"}


def _iter_source_files() -> List[Path]:
    paths: List[Path] = []
    if DOCS_DIR.exists():
        for path in DOCS_DIR.rglob("*"):
            if path.is_file() and path.suffix.lower() in ALLOWED_EXTENSIONS:
                paths.append(path)
    for path in BASE_DIR.glob("*.md"):
        if path.is_file() and path.suffix.lower() in ALLOWED_EXTENSIONS:
            paths.append(path)
    unique: Dict[str, Path] = {}
    for path in paths:
        unique[str(path.resolve())] = path
    return list(unique.values())


@lru_cache(maxsize=1)
def load_documents() -> List[Dict[str, str]]:
    documents: List[Dict[str, str]] = []
    for path in _iter_source_files():
        try:
            content = path.read_text(encoding="utf-8")
        except Exception:
            continue
        documents.append(
            {
                "id": str(path.relative_to(BASE_DIR)),
                "name": path.name,
                "content": content,
            }
        )
    return documents


def refresh_documents() -> None:
    load_documents.cache_clear()
    load_documents()


def _tokenize(text: str) -> List[str]:
    return [token for token in re.findall(r"\w+", text.lower()) if len(token) > 2]


def _make_snippet(content: str, center: int, window: int) -> str:
    half = window // 2
    start = max(center - half, 0)
    end = min(center + half, len(content))
    snippet = content[start:end].strip()
    return snippet


def search_documents(query: str, max_results: int = 3, window: int = 600) -> List[Dict[str, str]]:
    query = (query or "").strip()
    docs = load_documents()
    if not docs:
        return []
    if not query:
        return [
            {
                "source": doc["id"],
                "title": doc["name"],
                "snippet": doc["content"][:window].strip(),
                "score": 0,
            }
            for doc in docs[:max_results]
        ]

    tokens = _tokenize(query) or [query.lower()]
    scored: List[Dict[str, str]] = []
    for doc in docs:
        text = doc["content"]
        lowered = text.lower()
        score = sum(lowered.count(token) for token in tokens)
        if query.lower() in lowered:
            score += 2
        if score == 0:
            continue
        default_pos = lowered.find(query.lower())
        first_hit = min(
            (pos for pos in (lowered.find(token) for token in tokens) if pos != -1),
            default=default_pos if default_pos != -1 else None,
        )
        center = first_hit if first_hit is not None else len(text) // 2
        scored.append(
            {
                "source": doc["id"],
                "title": doc["name"],
                "snippet": _make_snippet(text, center, window),
                "score": score,
            }
        )

    if not scored:
        return [
            {
                "source": doc["id"],
                "title": doc["name"],
                "snippet": doc["content"][:window].strip(),
                "score": 0,
            }
            for doc in docs[:max_results]
        ]

    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored[:max_results]

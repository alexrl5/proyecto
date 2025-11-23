# Profesor Digital · Rebuild 2025

Aplicación rehecha desde cero para separar claramente backend y frontend. El backend usa FastAPI y un servicio de agentes compatible con tres modos (Threads nativos, `messages` o `input`). El frontend es una SPA estática sin dependencias que consume la API y muestra quizzes/tablas en vivo.

## Backend

```
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

1. Crea/actualiza `.env` en la raíz del repo con `OPENAI_API_KEY=...` (y opcional `STORE_PATH`).
2. Lanza el servidor: `uvicorn backend.app.main:app --reload --port 8000`
3. Documentación interactiva en `http://localhost:8000/swagger` (usa los assets por defecto de FastAPI) y ReDoc en `/docs`.

Arquitectura:

- `backend/app`: configuración y punto de entrada de FastAPI.
- `backend/api/routes`: routers de sistema (`/api/health`, `/api/reset`) y chat (`/api/chat`).
- `backend/services/agent.py`: lógica central del profesor, detección de features del SDK `agents`, tooling `launch_game`.
- `backend/services/store.py`: persistencia en `store.json` para mapear `trace -> thread_id` e historiales.
- `backend/schemas.py`: modelos Pydantic para requests/responses.

## Frontend

El front es un HTML+JS autónomo (`frontend/index.html`). Puedes abrirlo con Live Server o servirlo rápido:

```
npx serve frontend
# o
python -m http.server 4173 -d frontend
```

Por defecto llama a `http://localhost:8000/api`; puedes apuntarlo a otra URL usando `?api=https://tu-backend.com/api`. Incluye chips de prompts rápidos, visor del modo del backend y render dinámico de GameSpec.

## Notas

- `store.json` queda en la raíz (configurable con `STORE_PATH`). Contiene `threads` y `histories`.
- El backend cambia automáticamente de modo según las capacidades del SDK `agents`: Threads > Messages > Input.
- Botones “Nuevo trace” y “Reset hilo” desde el frontend limpian `localStorage` y notifican al backend.

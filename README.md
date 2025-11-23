# Profesor Electronica Digital

Separacion ligera en front/back. El backend expone FastAPI y el frontend es un HTML+JS estatico.

## Backend
1. `cd backend`
2. (Opcional) `python -m venv .venv && .venv\\Scripts\\activate`
3. `pip install -r requirements.txt`
4. Define `OPENAI_API_KEY` en `.env` (copiar desde la raiz o crear uno nuevo).
5. `uvicorn app:app --reload --port 3000` (los routers estan divididos por llamadas en `routes/`)

El front consume `http://localhost:3000/api/chat` por defecto. Cambia el puerto o la URL lanzando el HTML con `?api=http://host:puerto/api/chat`.

## Frontend
- Abre `frontend/index.html` con Live Server/VSCode o sirve la carpeta: `npx serve frontend` o `python -m http.server 4173 -d frontend`.
- Una vez cargado, escribe mensajes o usa los chips predefinidos. El `trace` se guarda en `localStorage` (botones "Nuevo chat" y "Reset hilo" lo limpian).

## Notas
- `store.json` se mantiene en la raiz del repo y guarda el mapeo `trace -> thread_id`.
- Si cambias la ubicacion del backend, ajusta `STORE_PATH` via variable de entorno para evitar colisiones.
- Si tu SDK `agents` no soporta Threads nativos, el backend cae en modo fallback usando el parametro `messages`; en ese caso `store.json` guarda el historial completo de la conversacion.
- FastAPI expone Swagger UI en `http://localhost:3000/swagger` (Redoc queda en `/docs`) para que pruebes los endpoints sin levantar el frontend.
- La logica esta estructurada por llamadas: `routes/system.py` maneja `/health` y `/reset`, `routes/chat.py` maneja `/api/chat`, y la capa de servicio vive en `services/agents.py`.

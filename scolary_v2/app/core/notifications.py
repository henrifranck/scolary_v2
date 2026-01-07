import asyncio
from typing import Any, List
from time import time
from contextlib import contextmanager

from fastapi import WebSocket, WebSocketDisconnect

from app.core.mongo import get_notifications_collection
from app.db.session import SessionLocal
from app.crud.crud_notification_template import notification_template


@contextmanager
def _db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class NotificationManager:
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: Any) -> None:
        disconnected: List[WebSocket] = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)
        for ws in disconnected:
            self.disconnect(ws)


manager = NotificationManager()


def _render_from_template(template_key: str | None, variables: dict | None):
    if not template_key:
        return None, None
    with _db_session() as db:
        try:
            tpl = notification_template.get_by_key(db, key=template_key)
            if not tpl or not tpl.template:
                return None, None
            vars_dict = variables or {}
            try:
                rendered_body = tpl.template.format(**vars_dict)
            except Exception:
                # Avoid breaking on missing keys; return raw template
                rendered_body = tpl.template
            try:
                rendered_title = tpl.title.format(**vars_dict) if tpl.title else tpl.title
            except Exception:
                rendered_title = tpl.title
            return rendered_body, rendered_title
        except Exception:
            return None, None


def _prepare_notification_payload(message: Any) -> Any:
    if not isinstance(message, dict):
        return message
    payload = dict(message)
    template_key = payload.get("template_key") or payload.get("type")
    rendered_body, rendered_title = _render_from_template(
        template_key, payload.get("template_vars")
    )
    if rendered_body:
        # Store the rendered text under message for UI and keep raw template key
        payload.setdefault("message", rendered_body)
        payload["rendered_template"] = rendered_body
    if rendered_title:
        payload.setdefault("title", rendered_title)
        payload["rendered_title"] = rendered_title
    return payload


def schedule_notification(message: Any) -> None:
    """Persist (if Mongo configured) and broadcast without blocking sync endpoints."""
    prepared = _prepare_notification_payload(message)
    try:
        coll = get_notifications_collection()
        if coll is not None:
            doc = {
                **(prepared if isinstance(prepared, dict) else {"message": str(prepared)}),
                "read": False,
                "created_at": time(),
            }
            result = coll.insert_one(doc)
            doc["_id"] = str(getattr(result, "inserted_id", "")) if result else None
            prepared = doc
    except Exception:
        pass

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(manager.broadcast(prepared))
    except RuntimeError:
        # Fallback: create a new loop if none running (rare in FastAPI context)
        asyncio.run(manager.broadcast(prepared))

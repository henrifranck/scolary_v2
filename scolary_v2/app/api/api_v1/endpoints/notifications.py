from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from jose import jwt, JWTError
from pydantic import ValidationError
from bson import ObjectId

from app.core.config import settings
from app.api import deps
from app import schemas, models
from app.core.notifications import manager
from app.core.mongo import get_notifications_collection

router = APIRouter()


def _get_roles_from_user(user: models.User) -> list[str]:
    roles = []
    try:
        for ur in getattr(user, "user_role", []) or []:
            if ur.role and ur.role.name:
                roles.append(ur.role.name)
    except Exception:
        pass
    return roles or ["user"]


@router.get("/notifications")
def list_notifications(
    limit: int = 50,
    current_user: models.User = Depends(deps.get_current_user)
):
    coll = get_notifications_collection()
    if coll is None:
        raise HTTPException(status_code=503, detail="Notifications storage not configured.")
    roles = _get_roles_from_user(current_user)
    print(roles)
    query = {
        "$or": [
            {"target_roles": {"$exists": False}},
            {"target_roles": {"$size": 0}},
            {"target_roles": {"$in": roles}}
        ]
    }
    docs = coll.find(query).sort("created_at", -1).limit(limit)
    results = []
    for doc in docs:
        doc["_id"] = str(doc.get("_id"))
        results.append(doc)
    return {"data": results}


@router.post("/notifications/{notification_id}/read")
def mark_notification_read(
    notification_id: str,
    current_user: models.User = Depends(deps.get_current_user)
):
    coll = get_notifications_collection()
    if coll is None:
        raise HTTPException(status_code=503, detail="Notifications storage not configured.")
    roles = _get_roles_from_user(current_user)
    try:
        _id = ObjectId(notification_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid notification id")
    result = coll.update_one(
        {
            "_id": _id,
            "$or": [
                {"target_roles": {"$exists": False}},
                {"target_roles": {"$size": 0}},
                {"target_roles": {"$in": roles}}
            ]
        },
        {"$set": {"read": True}}
    )
    if not result.matched_count:
        raise HTTPException(status_code=404, detail="Notification not found or not allowed")
    return {"status": "ok"}


@router.websocket("/notifications")
async def websocket_notifications(websocket: WebSocket):
    token = websocket.query_params.get("token") or websocket.headers.get("Authorization", "").replace("Bearer ", "")
    if token:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[deps.security.ALGORITHM])
            schemas.TokenPayload(**payload)
        except (JWTError, ValidationError):
            # If token is invalid, continue without user context (best effort)
            pass

    await manager.connect(websocket)
    try:
        while True:
            # We don't expect messages from clients yet; just keep connection alive.
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

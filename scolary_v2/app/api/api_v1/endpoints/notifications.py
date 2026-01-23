from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from jose import jwt, JWTError
from pydantic import ValidationError
from bson import ObjectId

from app.core.config import settings
from app.api import deps
from app import schemas, models
from app.core.notifications import manager
from app.core.mongo import get_notifications_collection
from app.db.session import SessionLocal

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
    value = _get_roles_from_user(current_user)
    roles = []
    for r in value:
        try:
            normalized = str(r).strip().lower()
        except Exception:
            normalized = ""
        if normalized:
            roles.append(normalized)
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
        read_by = doc.get("read_by", []) or []
        doc["read"] = current_user.id in read_by
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
        {"$addToSet": {"read_by": current_user.id}}
    )
    if not result.matched_count:
        raise HTTPException(status_code=404, detail="Notification not found or not allowed")
    return {"status": "ok"}


@router.websocket("/notifications")
async def websocket_notifications(websocket: WebSocket):
    token = websocket.query_params.get("token") or websocket.headers.get("Authorization", "").replace("Bearer ", "")
    roles: list[str] = []
    if token:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[deps.security.ALGORITHM])
            token_data = schemas.TokenPayload(**payload)
            with SessionLocal() as db:
                user = (
                    db.query(models.User)
                    .filter(models.User.id == token_data.id)
                    .join(models.UserRole, models.UserRole.id_user == models.User.id, isouter=True)
                    .join(models.Role, models.Role.id == models.UserRole.id_role, isouter=True)
                    .all()
                )
                if user:
                    roles = []
                    try:
                        for ur in getattr(user[0], "user_role", []) or []:
                            if ur.role and ur.role.name:
                                roles.append(ur.role.name)
                    except Exception:
                        pass
        except (JWTError, ValidationError):
            # If token is invalid, continue without user context (best effort)
            pass

    await manager.connect(websocket, roles)
    try:
        while True:
            # We don't expect messages from clients yet; just keep connection alive.
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

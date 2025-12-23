# begin #
# ---write your code here--- #
# end #

from typing import Generator

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def _build_permission_map(db: Session, user_id: int) -> dict:
    permissions = (
        db.query(models.Permission)
        .join(
            models.RolePermission,
            models.Permission.id == models.RolePermission.id_permission
        )
        .join(
            models.UserRole,
            models.RolePermission.id_role == models.UserRole.id_role
        )
        .filter(models.UserRole.id_user == user_id)
        .all()
    )
    available_models = crud.available_model.get_multi_where_array(
        db=db, skip=0, limit=1000
    )
    route_by_name = {
        (model.name or "").strip().lower(): (model.route_api or "").strip().lower()
        for model in available_models
        if (model.name or "").strip() and (model.route_api or "").strip()
    }

    permission_map = {}
    for permission in permissions:
        model_name = (permission.model_name or "unknown").strip().lower()
        route_api = route_by_name.get(model_name, model_name)
        route_api = route_api.lstrip("/")
        entry = permission_map.setdefault(
            route_api,
            {"get": False, "post": False, "put": False, "delete": False}
        )
        entry["get"] = entry["get"] or bool(permission.method_get)
        entry["post"] = entry["post"] or bool(permission.method_post)
        entry["put"] = entry["put"] or bool(permission.method_put)
        entry["delete"] = entry["delete"] or bool(permission.method_delete)
    return permission_map

def _resolve_model_from_path(db: Session, path: str) -> str:
    api_prefix = settings.API_V1_STR.rstrip("/")
    trimmed = path
    if api_prefix and trimmed.startswith(api_prefix):
        trimmed = trimmed[len(api_prefix):]
    trimmed = "/" + trimmed.lstrip("/")

    available_models = crud.available_model.get_multi_where_array(
        db=db, skip=0, limit=1000
    )
    sorted_models = sorted(
        available_models,
        key=lambda model: len((model.route_api or "").strip()),
        reverse=True
    )
    for model in sorted_models:
        route_api = (model.route_api or "").strip()
        if not route_api:
            continue
        route_api = "/" + route_api.lstrip("/")
        if trimmed == route_api or trimmed.startswith(f"{route_api}/"):
            return route_api.lstrip("/").lower()

    parts = [part for part in trimmed.split("/") if part]
    return parts[0].lower() if parts else ""

def _is_method_allowed(permission_map: dict, model_name: str, method: str) -> bool:
    method_key = {
        "GET": "get",
        "POST": "post",
        "PUT": "put",
        "DELETE": "delete"
    }.get(method)
    if not method_key:
        return False
    model_key = (model_name or "").strip().lower()
    model_permissions = permission_map.get(model_key)
    return bool(model_permissions and model_permissions.get(method_key))

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    where = [
        {
            "key":"id",
            "value":token_data.id,
            "operator":"==",
        }
    ]

    relation = ['user_mention.mention']

    user = crud.user.get_first_where_array(db, where=where, relations=relation)
    if not user:
        raise HTTPException(status_code=403, detail="User not found")
    user.permissions = _build_permission_map(db, user.id)
    return user


def get_user(token: str) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return token_data


def get_token_info(token: str = Depends(reusable_oauth2)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return token_data


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
    request: Request = None,
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    if getattr(current_user, "is_superuser", False):
        return current_user
    if request is None:
        raise HTTPException(status_code=403, detail="Permission denied")
    model_name = _resolve_model_from_path(db, request.url.path)
    if not model_name:
        raise HTTPException(status_code=403, detail="Permission denied")
    permission_map = getattr(current_user, "permissions", {}) or {}
    if not _is_method_allowed(permission_map, model_name, request.method):
        raise HTTPException(status_code=403, detail="Permission denied")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


# begin #
# ---write your code here--- #
# end #

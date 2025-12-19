from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponsePermission)
def read_permissions(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve permissions.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    permissions = crud.permission.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.permission.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponsePermission(**{'count': count, 'data': jsonable_encoder(permissions)})
    return response


@router.post('/', response_model=schemas.Permission)
def create_permission(
        *,
        db: Session = Depends(deps.get_db),
        permission_in: schemas.PermissionCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new permission.
    """
    permission = crud.permission.create(db=db, obj_in=permission_in)
    return permission


@router.put('/{permission_id}', response_model=schemas.Permission)
def update_permission(
        *,
        db: Session = Depends(deps.get_db),
        permission_id: int,
        permission_in: schemas.PermissionUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an permission.
    """
    permission = crud.permission.get(db=db, id=permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail='Permission not found')
    permission = crud.permission.update(db=db, db_obj=permission, obj_in=permission_in)
    return permission


@router.get('/{permission_id}', response_model=schemas.Permission)
def read_permission(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        permission_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get permission by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    permission = crud.permission.get(db=db, id=permission_id, relations=relations, where=wheres)
    if not permission:
        raise HTTPException(status_code=404, detail='Permission not found')
    return permission


@router.delete('/{permission_id}', response_model=schemas.Msg)
def delete_permission(
        *,
        db: Session = Depends(deps.get_db),
        permission_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an permission.
    """
    permission = crud.permission.get(db=db, id=permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail='Permission not found')
    permission = crud.permission.remove(db=db, id=permission_id)
    return schemas.Msg(msg='Permission deleted successfully')

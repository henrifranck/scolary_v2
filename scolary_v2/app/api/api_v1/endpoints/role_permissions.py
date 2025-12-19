from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseRolePermission)
def read_role_permissions(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve role_permissions.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    role_permissions = crud.role_permission.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.role_permission.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseRolePermission(**{'count': count, 'data': jsonable_encoder(role_permissions)})
    return response


@router.post('/', response_model=schemas.RolePermission)
def create_role_permission(
        *,
        db: Session = Depends(deps.get_db),
        role_permission_in: schemas.RolePermissionCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new role_permission.
    """
    role_permission = crud.role_permission.create(db=db, obj_in=role_permission_in)
    return role_permission


@router.put('/{role_permission_id}', response_model=schemas.RolePermission)
def update_role_permission(
        *,
        db: Session = Depends(deps.get_db),
        role_permission_id: int,
        role_permission_in: schemas.RolePermissionUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an role_permission.
    """
    role_permission = crud.role_permission.get(db=db, id=role_permission_id)
    if not role_permission:
        raise HTTPException(status_code=404, detail='RolePermission not found')
    role_permission = crud.role_permission.update(db=db, db_obj=role_permission, obj_in=role_permission_in)
    return role_permission


@router.get('/{role_permission_id}', response_model=schemas.RolePermission)
def read_role_permission(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        role_permission_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get role_permission by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    role_permission = crud.role_permission.get(db=db, id=role_permission_id, relations=relations, where=wheres)
    if not role_permission:
        raise HTTPException(status_code=404, detail='RolePermission not found')
    return role_permission


@router.delete('/{role_permission_id}', response_model=schemas.Msg)
def delete_role_permission(
        *,
        db: Session = Depends(deps.get_db),
        role_permission_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an role_permission.
    """
    role_permission = crud.role_permission.get(db=db, id=role_permission_id)
    if not role_permission:
        raise HTTPException(status_code=404, detail='RolePermission not found')
    role_permission = crud.role_permission.remove(db=db, id=role_permission_id)
    return schemas.Msg(msg='RolePermission deleted successfully')

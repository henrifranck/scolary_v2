from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseRole)
def read_roles(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve roles.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    roles = crud.role.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.role.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseRole(**{'count': count, 'data': jsonable_encoder(roles)})
    return response


@router.post('/', response_model=schemas.Role)
def create_role(
        *,
        db: Session = Depends(deps.get_db),
        role_in: schemas.RoleCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new role.
    """
    role = crud.role.create(db=db, obj_in=role_in)
    return role


@router.put('/{role_id}', response_model=schemas.Role)
def update_role(
        *,
        db: Session = Depends(deps.get_db),
        role_id: int,
        role_in: schemas.RoleUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an role.
    """
    role = crud.role.get(db=db, id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail='Role not found')
    role = crud.role.update(db=db, db_obj=role, obj_in=role_in)
    return role


@router.get('/{role_id}', response_model=schemas.Role)
def read_role(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        role_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get role by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    role = crud.role.get(db=db, id=role_id, relations=relations, where=wheres)
    if not role:
        raise HTTPException(status_code=404, detail='Role not found')
    return role


@router.delete('/{role_id}', response_model=schemas.Msg)
def delete_role(
        *,
        db: Session = Depends(deps.get_db),
        role_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an role.
    """
    role = crud.role.get(db=db, id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail='Role not found')
    role = crud.role.remove(db=db, id=role_id)
    return schemas.Msg(msg='Role deleted successfully')

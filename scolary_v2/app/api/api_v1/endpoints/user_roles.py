from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseUserRole)
def read_user_roles(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve user_roles.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    user_roles = crud.user_role.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.user_role.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseUserRole(**{'count': count, 'data': jsonable_encoder(user_roles)})
    return response


@router.post('/', response_model=schemas.UserRole)
def create_user_role(
        *,
        db: Session = Depends(deps.get_db),
        user_role_in: schemas.UserRoleCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new user_role.
    """
    user_role = crud.user_role.create(db=db, obj_in=user_role_in)
    return user_role


@router.put('/{user_role_id}', response_model=schemas.UserRole)
def update_user_role(
        *,
        db: Session = Depends(deps.get_db),
        user_role_id: int,
        user_role_in: schemas.UserRoleUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an user_role.
    """
    user_role = crud.user_role.get(db=db, id=user_role_id)
    if not user_role:
        raise HTTPException(status_code=404, detail='UserRole not found')
    user_role = crud.user_role.update(db=db, db_obj=user_role, obj_in=user_role_in)
    return user_role


@router.get('/{user_role_id}', response_model=schemas.UserRole)
def read_user_role(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        user_role_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get user_role by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    user_role = crud.user_role.get(db=db, id=user_role_id, relations=relations, where=wheres)
    if not user_role:
        raise HTTPException(status_code=404, detail='UserRole not found')
    return user_role


@router.delete('/{user_role_id}', response_model=schemas.Msg)
def delete_user_role(
        *,
        db: Session = Depends(deps.get_db),
        user_role_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an user_role.
    """
    user_role = crud.user_role.get(db=db, id=user_role_id)
    if not user_role:
        raise HTTPException(status_code=404, detail='UserRole not found')
    user_role = crud.user_role.remove(db=db, id=user_role_id)
    return schemas.Msg(msg='UserRole deleted successfully')

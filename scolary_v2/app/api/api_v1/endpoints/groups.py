from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseGroup)
def read_groups(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve groups.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    groups = crud.group.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.group.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseGroup(**{'count': count, 'data': jsonable_encoder(groups)})
    return response


@router.post('/', response_model=schemas.Group)
def create_group(
        *,
        db: Session = Depends(deps.get_db),
        group_in: schemas.GroupCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new group.
    """
    group = crud.group.create(db=db, obj_in=group_in)
    return group


@router.put('/{group_id}', response_model=schemas.Group)
def update_group(
        *,
        db: Session = Depends(deps.get_db),
        group_id: int,
        group_in: schemas.GroupUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an group.
    """
    group = crud.group.get(db=db, id=group_id)
    if not group:
        raise HTTPException(status_code=404, detail='Group not found')
    group = crud.group.update(db=db, db_obj=group, obj_in=group_in)
    return group


@router.get('/{group_id}', response_model=schemas.Group)
def read_group(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        group_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get group by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    group = crud.group.get(db=db, id=group_id, relations=relations, where=wheres)
    if not group:
        raise HTTPException(status_code=404, detail='Group not found')
    return group


@router.delete('/{group_id}', response_model=schemas.Msg)
def delete_group(
        *,
        db: Session = Depends(deps.get_db),
        group_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an group.
    """
    group = crud.group.get(db=db, id=group_id)
    if not group:
        raise HTTPException(status_code=404, detail='Group not found')
    group = crud.group.remove(db=db, id=group_id)
    return schemas.Msg(msg='Group deleted successfully')

from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseTeachingUnitOptionalGroup)
def read_teaching_unit_optional_groups(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve teaching_unit_optional_groups.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    teaching_unit_optional_groups = crud.teaching_unit_optional_group.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.teaching_unit_optional_group.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseTeachingUnitOptionalGroup(**{'count': count, 'data': jsonable_encoder(teaching_unit_optional_groups)})
    return response


@router.post('/', response_model=schemas.TeachingUnitOptionalGroup)
def create_teaching_unit_optional_group(
        *,
        db: Session = Depends(deps.get_db),
        teaching_unit_optional_group_in: schemas.TeachingUnitOptionalGroupCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new teaching_unit_optional_group.
    """
    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_in)
    return teaching_unit_optional_group


@router.put('/{teaching_unit_optional_group_id}', response_model=schemas.TeachingUnitOptionalGroup)
def update_teaching_unit_optional_group(
        *,
        db: Session = Depends(deps.get_db),
        teaching_unit_optional_group_id: int,
        teaching_unit_optional_group_in: schemas.TeachingUnitOptionalGroupUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an teaching_unit_optional_group.
    """
    teaching_unit_optional_group = crud.teaching_unit_optional_group.get(db=db, id=teaching_unit_optional_group_id)
    if not teaching_unit_optional_group:
        raise HTTPException(status_code=404, detail='TeachingUnitOptionalGroup not found')
    teaching_unit_optional_group = crud.teaching_unit_optional_group.update(db=db, db_obj=teaching_unit_optional_group, obj_in=teaching_unit_optional_group_in)
    return teaching_unit_optional_group


@router.get('/{teaching_unit_optional_group_id}', response_model=schemas.TeachingUnitOptionalGroup)
def read_teaching_unit_optional_group(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        teaching_unit_optional_group_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get teaching_unit_optional_group by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    teaching_unit_optional_group = crud.teaching_unit_optional_group.get(db=db, id=teaching_unit_optional_group_id, relations=relations, where=wheres)
    if not teaching_unit_optional_group:
        raise HTTPException(status_code=404, detail='TeachingUnitOptionalGroup not found')
    return teaching_unit_optional_group


@router.delete('/{teaching_unit_optional_group_id}', response_model=schemas.Msg)
def delete_teaching_unit_optional_group(
        *,
        db: Session = Depends(deps.get_db),
        teaching_unit_optional_group_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an teaching_unit_optional_group.
    """
    teaching_unit_optional_group = crud.teaching_unit_optional_group.get(db=db, id=teaching_unit_optional_group_id)
    if not teaching_unit_optional_group:
        raise HTTPException(status_code=404, detail='TeachingUnitOptionalGroup not found')
    teaching_unit_optional_group = crud.teaching_unit_optional_group.remove(db=db, id=teaching_unit_optional_group_id)
    return schemas.Msg(msg='TeachingUnitOptionalGroup deleted successfully')

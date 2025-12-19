from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseTeachingUnit)
def read_teaching_units(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve teaching_units.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    teaching_units = crud.teaching_unit.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.teaching_unit.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseTeachingUnit(**{'count': count, 'data': jsonable_encoder(teaching_units)})
    return response


@router.post('/', response_model=schemas.TeachingUnit)
def create_teaching_unit(
        *,
        db: Session = Depends(deps.get_db),
        teaching_unit_in: schemas.TeachingUnitCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new teaching_unit.
    """
    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_in)
    return teaching_unit


@router.put('/{teaching_unit_id}', response_model=schemas.TeachingUnit)
def update_teaching_unit(
        *,
        db: Session = Depends(deps.get_db),
        teaching_unit_id: int,
        teaching_unit_in: schemas.TeachingUnitUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an teaching_unit.
    """
    teaching_unit = crud.teaching_unit.get(db=db, id=teaching_unit_id)
    if not teaching_unit:
        raise HTTPException(status_code=404, detail='TeachingUnit not found')
    teaching_unit = crud.teaching_unit.update(db=db, db_obj=teaching_unit, obj_in=teaching_unit_in)
    return teaching_unit


@router.get('/{teaching_unit_id}', response_model=schemas.TeachingUnit)
def read_teaching_unit(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        teaching_unit_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get teaching_unit by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    teaching_unit = crud.teaching_unit.get(db=db, id=teaching_unit_id, relations=relations, where=wheres)
    if not teaching_unit:
        raise HTTPException(status_code=404, detail='TeachingUnit not found')
    return teaching_unit


@router.delete('/{teaching_unit_id}', response_model=schemas.Msg)
def delete_teaching_unit(
        *,
        db: Session = Depends(deps.get_db),
        teaching_unit_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an teaching_unit.
    """
    teaching_unit = crud.teaching_unit.get(db=db, id=teaching_unit_id)
    if not teaching_unit:
        raise HTTPException(status_code=404, detail='TeachingUnit not found')
    teaching_unit = crud.teaching_unit.remove(db=db, id=teaching_unit_id)
    return schemas.Msg(msg='TeachingUnit deleted successfully')

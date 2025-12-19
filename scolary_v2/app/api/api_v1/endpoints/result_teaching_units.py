from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseResultTeachingUnit)
def read_result_teaching_units(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve result_teaching_units.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    result_teaching_units = crud.result_teaching_unit.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.result_teaching_unit.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseResultTeachingUnit(**{'count': count, 'data': jsonable_encoder(result_teaching_units)})
    return response


@router.post('/', response_model=schemas.ResultTeachingUnit)
def create_result_teaching_unit(
        *,
        db: Session = Depends(deps.get_db),
        result_teaching_unit_in: schemas.ResultTeachingUnitCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new result_teaching_unit.
    """
    result_teaching_unit = crud.result_teaching_unit.create(db=db, obj_in=result_teaching_unit_in)
    return result_teaching_unit


@router.put('/{result_teaching_unit_id}', response_model=schemas.ResultTeachingUnit)
def update_result_teaching_unit(
        *,
        db: Session = Depends(deps.get_db),
        result_teaching_unit_id: int,
        result_teaching_unit_in: schemas.ResultTeachingUnitUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an result_teaching_unit.
    """
    result_teaching_unit = crud.result_teaching_unit.get(db=db, id=result_teaching_unit_id)
    if not result_teaching_unit:
        raise HTTPException(status_code=404, detail='ResultTeachingUnit not found')
    result_teaching_unit = crud.result_teaching_unit.update(db=db, db_obj=result_teaching_unit, obj_in=result_teaching_unit_in)
    return result_teaching_unit


@router.get('/{result_teaching_unit_id}', response_model=schemas.ResultTeachingUnit)
def read_result_teaching_unit(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        result_teaching_unit_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get result_teaching_unit by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    result_teaching_unit = crud.result_teaching_unit.get(db=db, id=result_teaching_unit_id, relations=relations, where=wheres)
    if not result_teaching_unit:
        raise HTTPException(status_code=404, detail='ResultTeachingUnit not found')
    return result_teaching_unit


@router.delete('/{result_teaching_unit_id}', response_model=schemas.Msg)
def delete_result_teaching_unit(
        *,
        db: Session = Depends(deps.get_db),
        result_teaching_unit_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an result_teaching_unit.
    """
    result_teaching_unit = crud.result_teaching_unit.get(db=db, id=result_teaching_unit_id)
    if not result_teaching_unit:
        raise HTTPException(status_code=404, detail='ResultTeachingUnit not found')
    result_teaching_unit = crud.result_teaching_unit.remove(db=db, id=result_teaching_unit_id)
    return schemas.Msg(msg='ResultTeachingUnit deleted successfully')

from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseWorkingTime)
def read_working_times(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve working_times.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    working_times = crud.working_time.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.working_time.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseWorkingTime(**{'count': count, 'data': jsonable_encoder(working_times)})
    return response


@router.post('/', response_model=schemas.WorkingTime)
def create_working_time(
        *,
        db: Session = Depends(deps.get_db),
        working_time_in: schemas.WorkingTimeCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new working_time.
    """
    working_time = crud.working_time.create(db=db, obj_in=working_time_in)
    return working_time


@router.put('/{working_time_id}', response_model=schemas.WorkingTime)
def update_working_time(
        *,
        db: Session = Depends(deps.get_db),
        working_time_id: int,
        working_time_in: schemas.WorkingTimeUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an working_time.
    """
    working_time = crud.working_time.get(db=db, id=working_time_id)
    if not working_time:
        raise HTTPException(status_code=404, detail='WorkingTime not found')
    working_time = crud.working_time.update(db=db, db_obj=working_time, obj_in=working_time_in)
    return working_time


@router.get('/{working_time_id}', response_model=schemas.WorkingTime)
def read_working_time(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        working_time_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get working_time by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    working_time = crud.working_time.get(db=db, id=working_time_id, relations=relations, where=wheres)
    if not working_time:
        raise HTTPException(status_code=404, detail='WorkingTime not found')
    return working_time


@router.delete('/{working_time_id}', response_model=schemas.Msg)
def delete_working_time(
        *,
        db: Session = Depends(deps.get_db),
        working_time_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an working_time.
    """
    working_time = crud.working_time.get(db=db, id=working_time_id)
    if not working_time:
        raise HTTPException(status_code=404, detail='WorkingTime not found')
    working_time = crud.working_time.remove(db=db, id=working_time_id)
    return schemas.Msg(msg='WorkingTime deleted successfully')

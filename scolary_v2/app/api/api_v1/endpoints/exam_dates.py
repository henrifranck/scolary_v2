from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseExamDate)
def read_exam_dates(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve exam_dates.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    exam_dates = crud.exam_date.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.exam_date.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseExamDate(**{'count': count, 'data': jsonable_encoder(exam_dates)})
    return response


@router.post('/', response_model=schemas.ExamDate)
def create_exam_date(
        *,
        db: Session = Depends(deps.get_db),
        exam_date_in: schemas.ExamDateCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new exam_date.
    """
    exam_date = crud.exam_date.create(db=db, obj_in=exam_date_in)
    return exam_date


@router.put('/{exam_date_id}', response_model=schemas.ExamDate)
def update_exam_date(
        *,
        db: Session = Depends(deps.get_db),
        exam_date_id: int,
        exam_date_in: schemas.ExamDateUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an exam_date.
    """
    exam_date = crud.exam_date.get(db=db, id=exam_date_id)
    if not exam_date:
        raise HTTPException(status_code=404, detail='ExamDate not found')
    exam_date = crud.exam_date.update(db=db, db_obj=exam_date, obj_in=exam_date_in)
    return exam_date


@router.get('/{exam_date_id}', response_model=schemas.ExamDate)
def read_exam_date(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        exam_date_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get exam_date by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    exam_date = crud.exam_date.get(db=db, id=exam_date_id, relations=relations, where=wheres)
    if not exam_date:
        raise HTTPException(status_code=404, detail='ExamDate not found')
    return exam_date


@router.delete('/{exam_date_id}', response_model=schemas.Msg)
def delete_exam_date(
        *,
        db: Session = Depends(deps.get_db),
        exam_date_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an exam_date.
    """
    exam_date = crud.exam_date.get(db=db, id=exam_date_id)
    if not exam_date:
        raise HTTPException(status_code=404, detail='ExamDate not found')
    exam_date = crud.exam_date.remove(db=db, id=exam_date_id)
    return schemas.Msg(msg='ExamDate deleted successfully')

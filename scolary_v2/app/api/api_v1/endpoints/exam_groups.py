from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseExamGroup)
def read_exam_groups(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve exam_groups.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    exam_groups = crud.exam_group.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.exam_group.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseExamGroup(**{'count': count, 'data': jsonable_encoder(exam_groups)})
    return response


@router.post('/', response_model=schemas.ExamGroup)
def create_exam_group(
        *,
        db: Session = Depends(deps.get_db),
        exam_group_in: schemas.ExamGroupCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new exam_group.
    """
    exam_group = crud.exam_group.create(db=db, obj_in=exam_group_in)
    return exam_group


@router.put('/{exam_group_id}', response_model=schemas.ExamGroup)
def update_exam_group(
        *,
        db: Session = Depends(deps.get_db),
        exam_group_id: int,
        exam_group_in: schemas.ExamGroupUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an exam_group.
    """
    exam_group = crud.exam_group.get(db=db, id=exam_group_id)
    if not exam_group:
        raise HTTPException(status_code=404, detail='ExamGroup not found')
    exam_group = crud.exam_group.update(db=db, db_obj=exam_group, obj_in=exam_group_in)
    return exam_group


@router.get('/{exam_group_id}', response_model=schemas.ExamGroup)
def read_exam_group(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        exam_group_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get exam_group by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    exam_group = crud.exam_group.get(db=db, id=exam_group_id, relations=relations, where=wheres)
    if not exam_group:
        raise HTTPException(status_code=404, detail='ExamGroup not found')
    return exam_group


@router.delete('/{exam_group_id}', response_model=schemas.Msg)
def delete_exam_group(
        *,
        db: Session = Depends(deps.get_db),
        exam_group_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an exam_group.
    """
    exam_group = crud.exam_group.get(db=db, id=exam_group_id)
    if not exam_group:
        raise HTTPException(status_code=404, detail='ExamGroup not found')
    exam_group = crud.exam_group.remove(db=db, id=exam_group_id)
    return schemas.Msg(msg='ExamGroup deleted successfully')

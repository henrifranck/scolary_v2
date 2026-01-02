from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps


@router.get('/', response_model=schemas.ResponseTeacher)
def read_teachers(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve teachers.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
        relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
        wheres += ast.literal_eval(where)

    teachers = crud.teacher.get_multi_where_array(
        db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.teacher.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseTeacher(**{'count': count, 'data': jsonable_encoder(teachers)})
    return response


@router.post('/', response_model=schemas.Teacher)
def create_teacher(
        *,
        db: Session = Depends(deps.get_db),
        teacher_in: schemas.TeacherCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new teacher.
    """
    teacher = crud.teacher.create(db=db, obj_in=teacher_in)
    return teacher


@router.put('/{teacher_id}', response_model=schemas.Teacher)
def update_teacher(
        *,
        db: Session = Depends(deps.get_db),
        teacher_id: int,
        teacher_in: schemas.TeacherUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an teacher.
    """
    teacher = crud.teacher.get(db=db, id=teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail='Teacher not found')
    teacher = crud.teacher.update(db=db, db_obj=teacher, obj_in=teacher_in)
    return teacher


@router.get('/{teacher_id}', response_model=schemas.Teacher)
def read_teacher(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        teacher_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get teacher by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
        relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
        wheres += ast.literal_eval(where)

    teacher = crud.teacher.get(db=db, id=teacher_id, relations=relations, where=wheres)
    if not teacher:
        raise HTTPException(status_code=404, detail='Teacher not found')
    return teacher


@router.delete('/{teacher_id}', response_model=schemas.Msg)
def delete_teacher(
        *,
        db: Session = Depends(deps.get_db),
        teacher_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an teacher.
    """
    teacher = crud.teacher.get(db=db, id=teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail='Teacher not found')
    teacher = crud.teacher.remove(db=db, id=teacher_id)
    return schemas.Msg(msg='Teacher deleted successfully')

from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps


@router.get('/', response_model=schemas.ResponseClassroom)
def read_classrooms(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve classrooms.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
        relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
        wheres += ast.literal_eval(where)

    classrooms = crud.classroom.get_multi_where_array(
        db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.classroom.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseClassroom(**{'count': count, 'data': jsonable_encoder(classrooms)})
    return response


@router.post('/', response_model=schemas.Classroom)
def create_classroom(
        *,
        db: Session = Depends(deps.get_db),
        classroom_in: schemas.ClassroomCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new classroom.
    """
    classroom = crud.classroom.create(db=db, obj_in=classroom_in)
    return classroom


@router.put('/{classroom_id}', response_model=schemas.Classroom)
def update_classroom(
        *,
        db: Session = Depends(deps.get_db),
        classroom_id: int,
        classroom_in: schemas.ClassroomUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an classroom.
    """
    classroom = crud.classroom.get(db=db, id=classroom_id)
    if not classroom:
        raise HTTPException(status_code=404, detail='Classroom not found')
    classroom = crud.classroom.update(db=db, db_obj=classroom, obj_in=classroom_in)
    return classroom


@router.get('/{classroom_id}', response_model=schemas.Classroom)
def read_classroom(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        classroom_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get classroom by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
        relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
        wheres += ast.literal_eval(where)

    classroom = crud.classroom.get(db=db, id=classroom_id, relations=relations, where=wheres)
    if not classroom:
        raise HTTPException(status_code=404, detail='Classroom not found')
    return classroom


@router.delete('/{classroom_id}', response_model=schemas.Msg)
def delete_classroom(
        *,
        db: Session = Depends(deps.get_db),
        classroom_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an classroom.
    """
    classroom = crud.classroom.get(db=db, id=classroom_id)
    if not classroom:
        raise HTTPException(status_code=404, detail='Classroom not found')
    classroom = crud.classroom.remove(db=db, id=classroom_id)
    return schemas.Msg(msg='Classroom deleted successfully')

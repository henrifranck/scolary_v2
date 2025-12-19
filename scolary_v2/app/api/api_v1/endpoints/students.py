from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps


@router.get('/', response_model=schemas.ResponseStudent)
def read_students(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where_relation: str = "[]",
        base_column: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve students.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
        relations += ast.literal_eval(relation)

    wheres_relations = []
    if where_relation is not None and where_relation != "" and where_relation != []:
        wheres_relations += ast.literal_eval(where_relation)

    base_columns = []
    if base_column is not None and base_column != "" and base_column != []:
        base_columns += ast.literal_eval(base_column)

    wheres = []
    if where is not None and where != "" and where != []:
        wheres += ast.literal_eval(where)

    students = crud.student.get_multi_where_array(
        db=db, relations=relations, skip=offset, limit=limit, where=wheres, base_columns=base_columns,
        where_relation=wheres_relations)
    count = crud.student.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseStudent(**{'count': count, 'data': jsonable_encoder(students)})
    return response


@router.get('/one_student', response_model=schemas.StudentWithRelation)
def read_one_student(
        *,
        relation: str = "[]",
        where: str = "[]",
        where_relation: str = "[]",
        base_column: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve students.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
        relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
        wheres += ast.literal_eval(where)

    wheres_relations = []
    if where_relation is not None and where_relation != "" and where_relation != []:
        wheres_relations += ast.literal_eval(where_relation)

    base_columns = []
    if base_column is not None and base_column != "" and base_column != []:
        base_columns += ast.literal_eval(base_column)

    student = crud.student.get_first_where_array(
        db=db, relations=relations, where=wheres, base_columns=base_columns, where_relation=wheres_relations)
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')

    return jsonable_encoder(student)


@router.post('/', response_model=schemas.Student)
def create_student(
        *,
        db: Session = Depends(deps.get_db),
        student_in: schemas.StudentCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new student.
    """
    student = crud.student.create(db=db, obj_in=student_in)
    return student


@router.put('/{student_id}', response_model=schemas.Student)
def update_student(
        *,
        db: Session = Depends(deps.get_db),
        student_id: int,
        student_in: schemas.StudentUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an student.
    """
    student = crud.student.get(db=db, id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')
    student = crud.student.update(db=db, db_obj=student, obj_in=student_in)
    return student


@router.get('/{student_id}', response_model=schemas.Student)
def read_student(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        student_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get student by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
        relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
        wheres += ast.literal_eval(where)

    student = crud.student.get(db=db, id=student_id, relations=relations, where=wheres)
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')
    return student


@router.delete('/{student_id}', response_model=schemas.Msg)
def delete_student(
        *,
        db: Session = Depends(deps.get_db),
        student_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an student.
    """
    student = crud.student.get(db=db, id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')
    student = crud.student.remove(db=db, id=student_id)
    return schemas.Msg(msg='Student deleted successfully')

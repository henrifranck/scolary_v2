from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseUniversity)
def read_universitys(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve universitys.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    universitys = crud.university.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.university.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseUniversity(**{'count': count, 'data': jsonable_encoder(universitys)})
    return response


@router.post('/', response_model=schemas.University)
def create_university(
        *,
        db: Session = Depends(deps.get_db),
        university_in: schemas.UniversityCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new university.
    """
    university = crud.university.create(db=db, obj_in=university_in)
    return university


@router.put('/{university_id}', response_model=schemas.University)
def update_university(
        *,
        db: Session = Depends(deps.get_db),
        university_id: int,
        university_in: schemas.UniversityUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an university.
    """
    university = crud.university.get(db=db, id=university_id)
    if not university:
        raise HTTPException(status_code=404, detail='University not found')
    university = crud.university.update(db=db, db_obj=university, obj_in=university_in)
    return university


@router.get('/{university_id}', response_model=schemas.University)
def read_university(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        university_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get university by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    university = crud.university.get(db=db, id=university_id, relations=relations, where=wheres)
    if not university:
        raise HTTPException(status_code=404, detail='University not found')
    return university


@router.delete('/{university_id}', response_model=schemas.Msg)
def delete_university(
        *,
        db: Session = Depends(deps.get_db),
        university_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an university.
    """
    university = crud.university.get(db=db, id=university_id)
    if not university:
        raise HTTPException(status_code=404, detail='University not found')
    university = crud.university.remove(db=db, id=university_id)
    return schemas.Msg(msg='University deleted successfully')

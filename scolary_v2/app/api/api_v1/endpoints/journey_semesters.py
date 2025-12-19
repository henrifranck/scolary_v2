from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseJourneySemester)
def read_journey_semesters(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve journey_semesters.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    journey_semesters = crud.journey_semester.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.journey_semester.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseJourneySemester(**{'count': count, 'data': jsonable_encoder(journey_semesters)})
    return response


@router.post('/', response_model=schemas.JourneySemester)
def create_journey_semester(
        *,
        db: Session = Depends(deps.get_db),
        journey_semester_in: schemas.JourneySemesterCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new journey_semester.
    """
    journey_semester = crud.journey_semester.create(db=db, obj_in=journey_semester_in)
    return journey_semester


@router.put('/{journey_semester_id}', response_model=schemas.JourneySemester)
def update_journey_semester(
        *,
        db: Session = Depends(deps.get_db),
        journey_semester_id: int,
        journey_semester_in: schemas.JourneySemesterUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an journey_semester.
    """
    journey_semester = crud.journey_semester.get(db=db, id=journey_semester_id)
    if not journey_semester:
        raise HTTPException(status_code=404, detail='JourneySemester not found')
    journey_semester = crud.journey_semester.update(db=db, db_obj=journey_semester, obj_in=journey_semester_in)
    return journey_semester


@router.get('/{journey_semester_id}', response_model=schemas.JourneySemester)
def read_journey_semester(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        journey_semester_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get journey_semester by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    journey_semester = crud.journey_semester.get(db=db, id=journey_semester_id, relations=relations, where=wheres)
    if not journey_semester:
        raise HTTPException(status_code=404, detail='JourneySemester not found')
    return journey_semester


@router.delete('/{journey_semester_id}', response_model=schemas.Msg)
def delete_journey_semester(
        *,
        db: Session = Depends(deps.get_db),
        journey_semester_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an journey_semester.
    """
    journey_semester = crud.journey_semester.get(db=db, id=journey_semester_id)
    if not journey_semester:
        raise HTTPException(status_code=404, detail='JourneySemester not found')
    journey_semester = crud.journey_semester.remove(db=db, id=journey_semester_id)
    return schemas.Msg(msg='JourneySemester deleted successfully')

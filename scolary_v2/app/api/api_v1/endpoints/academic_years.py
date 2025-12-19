from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseAcademicYear)
def read_academic_years(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve academic_years.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    academic_years = crud.academic_year.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.academic_year.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseAcademicYear(**{'count': count, 'data': jsonable_encoder(academic_years)})
    return response


@router.post('/', response_model=schemas.AcademicYear)
def create_academic_year(
        *,
        db: Session = Depends(deps.get_db),
        academic_year_in: schemas.AcademicYearCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new academic_year.
    """
    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_in)
    return academic_year


@router.put('/{academic_year_id}', response_model=schemas.AcademicYear)
def update_academic_year(
        *,
        db: Session = Depends(deps.get_db),
        academic_year_id: int,
        academic_year_in: schemas.AcademicYearUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an academic_year.
    """
    academic_year = crud.academic_year.get(db=db, id=academic_year_id)
    if not academic_year:
        raise HTTPException(status_code=404, detail='AcademicYear not found')
    academic_year = crud.academic_year.update(db=db, db_obj=academic_year, obj_in=academic_year_in)
    return academic_year


@router.get('/{academic_year_id}', response_model=schemas.AcademicYear)
def read_academic_year(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        academic_year_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get academic_year by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    academic_year = crud.academic_year.get(db=db, id=academic_year_id, relations=relations, where=wheres)
    if not academic_year:
        raise HTTPException(status_code=404, detail='AcademicYear not found')
    return academic_year


@router.delete('/{academic_year_id}', response_model=schemas.Msg)
def delete_academic_year(
        *,
        db: Session = Depends(deps.get_db),
        academic_year_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an academic_year.
    """
    academic_year = crud.academic_year.get(db=db, id=academic_year_id)
    if not academic_year:
        raise HTTPException(status_code=404, detail='AcademicYear not found')
    academic_year = crud.academic_year.remove(db=db, id=academic_year_id)
    return schemas.Msg(msg='AcademicYear deleted successfully')

from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseNationality)
def read_nationalitys(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve nationalitys.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    nationalitys = crud.nationality.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.nationality.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseNationality(**{'count': count, 'data': jsonable_encoder(nationalitys)})
    return response


@router.post('/', response_model=schemas.Nationality)
def create_nationality(
        *,
        db: Session = Depends(deps.get_db),
        nationality_in: schemas.NationalityCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new nationality.
    """
    nationality = crud.nationality.create(db=db, obj_in=nationality_in)
    return nationality


@router.put('/{nationality_id}', response_model=schemas.Nationality)
def update_nationality(
        *,
        db: Session = Depends(deps.get_db),
        nationality_id: int,
        nationality_in: schemas.NationalityUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an nationality.
    """
    nationality = crud.nationality.get(db=db, id=nationality_id)
    if not nationality:
        raise HTTPException(status_code=404, detail='Nationality not found')
    nationality = crud.nationality.update(db=db, db_obj=nationality, obj_in=nationality_in)
    return nationality


@router.get('/{nationality_id}', response_model=schemas.Nationality)
def read_nationality(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        nationality_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get nationality by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    nationality = crud.nationality.get(db=db, id=nationality_id, relations=relations, where=wheres)
    if not nationality:
        raise HTTPException(status_code=404, detail='Nationality not found')
    return nationality


@router.delete('/{nationality_id}', response_model=schemas.Msg)
def delete_nationality(
        *,
        db: Session = Depends(deps.get_db),
        nationality_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an nationality.
    """
    nationality = crud.nationality.get(db=db, id=nationality_id)
    if not nationality:
        raise HTTPException(status_code=404, detail='Nationality not found')
    nationality = crud.nationality.remove(db=db, id=nationality_id)
    return schemas.Msg(msg='Nationality deleted successfully')

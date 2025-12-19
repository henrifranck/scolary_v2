from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseBaccalaureateSerie)
def read_baccalaureate_series(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve baccalaureate_series.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    baccalaureate_series = crud.baccalaureate_serie.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.baccalaureate_serie.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseBaccalaureateSerie(**{'count': count, 'data': jsonable_encoder(baccalaureate_series)})
    return response


@router.post('/', response_model=schemas.BaccalaureateSerie)
def create_baccalaureate_serie(
        *,
        db: Session = Depends(deps.get_db),
        baccalaureate_serie_in: schemas.BaccalaureateSerieCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new baccalaureate_serie.
    """
    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_in)
    return baccalaureate_serie


@router.put('/{baccalaureate_serie_id}', response_model=schemas.BaccalaureateSerie)
def update_baccalaureate_serie(
        *,
        db: Session = Depends(deps.get_db),
        baccalaureate_serie_id: int,
        baccalaureate_serie_in: schemas.BaccalaureateSerieUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an baccalaureate_serie.
    """
    baccalaureate_serie = crud.baccalaureate_serie.get(db=db, id=baccalaureate_serie_id)
    if not baccalaureate_serie:
        raise HTTPException(status_code=404, detail='BaccalaureateSerie not found')
    baccalaureate_serie = crud.baccalaureate_serie.update(db=db, db_obj=baccalaureate_serie, obj_in=baccalaureate_serie_in)
    return baccalaureate_serie


@router.get('/{baccalaureate_serie_id}', response_model=schemas.BaccalaureateSerie)
def read_baccalaureate_serie(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        baccalaureate_serie_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get baccalaureate_serie by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    baccalaureate_serie = crud.baccalaureate_serie.get(db=db, id=baccalaureate_serie_id, relations=relations, where=wheres)
    if not baccalaureate_serie:
        raise HTTPException(status_code=404, detail='BaccalaureateSerie not found')
    return baccalaureate_serie


@router.delete('/{baccalaureate_serie_id}', response_model=schemas.Msg)
def delete_baccalaureate_serie(
        *,
        db: Session = Depends(deps.get_db),
        baccalaureate_serie_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an baccalaureate_serie.
    """
    baccalaureate_serie = crud.baccalaureate_serie.get(db=db, id=baccalaureate_serie_id)
    if not baccalaureate_serie:
        raise HTTPException(status_code=404, detail='BaccalaureateSerie not found')
    baccalaureate_serie = crud.baccalaureate_serie.remove(db=db, id=baccalaureate_serie_id)
    return schemas.Msg(msg='BaccalaureateSerie deleted successfully')

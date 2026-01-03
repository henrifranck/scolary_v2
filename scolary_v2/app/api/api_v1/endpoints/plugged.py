from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponsePlugged)
def read_pluggeds(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve pluggeds.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    pluggeds = crud.plugged.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.plugged.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponsePlugged(**{'count': count, 'data': jsonable_encoder(pluggeds)})
    return response


@router.post('/', response_model=schemas.Plugged)
def create_plugged(
        *,
        db: Session = Depends(deps.get_db),
        plugged_in: schemas.PluggedCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new plugged.
    """
    plugged = crud.plugged.create(db=db, obj_in=plugged_in)
    return plugged


@router.put('/{plugged_id}', response_model=schemas.Plugged)
def update_plugged(
        *,
        db: Session = Depends(deps.get_db),
        plugged_id: int,
        plugged_in: schemas.PluggedUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an plugged.
    """
    plugged = crud.plugged.get(db=db, id=plugged_id)
    if not plugged:
        raise HTTPException(status_code=404, detail='Plugged not found')
    plugged = crud.plugged.update(db=db, db_obj=plugged, obj_in=plugged_in)
    return plugged


@router.get('/{plugged_id}', response_model=schemas.Plugged)
def read_plugged(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        plugged_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get plugged by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    plugged = crud.plugged.get(db=db, id=plugged_id, relations=relations, where=wheres)
    if not plugged:
        raise HTTPException(status_code=404, detail='Plugged not found')
    return plugged


@router.delete('/{plugged_id}', response_model=schemas.Msg)
def delete_plugged(
        *,
        db: Session = Depends(deps.get_db),
        plugged_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an plugged.
    """
    plugged = crud.plugged.get(db=db, id=plugged_id)
    if not plugged:
        raise HTTPException(status_code=404, detail='Plugged not found')
    plugged = crud.plugged.remove(db=db, id=plugged_id)
    return schemas.Msg(msg='Plugged deleted successfully')

from typing import Any
import ast

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get('/', response_model=schemas.ResponseAvailableModel)
def read_available_models(
    *,
    offset: int = 0,
    limit: int = 20,
    relation: str = "[]",
    where: str = "[]",
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve available models.
    """
    relations = []
    if relation not in (None, "", [], "[]"):
        relations += ast.literal_eval(relation)

    wheres = []
    if where not in (None, "", []):
        wheres += ast.literal_eval(where)

    available_models = crud.available_model.get_multi_where_array(
        db=db, relations=relations, skip=offset, limit=limit, where=wheres
    )
    count = crud.available_model.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseAvailableModel(
        **{'count': count, 'data': jsonable_encoder(available_models)}
    )
    return response


@router.post('/', response_model=schemas.AvailableModel)
def create_available_model(
    *,
    db: Session = Depends(deps.get_db),
    available_model_in: schemas.AvailableModelCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new available model.
    """
    available_model = crud.available_model.create(db=db, obj_in=available_model_in)
    return available_model


@router.put('/{available_model_id}', response_model=schemas.AvailableModel)
def update_available_model(
    *,
    db: Session = Depends(deps.get_db),
    available_model_id: int,
    available_model_in: schemas.AvailableModelUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an available model.
    """
    available_model = crud.available_model.get(db=db, id=available_model_id)
    if not available_model:
        raise HTTPException(status_code=404, detail='AvailableModel not found')
    available_model = crud.available_model.update(
        db=db, db_obj=available_model, obj_in=available_model_in
    )
    return available_model


@router.get('/{available_model_id}', response_model=schemas.AvailableModel)
def read_available_model(
    *,
    relation: str = "[]",
    where: str = "[]",
    db: Session = Depends(deps.get_db),
    available_model_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get available model by ID.
    """
    relations = []
    if relation not in (None, "", [], "[]"):
        relations += ast.literal_eval(relation)

    wheres = []
    if where not in (None, "", []):
        wheres += ast.literal_eval(where)

    available_model = crud.available_model.get(
        db=db, id=available_model_id, relations=relations, where=wheres
    )
    if not available_model:
        raise HTTPException(status_code=404, detail='AvailableModel not found')
    return available_model


@router.delete('/{available_model_id}', response_model=schemas.Msg)
def delete_available_model(
    *,
    db: Session = Depends(deps.get_db),
    available_model_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an available model.
    """
    available_model = crud.available_model.get(db=db, id=available_model_id)
    if not available_model:
        raise HTTPException(status_code=404, detail='AvailableModel not found')
    crud.available_model.remove(db=db, id=available_model_id)
    return schemas.Msg(msg='AvailableModel deleted successfully')

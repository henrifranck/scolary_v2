from typing import Any
import ast

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get('/', response_model=schemas.ResponseAvailableService)
def read_available_services(
    *,
    offset: int = 0,
    limit: int = 20,
    relation: str = "[]",
    where: str = "[]",
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve available services.
    """
    relations = []
    if relation not in (None, "", [], "[]"):
        relations += ast.literal_eval(relation)

    wheres = []
    if where not in (None, "", []):
        wheres += ast.literal_eval(where)

    available_services = crud.available_service.get_multi_where_array(
        db=db, relations=relations, skip=offset, limit=limit, where=wheres
    )
    count = crud.available_service.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseAvailableService(
        **{'count': count, 'data': jsonable_encoder(available_services)}
    )
    return response


@router.post('/', response_model=schemas.AvailableService)
def create_available_service(
    *,
    db: Session = Depends(deps.get_db),
    available_service_in: schemas.AvailableServiceCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new available service.
    """
    available_service = crud.available_service.create(db=db, obj_in=available_service_in)
    return available_service


@router.put('/{available_service_id}', response_model=schemas.AvailableService)
def update_available_service(
    *,
    db: Session = Depends(deps.get_db),
    available_service_id: int,
    available_service_in: schemas.AvailableServiceUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an available service.
    """
    available_service = crud.available_service.get(db=db, id=available_service_id)
    if not available_service:
        raise HTTPException(status_code=404, detail='AvailableService not found')
    available_service = crud.available_service.update(
        db=db, db_obj=available_service, obj_in=available_service_in
    )
    return available_service


@router.get('/{available_service_id}', response_model=schemas.AvailableService)
def read_available_service(
    *,
    relation: str = "[]",
    where: str = "[]",
    db: Session = Depends(deps.get_db),
    available_service_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get available service by ID.
    """
    relations = []
    if relation not in (None, "", [], "[]"):
        relations += ast.literal_eval(relation)

    wheres = []
    if where not in (None, "", []):
        wheres += ast.literal_eval(where)

    available_service = crud.available_service.get(
        db=db, id=available_service_id, relations=relations, where=wheres
    )
    if not available_service:
        raise HTTPException(status_code=404, detail='AvailableService not found')
    return available_service


@router.delete('/{available_service_id}', response_model=schemas.Msg)
def delete_available_service(
    *,
    db: Session = Depends(deps.get_db),
    available_service_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an available service.
    """
    available_service = crud.available_service.get(db=db, id=available_service_id)
    if not available_service:
        raise HTTPException(status_code=404, detail='AvailableService not found')
    crud.available_service.remove(db=db, id=available_service_id)
    return schemas.Msg(msg='AvailableService deleted successfully')

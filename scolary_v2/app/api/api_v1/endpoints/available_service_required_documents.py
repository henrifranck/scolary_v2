from typing import Any
import ast

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get('/', response_model=schemas.ResponseAvailableServiceRequiredDocument)
def read_available_service_required_documents(
    *,
    offset: int = 0,
    limit: int = 20,
    relation: str = "[]",
    where: str = "[]",
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve available_service_required_documents.
    """
    relations = []
    if relation not in (None, "", [], "[]"):
        relations += ast.literal_eval(relation)

    wheres = []
    if where not in (None, "", []):
        wheres += ast.literal_eval(where)

    available_service_required_documents = crud.available_service_required_document.get_multi_where_array(
        db=db, relations=relations, skip=offset, limit=limit, where=wheres
    )
    count = crud.available_service_required_document.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseAvailableServiceRequiredDocument(
        **{'count': count, 'data': jsonable_encoder(available_service_required_documents)}
    )
    return response


@router.post('/', response_model=schemas.AvailableServiceRequiredDocument)
def create_available_service_required_document(
    *,
    db: Session = Depends(deps.get_db),
    available_service_required_document_in: schemas.AvailableServiceRequiredDocumentCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new available_service_required_document.
    """
    available_service_required_document = crud.available_service_required_document.create(
        db=db, obj_in=available_service_required_document_in
    )
    return available_service_required_document


@router.put('/{available_service_required_document_id}', response_model=schemas.AvailableServiceRequiredDocument)
def update_available_service_required_document(
    *,
    db: Session = Depends(deps.get_db),
    available_service_required_document_id: int,
    available_service_required_document_in: schemas.AvailableServiceRequiredDocumentUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an available_service_required_document.
    """
    available_service_required_document = crud.available_service_required_document.get(
        db=db, id=available_service_required_document_id
    )
    if not available_service_required_document:
        raise HTTPException(status_code=404, detail='AvailableServiceRequiredDocument not found')
    available_service_required_document = crud.available_service_required_document.update(
        db=db,
        db_obj=available_service_required_document,
        obj_in=available_service_required_document_in,
    )
    return available_service_required_document


@router.get('/{available_service_required_document_id}', response_model=schemas.AvailableServiceRequiredDocument)
def read_available_service_required_document(
    *,
    relation: str = "[]",
    where: str = "[]",
    db: Session = Depends(deps.get_db),
    available_service_required_document_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get available_service_required_document by ID.
    """
    relations = []
    if relation not in (None, "", [], "[]"):
        relations += ast.literal_eval(relation)

    wheres = []
    if where not in (None, "", []):
        wheres += ast.literal_eval(where)

    available_service_required_document = crud.available_service_required_document.get(
        db=db,
        id=available_service_required_document_id,
        relations=relations,
        where=wheres,
    )
    if not available_service_required_document:
        raise HTTPException(status_code=404, detail='AvailableServiceRequiredDocument not found')
    return available_service_required_document


@router.delete('/{available_service_required_document_id}', response_model=schemas.Msg)
def delete_available_service_required_document(
    *,
    db: Session = Depends(deps.get_db),
    available_service_required_document_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an available_service_required_document.
    """
    available_service_required_document = crud.available_service_required_document.get(
        db=db, id=available_service_required_document_id
    )
    if not available_service_required_document:
        raise HTTPException(status_code=404, detail='AvailableServiceRequiredDocument not found')
    crud.available_service_required_document.remove(db=db, id=available_service_required_document_id)
    return schemas.Msg(msg='AvailableServiceRequiredDocument deleted successfully')

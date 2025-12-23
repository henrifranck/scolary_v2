from typing import Any
import ast

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get('/', response_model=schemas.ResponseRequiredDocument)
def read_required_documents(
    *,
    offset: int = 0,
    limit: int = 20,
    relation: str = "[]",
    where: str = "[]",
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve required documents.
    """
    relations = []
    if relation not in (None, "", [], "[]"):
        relations += ast.literal_eval(relation)

    wheres = []
    if where not in (None, "", []):
        wheres += ast.literal_eval(where)

    required_documents = crud.required_document.get_multi_where_array(
        db=db, relations=relations, skip=offset, limit=limit, where=wheres
    )
    count = crud.required_document.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseRequiredDocument(
        **{'count': count, 'data': jsonable_encoder(required_documents)}
    )
    return response


@router.post('/', response_model=schemas.RequiredDocument)
def create_required_document(
    *,
    db: Session = Depends(deps.get_db),
    required_document_in: schemas.RequiredDocumentCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new required document.
    """
    required_document = crud.required_document.create(db=db, obj_in=required_document_in)
    return required_document


@router.put('/{required_document_id}', response_model=schemas.RequiredDocument)
def update_required_document(
    *,
    db: Session = Depends(deps.get_db),
    required_document_id: int,
    required_document_in: schemas.RequiredDocumentUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an required document.
    """
    required_document = crud.required_document.get(db=db, id=required_document_id)
    if not required_document:
        raise HTTPException(status_code=404, detail='RequiredDocument not found')
    required_document = crud.required_document.update(
        db=db, db_obj=required_document, obj_in=required_document_in
    )
    return required_document


@router.get('/{required_document_id}', response_model=schemas.RequiredDocument)
def read_required_document(
    *,
    relation: str = "[]",
    where: str = "[]",
    db: Session = Depends(deps.get_db),
    required_document_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get required document by ID.
    """
    relations = []
    if relation not in (None, "", [], "[]"):
        relations += ast.literal_eval(relation)

    wheres = []
    if where not in (None, "", []):
        wheres += ast.literal_eval(where)

    required_document = crud.required_document.get(
        db=db, id=required_document_id, relations=relations, where=wheres
    )
    if not required_document:
        raise HTTPException(status_code=404, detail='RequiredDocument not found')
    return required_document


@router.delete('/{required_document_id}', response_model=schemas.Msg)
def delete_required_document(
    *,
    db: Session = Depends(deps.get_db),
    required_document_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an required document.
    """
    required_document = crud.required_document.get(db=db, id=required_document_id)
    if not required_document:
        raise HTTPException(status_code=404, detail='RequiredDocument not found')
    crud.required_document.remove(db=db, id=required_document_id)
    return schemas.Msg(msg='RequiredDocument deleted successfully')

import ast
import shutil
from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.api import deps
from app import crud, models, schemas

router = APIRouter()


@router.get('/', response_model=schemas.ResponseDocument)
def read_documents(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    relations = []
    if relation:
        try:
            relations += ast.literal_eval(relation)
        except (ValueError, SyntaxError):
            pass

    wheres = []
    if where:
        try:
            wheres += ast.literal_eval(where)
        except (ValueError, SyntaxError):
            pass

    documents = crud.document.get_multi_where_array(
        db=db, relations=relations, skip=offset, limit=limit, where=wheres
    )
    count = crud.document.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseDocument(**{'count': count, 'data': jsonable_encoder(documents)})
    return response


@router.post('/', response_model=schemas.Document)
def create_document(
        *,
        db: Session = Depends(deps.get_db),
        document_in: schemas.DocumentCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    return crud.document.create(db=db, obj_in=document_in)


@router.put('/{document_id}', response_model=schemas.Document)
def update_document(
        *,
        db: Session = Depends(deps.get_db),
        document_id: int,
        document_in: schemas.DocumentUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    document = crud.document.get(db=db, id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail='Document not found')
    return crud.document.update(db=db, db_obj=document, obj_in=document_in)


@router.get('/{document_id}', response_model=schemas.Document)
def read_document(
        *,
        db: Session = Depends(deps.get_db),
        document_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    document = crud.document.get(db=db, id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail='Document not found')
    return document


@router.delete('/{document_id}', response_model=schemas.Msg)
def delete_document(
        *,
        db: Session = Depends(deps.get_db),
        document_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    document = crud.document.get(db=db, id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail='Document not found')
    crud.document.remove(db=db, id=document_id)
    return schemas.Msg(msg='Document deleted successfully')
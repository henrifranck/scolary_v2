from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseNote)
def read_notes(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve notes.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    notes = crud.note.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.note.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseNote(**{'count': count, 'data': jsonable_encoder(notes)})
    return response


@router.post('/', response_model=schemas.Note)
def create_note(
        *,
        db: Session = Depends(deps.get_db),
        note_in: schemas.NoteCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new note.
    """
    note = crud.note.create(db=db, obj_in=note_in)
    return note


@router.put('/{note_id}', response_model=schemas.Note)
def update_note(
        *,
        db: Session = Depends(deps.get_db),
        note_id: int,
        note_in: schemas.NoteUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an note.
    """
    note = crud.note.get(db=db, id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail='Note not found')
    note = crud.note.update(db=db, db_obj=note, obj_in=note_in)
    return note


@router.get('/{note_id}', response_model=schemas.Note)
def read_note(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        note_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get note by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    note = crud.note.get(db=db, id=note_id, relations=relations, where=wheres)
    if not note:
        raise HTTPException(status_code=404, detail='Note not found')
    return note


@router.delete('/{note_id}', response_model=schemas.Msg)
def delete_note(
        *,
        db: Session = Depends(deps.get_db),
        note_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an note.
    """
    note = crud.note.get(db=db, id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail='Note not found')
    note = crud.note.remove(db=db, id=note_id)
    return schemas.Msg(msg='Note deleted successfully')

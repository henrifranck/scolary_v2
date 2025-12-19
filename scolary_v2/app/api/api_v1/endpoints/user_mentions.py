from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseUserMention)
def read_user_mentions(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve user_mentions.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    user_mentions = crud.user_mention.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.user_mention.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseUserMention(**{'count': count, 'data': jsonable_encoder(user_mentions)})
    return response


@router.post('/', response_model=schemas.UserMention)
def create_user_mention(
        *,
        db: Session = Depends(deps.get_db),
        user_mention_in: schemas.UserMentionCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new user_mention.
    """
    user_mention = crud.user_mention.create(db=db, obj_in=user_mention_in)
    return user_mention


@router.put('/{user_mention_id}', response_model=schemas.UserMention)
def update_user_mention(
        *,
        db: Session = Depends(deps.get_db),
        user_mention_id: int,
        user_mention_in: schemas.UserMentionUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an user_mention.
    """
    user_mention = crud.user_mention.get(db=db, id=user_mention_id)
    if not user_mention:
        raise HTTPException(status_code=404, detail='UserMention not found')
    user_mention = crud.user_mention.update(db=db, db_obj=user_mention, obj_in=user_mention_in)
    return user_mention


@router.get('/{user_mention_id}', response_model=schemas.UserMention)
def read_user_mention(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        user_mention_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get user_mention by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    user_mention = crud.user_mention.get(db=db, id=user_mention_id, relations=relations, where=wheres)
    if not user_mention:
        raise HTTPException(status_code=404, detail='UserMention not found')
    return user_mention


@router.delete('/{user_mention_id}', response_model=schemas.Msg)
def delete_user_mention(
        *,
        db: Session = Depends(deps.get_db),
        user_mention_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an user_mention.
    """
    user_mention = crud.user_mention.get(db=db, id=user_mention_id)
    if not user_mention:
        raise HTTPException(status_code=404, detail='UserMention not found')
    user_mention = crud.user_mention.remove(db=db, id=user_mention_id)
    return schemas.Msg(msg='UserMention deleted successfully')

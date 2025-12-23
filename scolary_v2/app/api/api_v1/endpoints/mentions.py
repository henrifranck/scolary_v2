from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps


@router.get('/', response_model=schemas.ResponseMention)
def read_mentions(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        user_only: bool = False,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve mentions.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
        relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
        wheres += ast.literal_eval(where)
    if user_only and current_user.is_superuser == False:
        mention_ids = [
            assignment.id_mention
            for assignment in (current_user.user_mention or [])
            if assignment and assignment.id_mention
        ]
        wheres.append(
            {
                "key": "id",
                "operator": "in",
                "value": mention_ids
            }
        )

    mentions = crud.mention.get_multi_where_array(
        db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.mention.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseMention(**{'count': count, 'data': jsonable_encoder(mentions)})
    return response


@router.post('/', response_model=schemas.Mention)
def create_mention(
        *,
        db: Session = Depends(deps.get_db),
        mention_in: schemas.MentionCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new mention.
    """
    mention = crud.mention.create(db=db, obj_in=mention_in)
    return mention


@router.put('/{mention_id}', response_model=schemas.Mention)
def update_mention(
        *,
        db: Session = Depends(deps.get_db),
        mention_id: int,
        mention_in: schemas.MentionUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an mention.
    """
    mention = crud.mention.get(db=db, id=mention_id)
    if not mention:
        raise HTTPException(status_code=404, detail='Mention not found')
    mention = crud.mention.update(db=db, db_obj=mention, obj_in=mention_in)
    return mention


@router.get('/{mention_id}', response_model=schemas.Mention)
def read_mention(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        mention_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get mention by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
        relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
        wheres += ast.literal_eval(where)

    mention = crud.mention.get(db=db, id=mention_id, relations=relations, where=wheres)
    if not mention:
        raise HTTPException(status_code=404, detail='Mention not found')
    return mention


@router.delete('/{mention_id}', response_model=schemas.Msg)
def delete_mention(
        *,
        db: Session = Depends(deps.get_db),
        mention_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an mention.
    """
    mention = crud.mention.get(db=db, id=mention_id)
    if not mention:
        raise HTTPException(status_code=404, detail='Mention not found')
    mention = crud.mention.remove(db=db, id=mention_id)
    return schemas.Msg(msg='Mention deleted successfully')

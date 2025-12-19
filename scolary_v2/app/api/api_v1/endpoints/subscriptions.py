from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseSubscription)
def read_subscriptions(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve subscriptions.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    subscriptions = crud.subscription.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.subscription.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseSubscription(**{'count': count, 'data': jsonable_encoder(subscriptions)})
    return response


@router.post('/', response_model=schemas.Subscription)
def create_subscription(
        *,
        db: Session = Depends(deps.get_db),
        subscription_in: schemas.SubscriptionCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new subscription.
    """
    subscription = crud.subscription.create(db=db, obj_in=subscription_in)
    return subscription


@router.put('/{subscription_id}', response_model=schemas.Subscription)
def update_subscription(
        *,
        db: Session = Depends(deps.get_db),
        subscription_id: int,
        subscription_in: schemas.SubscriptionUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an subscription.
    """
    subscription = crud.subscription.get(db=db, id=subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail='Subscription not found')
    subscription = crud.subscription.update(db=db, db_obj=subscription, obj_in=subscription_in)
    return subscription


@router.get('/{subscription_id}', response_model=schemas.Subscription)
def read_subscription(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        subscription_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get subscription by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    subscription = crud.subscription.get(db=db, id=subscription_id, relations=relations, where=wheres)
    if not subscription:
        raise HTTPException(status_code=404, detail='Subscription not found')
    return subscription


@router.delete('/{subscription_id}', response_model=schemas.Msg)
def delete_subscription(
        *,
        db: Session = Depends(deps.get_db),
        subscription_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an subscription.
    """
    subscription = crud.subscription.get(db=db, id=subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail='Subscription not found')
    subscription = crud.subscription.remove(db=db, id=subscription_id)
    return schemas.Msg(msg='Subscription deleted successfully')

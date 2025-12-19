from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseSubscriptionFeature)
def read_subscription_features(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve subscription_features.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    subscription_features = crud.subscription_feature.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.subscription_feature.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseSubscriptionFeature(**{'count': count, 'data': jsonable_encoder(subscription_features)})
    return response


@router.post('/', response_model=schemas.SubscriptionFeature)
def create_subscription_feature(
        *,
        db: Session = Depends(deps.get_db),
        subscription_feature_in: schemas.SubscriptionFeatureCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new subscription_feature.
    """
    subscription_feature = crud.subscription_feature.create(db=db, obj_in=subscription_feature_in)
    return subscription_feature


@router.put('/{subscription_feature_id}', response_model=schemas.SubscriptionFeature)
def update_subscription_feature(
        *,
        db: Session = Depends(deps.get_db),
        subscription_feature_id: int,
        subscription_feature_in: schemas.SubscriptionFeatureUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an subscription_feature.
    """
    subscription_feature = crud.subscription_feature.get(db=db, id=subscription_feature_id)
    if not subscription_feature:
        raise HTTPException(status_code=404, detail='SubscriptionFeature not found')
    subscription_feature = crud.subscription_feature.update(db=db, db_obj=subscription_feature, obj_in=subscription_feature_in)
    return subscription_feature


@router.get('/{subscription_feature_id}', response_model=schemas.SubscriptionFeature)
def read_subscription_feature(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        subscription_feature_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get subscription_feature by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    subscription_feature = crud.subscription_feature.get(db=db, id=subscription_feature_id, relations=relations, where=wheres)
    if not subscription_feature:
        raise HTTPException(status_code=404, detail='SubscriptionFeature not found')
    return subscription_feature


@router.delete('/{subscription_feature_id}', response_model=schemas.Msg)
def delete_subscription_feature(
        *,
        db: Session = Depends(deps.get_db),
        subscription_feature_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an subscription_feature.
    """
    subscription_feature = crud.subscription_feature.get(db=db, id=subscription_feature_id)
    if not subscription_feature:
        raise HTTPException(status_code=404, detail='SubscriptionFeature not found')
    subscription_feature = crud.subscription_feature.remove(db=db, id=subscription_feature_id)
    return schemas.Msg(msg='SubscriptionFeature deleted successfully')

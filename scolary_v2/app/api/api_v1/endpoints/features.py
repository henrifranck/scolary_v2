from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseFeature)
def read_features(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve features.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    features = crud.feature.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.feature.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseFeature(**{'count': count, 'data': jsonable_encoder(features)})
    return response


@router.post('/', response_model=schemas.Feature)
def create_feature(
        *,
        db: Session = Depends(deps.get_db),
        feature_in: schemas.FeatureCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new feature.
    """
    feature = crud.feature.create(db=db, obj_in=feature_in)
    return feature


@router.put('/{feature_id}', response_model=schemas.Feature)
def update_feature(
        *,
        db: Session = Depends(deps.get_db),
        feature_id: int,
        feature_in: schemas.FeatureUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an feature.
    """
    feature = crud.feature.get(db=db, id=feature_id)
    if not feature:
        raise HTTPException(status_code=404, detail='Feature not found')
    feature = crud.feature.update(db=db, db_obj=feature, obj_in=feature_in)
    return feature


@router.get('/{feature_id}', response_model=schemas.Feature)
def read_feature(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        feature_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get feature by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    feature = crud.feature.get(db=db, id=feature_id, relations=relations, where=wheres)
    if not feature:
        raise HTTPException(status_code=404, detail='Feature not found')
    return feature


@router.delete('/{feature_id}', response_model=schemas.Msg)
def delete_feature(
        *,
        db: Session = Depends(deps.get_db),
        feature_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an feature.
    """
    feature = crud.feature.get(db=db, id=feature_id)
    if not feature:
        raise HTTPException(status_code=404, detail='Feature not found')
    feature = crud.feature.remove(db=db, id=feature_id)
    return schemas.Msg(msg='Feature deleted successfully')

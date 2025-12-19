from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseJourney)
def read_journeys(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve journeys.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    journeys = crud.journey.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.journey.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseJourney(**{'count': count, 'data': jsonable_encoder(journeys)})
    return response


@router.post('/', response_model=schemas.Journey)
def create_journey(
        *,
        db: Session = Depends(deps.get_db),
        journey_in: schemas.JourneyCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new journey.
    """
    journey = crud.journey.create(db=db, obj_in=journey_in)
    return jsonable_encoder(journey)


@router.put('/{journey_id}', response_model=schemas.Journey)
def update_journey(
        *,
        db: Session = Depends(deps.get_db),
        journey_id: int,
        journey_in: schemas.JourneyUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an journey.
    """
    journey = crud.journey.get(db=db, id=journey_id)
    if not journey:
        raise HTTPException(status_code=404, detail='Journey not found')
    journey = crud.journey.update(db=db, db_obj=journey, obj_in=journey_in)
    return jsonable_encoder(journey)


@router.get('/{journey_id}', response_model=schemas.Journey)
def read_journey(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        journey_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get journey by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    journey = crud.journey.get(db=db, id=journey_id, relations=relations, where=wheres)
    if not journey:
        raise HTTPException(status_code=404, detail='Journey not found')
    return jsonable_encoder(journey)


@router.delete('/{journey_id}', response_model=schemas.Msg)
def delete_journey(
        *,
        db: Session = Depends(deps.get_db),
        journey_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an journey.
    """
    journey = crud.journey.get(db=db, id=journey_id)
    if not journey:
        raise HTTPException(status_code=404, detail='Journey not found')
    journey = crud.journey.remove(db=db, id=journey_id)
    return schemas.Msg(msg='Journey deleted successfully')

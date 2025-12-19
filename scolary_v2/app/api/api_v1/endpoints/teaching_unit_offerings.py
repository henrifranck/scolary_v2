from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseTeachingUnitOffering)
def read_teaching_unit_offerings(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve teaching_unit_offerings.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    teaching_unit_offerings = crud.teaching_unit_offering.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.teaching_unit_offering.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseTeachingUnitOffering(**{'count': count, 'data': jsonable_encoder(teaching_unit_offerings)})
    return response


@router.post('/', response_model=schemas.TeachingUnitOffering)
def create_teaching_unit_offering(
        *,
        db: Session = Depends(deps.get_db),
        teaching_unit_offering_in: schemas.TeachingUnitOfferingCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new teaching_unit_offering.
    """
    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_in)
    return teaching_unit_offering


@router.put('/{teaching_unit_offering_id}', response_model=schemas.TeachingUnitOffering)
def update_teaching_unit_offering(
        *,
        db: Session = Depends(deps.get_db),
        teaching_unit_offering_id: int,
        teaching_unit_offering_in: schemas.TeachingUnitOfferingUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an teaching_unit_offering.
    """
    teaching_unit_offering = crud.teaching_unit_offering.get(db=db, id=teaching_unit_offering_id)
    if not teaching_unit_offering:
        raise HTTPException(status_code=404, detail='TeachingUnitOffering not found')
    teaching_unit_offering = crud.teaching_unit_offering.update(db=db, db_obj=teaching_unit_offering, obj_in=teaching_unit_offering_in)
    return teaching_unit_offering


@router.get('/{teaching_unit_offering_id}', response_model=schemas.TeachingUnitOffering)
def read_teaching_unit_offering(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        teaching_unit_offering_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get teaching_unit_offering by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    teaching_unit_offering = crud.teaching_unit_offering.get(db=db, id=teaching_unit_offering_id, relations=relations, where=wheres)
    if not teaching_unit_offering:
        raise HTTPException(status_code=404, detail='TeachingUnitOffering not found')
    return teaching_unit_offering


@router.delete('/{teaching_unit_offering_id}', response_model=schemas.Msg)
def delete_teaching_unit_offering(
        *,
        db: Session = Depends(deps.get_db),
        teaching_unit_offering_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an teaching_unit_offering.
    """
    teaching_unit_offering = crud.teaching_unit_offering.get(db=db, id=teaching_unit_offering_id)
    if not teaching_unit_offering:
        raise HTTPException(status_code=404, detail='TeachingUnitOffering not found')
    teaching_unit_offering = crud.teaching_unit_offering.remove(db=db, id=teaching_unit_offering_id)
    return schemas.Msg(msg='TeachingUnitOffering deleted successfully')

from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseConstituentElementOffering)
def read_constituent_element_offerings(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve constituent_element_offerings.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    constituent_element_offerings = crud.constituent_element_offering.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.constituent_element_offering.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseConstituentElementOffering(**{'count': count, 'data': jsonable_encoder(constituent_element_offerings)})
    return response


@router.post('/', response_model=schemas.ConstituentElementOffering)
def create_constituent_element_offering(
        *,
        db: Session = Depends(deps.get_db),
        constituent_element_offering_in: schemas.ConstituentElementOfferingCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new constituent_element_offering.
    """
    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_in)
    return constituent_element_offering


@router.put('/{constituent_element_offering_id}', response_model=schemas.ConstituentElementOffering)
def update_constituent_element_offering(
        *,
        db: Session = Depends(deps.get_db),
        constituent_element_offering_id: int,
        constituent_element_offering_in: schemas.ConstituentElementOfferingUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an constituent_element_offering.
    """
    constituent_element_offering = crud.constituent_element_offering.get(db=db, id=constituent_element_offering_id)
    if not constituent_element_offering:
        raise HTTPException(status_code=404, detail='ConstituentElementOffering not found')
    constituent_element_offering = crud.constituent_element_offering.update(db=db, db_obj=constituent_element_offering, obj_in=constituent_element_offering_in)
    return constituent_element_offering


@router.get('/{constituent_element_offering_id}', response_model=schemas.ConstituentElementOffering)
def read_constituent_element_offering(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        constituent_element_offering_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get constituent_element_offering by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    constituent_element_offering = crud.constituent_element_offering.get(db=db, id=constituent_element_offering_id, relations=relations, where=wheres)
    if not constituent_element_offering:
        raise HTTPException(status_code=404, detail='ConstituentElementOffering not found')
    return constituent_element_offering


@router.delete('/{constituent_element_offering_id}', response_model=schemas.Msg)
def delete_constituent_element_offering(
        *,
        db: Session = Depends(deps.get_db),
        constituent_element_offering_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an constituent_element_offering.
    """
    constituent_element_offering = crud.constituent_element_offering.get(db=db, id=constituent_element_offering_id)
    if not constituent_element_offering:
        raise HTTPException(status_code=404, detail='ConstituentElementOffering not found')
    constituent_element_offering = crud.constituent_element_offering.remove(db=db, id=constituent_element_offering_id)
    return schemas.Msg(msg='ConstituentElementOffering deleted successfully')

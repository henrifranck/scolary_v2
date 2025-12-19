from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseConstituentElement)
def read_constituent_elements(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve constituent_elements.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    constituent_elements = crud.constituent_element.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.constituent_element.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseConstituentElement(**{'count': count, 'data': jsonable_encoder(constituent_elements)})
    return response


@router.post('/', response_model=schemas.ConstituentElement)
def create_constituent_element(
        *,
        db: Session = Depends(deps.get_db),
        constituent_element_in: schemas.ConstituentElementCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new constituent_element.
    """
    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_in)
    return constituent_element


@router.put('/{constituent_element_id}', response_model=schemas.ConstituentElement)
def update_constituent_element(
        *,
        db: Session = Depends(deps.get_db),
        constituent_element_id: int,
        constituent_element_in: schemas.ConstituentElementUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an constituent_element.
    """
    constituent_element = crud.constituent_element.get(db=db, id=constituent_element_id)
    if not constituent_element:
        raise HTTPException(status_code=404, detail='ConstituentElement not found')
    constituent_element = crud.constituent_element.update(db=db, db_obj=constituent_element, obj_in=constituent_element_in)
    return constituent_element


@router.get('/{constituent_element_id}', response_model=schemas.ConstituentElement)
def read_constituent_element(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        constituent_element_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get constituent_element by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    constituent_element = crud.constituent_element.get(db=db, id=constituent_element_id, relations=relations, where=wheres)
    if not constituent_element:
        raise HTTPException(status_code=404, detail='ConstituentElement not found')
    return constituent_element


@router.delete('/{constituent_element_id}', response_model=schemas.Msg)
def delete_constituent_element(
        *,
        db: Session = Depends(deps.get_db),
        constituent_element_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an constituent_element.
    """
    constituent_element = crud.constituent_element.get(db=db, id=constituent_element_id)
    if not constituent_element:
        raise HTTPException(status_code=404, detail='ConstituentElement not found')
    constituent_element = crud.constituent_element.remove(db=db, id=constituent_element_id)
    return schemas.Msg(msg='ConstituentElement deleted successfully')

from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseConstituentElementOptionalGroup)
def read_constituent_element_optional_groups(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve constituent_element_optional_groups.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    constituent_element_optional_groups = crud.constituent_element_optional_group.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.constituent_element_optional_group.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseConstituentElementOptionalGroup(**{'count': count, 'data': jsonable_encoder(constituent_element_optional_groups)})
    return response


@router.post('/', response_model=schemas.ConstituentElementOptionalGroup)
def create_constituent_element_optional_group(
        *,
        db: Session = Depends(deps.get_db),
        constituent_element_optional_group_in: schemas.ConstituentElementOptionalGroupCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new constituent_element_optional_group.
    """
    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_in)
    return constituent_element_optional_group


@router.put('/{constituent_element_optional_group_id}', response_model=schemas.ConstituentElementOptionalGroup)
def update_constituent_element_optional_group(
        *,
        db: Session = Depends(deps.get_db),
        constituent_element_optional_group_id: int,
        constituent_element_optional_group_in: schemas.ConstituentElementOptionalGroupUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an constituent_element_optional_group.
    """
    constituent_element_optional_group = crud.constituent_element_optional_group.get(db=db, id=constituent_element_optional_group_id)
    if not constituent_element_optional_group:
        raise HTTPException(status_code=404, detail='ConstituentElementOptionalGroup not found')
    constituent_element_optional_group = crud.constituent_element_optional_group.update(db=db, db_obj=constituent_element_optional_group, obj_in=constituent_element_optional_group_in)
    return constituent_element_optional_group


@router.get('/{constituent_element_optional_group_id}', response_model=schemas.ConstituentElementOptionalGroup)
def read_constituent_element_optional_group(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        constituent_element_optional_group_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get constituent_element_optional_group by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    constituent_element_optional_group = crud.constituent_element_optional_group.get(db=db, id=constituent_element_optional_group_id, relations=relations, where=wheres)
    if not constituent_element_optional_group:
        raise HTTPException(status_code=404, detail='ConstituentElementOptionalGroup not found')
    return constituent_element_optional_group


@router.delete('/{constituent_element_optional_group_id}', response_model=schemas.Msg)
def delete_constituent_element_optional_group(
        *,
        db: Session = Depends(deps.get_db),
        constituent_element_optional_group_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an constituent_element_optional_group.
    """
    constituent_element_optional_group = crud.constituent_element_optional_group.get(db=db, id=constituent_element_optional_group_id)
    if not constituent_element_optional_group:
        raise HTTPException(status_code=404, detail='ConstituentElementOptionalGroup not found')
    constituent_element_optional_group = crud.constituent_element_optional_group.remove(db=db, id=constituent_element_optional_group_id)
    return schemas.Msg(msg='ConstituentElementOptionalGroup deleted successfully')

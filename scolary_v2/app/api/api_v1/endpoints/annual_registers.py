from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps


@router.get('/', response_model=schemas.ResponseAnnualRegister)
def read_annual_registers(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve annual_registers.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
        relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
        wheres += ast.literal_eval(where)

    annual_registers = crud.annual_register.get_multi_where_array(
        db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.annual_register.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseAnnualRegister(**{'count': count, 'data': jsonable_encoder(annual_registers)})
    return response


@router.post('/', response_model=schemas.AnnualRegister)
def create_annual_register(
        *,
        db: Session = Depends(deps.get_db),
        annual_register_in: schemas.AnnualRegisterCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new annual_register.
    """
    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_in)
    return annual_register


@router.put('/{annual_register_id}', response_model=schemas.AnnualRegister)
def update_annual_register(
        *,
        db: Session = Depends(deps.get_db),
        annual_register_id: int,
        annual_register_in: schemas.AnnualRegisterUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an annual_register.
    """
    annual_register = crud.annual_register.get(db=db, id=annual_register_id)
    if not annual_register:
        raise HTTPException(status_code=404, detail='AnnualRegister not found')
    annual_register = crud.annual_register.update(db=db, db_obj=annual_register, obj_in=annual_register_in)
    return annual_register


@router.get('/{annual_register_id}', response_model=schemas.AnnualRegister)
def read_annual_register(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        annual_register_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get annual_register by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
        relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
        wheres += ast.literal_eval(where)

    annual_register = crud.annual_register.get(db=db, id=annual_register_id, relations=relations, where=wheres)
    if not annual_register:
        raise HTTPException(status_code=404, detail='AnnualRegister not found')
    return annual_register


@router.delete('/{annual_register_id}', response_model=schemas.Msg)
def delete_annual_register(
        *,
        db: Session = Depends(deps.get_db),
        annual_register_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an annual_register.
    """
    annual_register = crud.annual_register.get(db=db, id=annual_register_id)
    if not annual_register:
        raise HTTPException(status_code=404, detail='AnnualRegister not found')
    annual_register = crud.annual_register.remove(db=db, id=annual_register_id)
    return schemas.Msg(msg='AnnualRegister deleted successfully')

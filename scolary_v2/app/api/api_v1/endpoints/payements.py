from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponsePayement)
def read_payements(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve payements.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    payements = crud.payement.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.payement.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponsePayement(**{'count': count, 'data': jsonable_encoder(payements)})
    return response


@router.post('/', response_model=schemas.Payement)
def create_payement(
        *,
        db: Session = Depends(deps.get_db),
        payement_in: schemas.PayementCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new payement.
    """
    payement = crud.payement.create(db=db, obj_in=payement_in)
    return payement


@router.put('/{payement_id}', response_model=schemas.Payement)
def update_payement(
        *,
        db: Session = Depends(deps.get_db),
        payement_id: int,
        payement_in: schemas.PayementUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an payement.
    """
    payement = crud.payement.get(db=db, id=payement_id)
    if not payement:
        raise HTTPException(status_code=404, detail='Payement not found')
    payement = crud.payement.update(db=db, db_obj=payement, obj_in=payement_in)
    return payement


@router.get('/{payement_id}', response_model=schemas.Payement)
def read_payement(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        payement_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get payement by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    payement = crud.payement.get(db=db, id=payement_id, relations=relations, where=wheres)
    if not payement:
        raise HTTPException(status_code=404, detail='Payement not found')
    return payement


@router.delete('/{payement_id}', response_model=schemas.Msg)
def delete_payement(
        *,
        db: Session = Depends(deps.get_db),
        payement_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an payement.
    """
    payement = crud.payement.get(db=db, id=payement_id)
    if not payement:
        raise HTTPException(status_code=404, detail='Payement not found')
    payement = crud.payement.remove(db=db, id=payement_id)
    return schemas.Msg(msg='Payement deleted successfully')

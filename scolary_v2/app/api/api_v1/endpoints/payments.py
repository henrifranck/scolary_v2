from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps

@router.get('/', response_model=schemas.ResponsePayment)
def read_payments(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve payments.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    payments = crud.payment.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.payment.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponsePayment(**{'count': count, 'data': jsonable_encoder(payments)})
    return response


@router.post('/', response_model=schemas.Payment)
def create_payment(
        *,
        db: Session = Depends(deps.get_db),
        payment_in: schemas.PaymentCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new payment.
    """
    payment = crud.payment.create(db=db, obj_in=payment_in)
    return payment


@router.put('/{payment_id}', response_model=schemas.Payment)
def update_payment(
        *,
        db: Session = Depends(deps.get_db),
        payment_id: int,
        payment_in: schemas.PaymentUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an payment.
    """
    payment = crud.payment.get(db=db, id=payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail='Payment not found')
    payment = crud.payment.update(db=db, db_obj=payment, obj_in=payment_in)
    return payment


@router.get('/{payment_id}', response_model=schemas.Payment)
def read_payment(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        payment_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get payment by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    payment = crud.payment.get(db=db, id=payment_id, relations=relations, where=wheres)
    if not payment:
        raise HTTPException(status_code=404, detail='Payment not found')
    return payment


@router.delete('/{payment_id}', response_model=schemas.Msg)
def delete_payment(
        *,
        db: Session = Depends(deps.get_db),
        payment_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a payment.
    """
    payment = crud.payment.get(db=db, id=payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail='Payment not found')
    payment = crud.payment.remove(db=db, id=payment_id)
    return schemas.Msg(msg='Payment deleted successfully')

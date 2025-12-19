from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseEnrollmentFee)
def read_enrollment_fees(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve enrollment_fees.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    enrollment_fees = crud.enrollment_fee.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.enrollment_fee.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseEnrollmentFee(**{'count': count, 'data': jsonable_encoder(enrollment_fees)})
    return response


@router.post('/', response_model=schemas.EnrollmentFee)
def create_enrollment_fee(
        *,
        db: Session = Depends(deps.get_db),
        enrollment_fee_in: schemas.EnrollmentFeeCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new enrollment_fee.
    """
    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_in)
    return enrollment_fee


@router.put('/{enrollment_fee_id}', response_model=schemas.EnrollmentFee)
def update_enrollment_fee(
        *,
        db: Session = Depends(deps.get_db),
        enrollment_fee_id: int,
        enrollment_fee_in: schemas.EnrollmentFeeUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an enrollment_fee.
    """
    enrollment_fee = crud.enrollment_fee.get(db=db, id=enrollment_fee_id)
    if not enrollment_fee:
        raise HTTPException(status_code=404, detail='EnrollmentFee not found')
    enrollment_fee = crud.enrollment_fee.update(db=db, db_obj=enrollment_fee, obj_in=enrollment_fee_in)
    return enrollment_fee


@router.get('/{enrollment_fee_id}', response_model=schemas.EnrollmentFee)
def read_enrollment_fee(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        enrollment_fee_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get enrollment_fee by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    enrollment_fee = crud.enrollment_fee.get(db=db, id=enrollment_fee_id, relations=relations, where=wheres)
    if not enrollment_fee:
        raise HTTPException(status_code=404, detail='EnrollmentFee not found')
    return enrollment_fee


@router.delete('/{enrollment_fee_id}', response_model=schemas.Msg)
def delete_enrollment_fee(
        *,
        db: Session = Depends(deps.get_db),
        enrollment_fee_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an enrollment_fee.
    """
    enrollment_fee = crud.enrollment_fee.get(db=db, id=enrollment_fee_id)
    if not enrollment_fee:
        raise HTTPException(status_code=404, detail='EnrollmentFee not found')
    enrollment_fee = crud.enrollment_fee.remove(db=db, id=enrollment_fee_id)
    return schemas.Msg(msg='EnrollmentFee deleted successfully')

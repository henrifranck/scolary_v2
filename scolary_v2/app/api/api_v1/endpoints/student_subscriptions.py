from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseStudentSubscription)
def read_student_subscriptions(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve student_subscriptions.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    student_subscriptions = crud.student_subscription.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.student_subscription.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseStudentSubscription(**{'count': count, 'data': jsonable_encoder(student_subscriptions)})
    return response


@router.post('/', response_model=schemas.StudentSubscription)
def create_student_subscription(
        *,
        db: Session = Depends(deps.get_db),
        student_subscription_in: schemas.StudentSubscriptionCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new student_subscription.
    """
    student_subscription = crud.student_subscription.create(db=db, obj_in=student_subscription_in)
    return student_subscription


@router.put('/{student_subscription_id}', response_model=schemas.StudentSubscription)
def update_student_subscription(
        *,
        db: Session = Depends(deps.get_db),
        student_subscription_id: int,
        student_subscription_in: schemas.StudentSubscriptionUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an student_subscription.
    """
    student_subscription = crud.student_subscription.get(db=db, id=student_subscription_id)
    if not student_subscription:
        raise HTTPException(status_code=404, detail='StudentSubscription not found')
    student_subscription = crud.student_subscription.update(db=db, db_obj=student_subscription, obj_in=student_subscription_in)
    return student_subscription


@router.get('/{student_subscription_id}', response_model=schemas.StudentSubscription)
def read_student_subscription(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        student_subscription_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get student_subscription by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    student_subscription = crud.student_subscription.get(db=db, id=student_subscription_id, relations=relations, where=wheres)
    if not student_subscription:
        raise HTTPException(status_code=404, detail='StudentSubscription not found')
    return student_subscription


@router.delete('/{student_subscription_id}', response_model=schemas.Msg)
def delete_student_subscription(
        *,
        db: Session = Depends(deps.get_db),
        student_subscription_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an student_subscription.
    """
    student_subscription = crud.student_subscription.get(db=db, id=student_subscription_id)
    if not student_subscription:
        raise HTTPException(status_code=404, detail='StudentSubscription not found')
    student_subscription = crud.student_subscription.remove(db=db, id=student_subscription_id)
    return schemas.Msg(msg='StudentSubscription deleted successfully')

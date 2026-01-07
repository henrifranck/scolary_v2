from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast

from app.core.notifications import schedule_notification

router = APIRouter()
from app.api import deps
@router.get('/', response_model=schemas.ResponseRegisterSemester)
def read_register_semesters(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve register_semesters.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    register_semesters = crud.register_semester.get_multi_where_array(
      db=db, relations=relations, skip=offset, limit=limit, where=wheres)
    count = crud.register_semester.get_count_where_array(db=db, where=wheres)
    response = schemas.ResponseRegisterSemester(**{'count': count, 'data': jsonable_encoder(register_semesters)})
    return response


@router.post('/', response_model=schemas.RegisterSemester)
def create_register_semester(
        *,
        db: Session = Depends(deps.get_db),
        register_semester_in: schemas.RegisterSemesterCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new register_semester.
    """
    duplicate = crud.register_semester.get_first_where_array(
      db=db,
      where=[
        {"key": "id_annual_register", "operator": "==", "value": register_semester_in.id_annual_register},
        {"key": "id_journey", "operator": "==", "value": register_semester_in.id_journey},
        {"key": "semester", "operator": "==", "value": register_semester_in.semester},
      ],
    )
    if duplicate:
        raise HTTPException(status_code=409, detail="RegisterSemester already exists for this annual register.")
    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_in)
    try:
        journey_name = None
        try:
            journey_rel = getattr(register_semester, "journey", None)
            if journey_rel and getattr(journey_rel, "name", None):
                print("nahazo ako", journey_rel)
                journey_name = journey_rel.name
            elif register_semester.id_journey:
                print("tsy nahazo ako", journey_rel)
                journey_obj = crud.journey.get(db=db, id=register_semester.id_journey)
                if journey_obj and getattr(journey_obj, "name", None):
                    journey_name = journey_obj.name
        except Exception:
            journey_name = None
        schedule_notification(
            {
                "type": "student_registered",
                "target_roles": ["Admin"],
                "template_vars": {
                    "card_number": register_semester.annual_register.num_carte,
                    "journey": journey_name,
                    "semester": register_semester.semester,
                }
            }
        )
    except Exception:
        pass
    return register_semester


@router.put('/{register_semester_id}', response_model=schemas.RegisterSemester)
def update_register_semester(
        *,
        db: Session = Depends(deps.get_db),
        register_semester_id: int,
        register_semester_in: schemas.RegisterSemesterUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an register_semester.
    """
    register_semester = crud.register_semester.get(db=db, id=register_semester_id)
    if not register_semester:
        raise HTTPException(status_code=404, detail='RegisterSemester not found')
    if register_semester_in.id_annual_register and register_semester_in.id_journey and register_semester_in.semester and register_semester_in.repeat_status:
        duplicate = crud.register_semester.get_multi_where_array(
          db=db,
          where=[
            {"key": "id_annual_register", "operator": "==", "value": register_semester_in.id_annual_register},
            {"key": "id_journey", "operator": "==", "value": register_semester_in.id_journey},
            {"key": "semester", "operator": "==", "value": register_semester_in.semester},
            {"key": "repeat_status", "operator": "==", "value": register_semester_in.repeat_status},
          ],
          limit=1
        )
        if duplicate and duplicate[0].id != register_semester_id:
            raise HTTPException(status_code=409, detail="RegisterSemester already exists for this annual register.")
    register_semester = crud.register_semester.update(db=db, db_obj=register_semester, obj_in=register_semester_in)
    return register_semester


@router.get('/{register_semester_id}', response_model=schemas.RegisterSemester)
def read_register_semester(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        register_semester_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get register_semester by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
       relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
       wheres += ast.literal_eval(where)

    register_semester = crud.register_semester.get(db=db, id=register_semester_id, relations=relations, where=wheres)
    if not register_semester:
        raise HTTPException(status_code=404, detail='RegisterSemester not found')
    return register_semester


@router.delete('/{register_semester_id}', response_model=schemas.Msg)
def delete_register_semester(
        *,
        db: Session = Depends(deps.get_db),
        register_semester_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an register_semester.
    """
    register_semester = crud.register_semester.get(db=db, id=register_semester_id)
    if not register_semester:
        raise HTTPException(status_code=404, detail='RegisterSemester not found')
    register_semester = crud.register_semester.remove(db=db, id=register_semester_id)
    return schemas.Msg(msg='RegisterSemester deleted successfully')

# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.journey import Journey
from app.models.journey_semester import JourneySemester
from app.schemas.journey import JourneyCreate, JourneyUpdate


class CRUDJourney(CRUDBase[Journey, JourneyCreate, JourneyUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[Journey]:
        return db.query(Journey).filter(getattr(Journey, field) == value).first()

    def _sync_journey_semester(
            self,
            db: Session,
            *,
            journey_id: int,
            semester_list: Optional[List[str]],
            commit: bool = True,
    ) -> None:
        target_ids = set(semester_list)
        if not target_ids and semester_list is None:
            return

        existing_semester = db.query(JourneySemester).filter(JourneySemester.id_journey == journey_id).all()
        existing_ids = {um.semester for um in existing_semester}

        for journey_ in existing_semester:
            if journey_.semester not in target_ids:
                db.delete(journey_)

        for semester in target_ids - existing_ids:
            db.add(JourneySemester(id_journey=journey_id, semester=semester))

        if commit:
            db.commit()
            
    def create(self, db: Session, *, obj_in: JourneyCreate) -> Journey:
        obj_data = jsonable_encoder(obj_in)
        semester_list = obj_data.pop('semester_list', None)
        db_obj = Journey(**obj_data)
        db.add(db_obj)
        db.flush()
        self._sync_journey_semester(db, journey_id=db_obj.id, semester_list=semester_list, commit=False)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Journey,
        obj_in: Union[JourneyUpdate, Dict[str, Any]],
        commit: bool = True,
    ) -> Journey:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in.copy()
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        semester_list = update_data.pop('semester_list', None)
        update_data["updated_at"] = func.now()

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.flush()
        self._sync_journey_semester(db, journey_id=db_obj.id, semester_list=semester_list, commit=False)
        if commit:
            db.commit()
            db.refresh(db_obj)
        return db_obj


journey = CRUDJourney(Journey)

# begin #
# ---write your code here--- #
# end #

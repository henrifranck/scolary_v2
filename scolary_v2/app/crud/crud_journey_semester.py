# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.journey_semester import JourneySemester
from app.schemas.journey_semester import JourneySemesterCreate, JourneySemesterUpdate


class CRUDJourneySemester(CRUDBase[JourneySemester, JourneySemesterCreate, JourneySemesterUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[JourneySemester]:
        return db.query(JourneySemester).filter(getattr(JourneySemester, field) == value).first()

journey_semester = CRUDJourneySemester(JourneySemester)


# begin #
# ---write your code here--- #
# end #

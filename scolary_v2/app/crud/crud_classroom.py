# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.classroom import Classroom
from app.schemas.classroom import ClassroomCreate, ClassroomUpdate


class CRUDClassroom(CRUDBase[Classroom, ClassroomCreate, ClassroomUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[Classroom]:
        return db.query(Classroom).filter(getattr(Classroom, field) == value).first()

classroom = CRUDClassroom(Classroom)


# begin #
# ---write your code here--- #
# end #

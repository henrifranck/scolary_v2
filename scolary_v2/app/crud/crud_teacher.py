# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate, TeacherUpdate


class CRUDTeacher(CRUDBase[Teacher, TeacherCreate, TeacherUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[Teacher]:
        return db.query(Teacher).filter(getattr(Teacher, field) == value).first()


teacher = CRUDTeacher(Teacher)

# begin #
# ---write your code here--- #
# end #

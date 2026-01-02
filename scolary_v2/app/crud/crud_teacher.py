# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate, TeacherUpdate


class CRUDTeacher(CRUDBase[Teacher, TeacherCreate, TeacherUpdate]):
    def get_by_user(self, db: Session, *, id_user: int) -> Optional[Teacher]:
        return db.query(Teacher).filter(Teacher.id_user == id_user).first()


teacher = CRUDTeacher(Teacher)

# begin #
# ---write your code here--- #
# end #

# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


class CRUDStudent(CRUDBase[Student, StudentCreate, StudentUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[Student]:
        return db.query(Student).filter(getattr(Student, field) == value).first()

student = CRUDStudent(Student)


# begin #
# ---write your code here--- #
# end #

# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.register_semester import RegisterSemester
from app.schemas.register_semester import RegisterSemesterCreate, RegisterSemesterUpdate


class CRUDRegisterSemester(CRUDBase[RegisterSemester, RegisterSemesterCreate, RegisterSemesterUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[RegisterSemester]:
        return db.query(RegisterSemester).filter(getattr(RegisterSemester, field) == value).first()

register_semester = CRUDRegisterSemester(RegisterSemester)


# begin #
# ---write your code here--- #
# end #

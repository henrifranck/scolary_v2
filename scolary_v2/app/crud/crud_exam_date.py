# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.exam_date import ExamDate
from app.schemas.exam_date import ExamDateCreate, ExamDateUpdate


class CRUDExamDate(CRUDBase[ExamDate, ExamDateCreate, ExamDateUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[ExamDate]:
        return db.query(ExamDate).filter(getattr(ExamDate, field) == value).first()

exam_date = CRUDExamDate(ExamDate)


# begin #
# ---write your code here--- #
# end #

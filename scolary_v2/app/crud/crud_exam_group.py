# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.exam_group import ExamGroup
from app.schemas.exam_group import ExamGroupCreate, ExamGroupUpdate


class CRUDExamGroup(CRUDBase[ExamGroup, ExamGroupCreate, ExamGroupUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[ExamGroup]:
        return db.query(ExamGroup).filter(getattr(ExamGroup, field) == value).first()

exam_group = CRUDExamGroup(ExamGroup)


# begin #
# ---write your code here--- #
# end #

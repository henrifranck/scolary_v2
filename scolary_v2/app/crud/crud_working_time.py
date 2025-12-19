# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.working_time import WorkingTime
from app.schemas.working_time import WorkingTimeCreate, WorkingTimeUpdate


class CRUDWorkingTime(CRUDBase[WorkingTime, WorkingTimeCreate, WorkingTimeUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[WorkingTime]:
        return db.query(WorkingTime).filter(getattr(WorkingTime, field) == value).first()

working_time = CRUDWorkingTime(WorkingTime)


# begin #
# ---write your code here--- #
# end #

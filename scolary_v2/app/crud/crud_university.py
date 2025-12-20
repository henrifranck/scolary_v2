# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.university import University
from app.schemas.university import UniversityCreate, UniversityUpdate


class CRUDUniversity(CRUDBase[University, UniversityCreate, UniversityUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[University]:
        return db.query(University).filter(getattr(University, field) == value).first()

    def get_info(self, db: Session) -> Optional[University]:
        return db.query(University).first()


university = CRUDUniversity(University)

# begin #
# ---write your code here--- #
# end #

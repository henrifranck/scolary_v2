# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.teaching_unit import TeachingUnit
from app.schemas.teaching_unit import TeachingUnitCreate, TeachingUnitUpdate


class CRUDTeachingUnit(CRUDBase[TeachingUnit, TeachingUnitCreate, TeachingUnitUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[TeachingUnit]:
        return db.query(TeachingUnit).filter(getattr(TeachingUnit, field) == value).first()

teaching_unit = CRUDTeachingUnit(TeachingUnit)


# begin #
# ---write your code here--- #
# end #

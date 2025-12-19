# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.result_teaching_unit import ResultTeachingUnit
from app.schemas.result_teaching_unit import ResultTeachingUnitCreate, ResultTeachingUnitUpdate


class CRUDResultTeachingUnit(CRUDBase[ResultTeachingUnit, ResultTeachingUnitCreate, ResultTeachingUnitUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[ResultTeachingUnit]:
        return db.query(ResultTeachingUnit).filter(getattr(ResultTeachingUnit, field) == value).first()

result_teaching_unit = CRUDResultTeachingUnit(ResultTeachingUnit)


# begin #
# ---write your code here--- #
# end #

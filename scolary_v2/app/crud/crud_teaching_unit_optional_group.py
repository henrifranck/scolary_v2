# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.teaching_unit_optional_group import TeachingUnitOptionalGroup
from app.schemas.teaching_unit_optional_group import TeachingUnitOptionalGroupCreate, TeachingUnitOptionalGroupUpdate


class CRUDTeachingUnitOptionalGroup(CRUDBase[TeachingUnitOptionalGroup, TeachingUnitOptionalGroupCreate, TeachingUnitOptionalGroupUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[TeachingUnitOptionalGroup]:
        return db.query(TeachingUnitOptionalGroup).filter(getattr(TeachingUnitOptionalGroup, field) == value).first()

teaching_unit_optional_group = CRUDTeachingUnitOptionalGroup(TeachingUnitOptionalGroup)


# begin #
# ---write your code here--- #
# end #

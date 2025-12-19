# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.teaching_unit_offering import TeachingUnitOffering
from app.schemas.teaching_unit_offering import TeachingUnitOfferingCreate, TeachingUnitOfferingUpdate


class CRUDTeachingUnitOffering(CRUDBase[TeachingUnitOffering, TeachingUnitOfferingCreate, TeachingUnitOfferingUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[TeachingUnitOffering]:
        return db.query(TeachingUnitOffering).filter(getattr(TeachingUnitOffering, field) == value).first()

teaching_unit_offering = CRUDTeachingUnitOffering(TeachingUnitOffering)


# begin #
# ---write your code here--- #
# end #

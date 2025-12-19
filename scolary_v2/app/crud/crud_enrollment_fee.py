# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.enrollment_fee import EnrollmentFee
from app.schemas.enrollment_fee import EnrollmentFeeCreate, EnrollmentFeeUpdate


class CRUDEnrollmentFee(CRUDBase[EnrollmentFee, EnrollmentFeeCreate, EnrollmentFeeUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[EnrollmentFee]:
        return db.query(EnrollmentFee).filter(getattr(EnrollmentFee, field) == value).first()

enrollment_fee = CRUDEnrollmentFee(EnrollmentFee)


# begin #
# ---write your code here--- #
# end #

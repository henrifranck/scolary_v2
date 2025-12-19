# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.student_subscription import StudentSubscription
from app.schemas.student_subscription import StudentSubscriptionCreate, StudentSubscriptionUpdate


class CRUDStudentSubscription(CRUDBase[StudentSubscription, StudentSubscriptionCreate, StudentSubscriptionUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[StudentSubscription]:
        return db.query(StudentSubscription).filter(getattr(StudentSubscription, field) == value).first()

student_subscription = CRUDStudentSubscription(StudentSubscription)


# begin #
# ---write your code here--- #
# end #

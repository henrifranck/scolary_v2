# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentUpdate


class CRUDPayment(CRUDBase[Payment, PaymentCreate, PaymentUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[Payment]:
        return db.query(Payment).filter(getattr(Payment, field) == value).first()

payment = CRUDPayment(Payment)


# begin #
# ---write your code here--- #
# end #

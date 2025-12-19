# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate


class CRUDSubscription(CRUDBase[Subscription, SubscriptionCreate, SubscriptionUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[Subscription]:
        return db.query(Subscription).filter(getattr(Subscription, field) == value).first()

subscription = CRUDSubscription(Subscription)


# begin #
# ---write your code here--- #
# end #

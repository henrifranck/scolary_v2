# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.subscription_feature import SubscriptionFeature
from app.schemas.subscription_feature import SubscriptionFeatureCreate, SubscriptionFeatureUpdate


class CRUDSubscriptionFeature(CRUDBase[SubscriptionFeature, SubscriptionFeatureCreate, SubscriptionFeatureUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[SubscriptionFeature]:
        return db.query(SubscriptionFeature).filter(getattr(SubscriptionFeature, field) == value).first()

subscription_feature = CRUDSubscriptionFeature(SubscriptionFeature)


# begin #
# ---write your code here--- #
# end #

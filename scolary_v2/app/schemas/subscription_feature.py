# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from .subscription import Subscription
from .feature import Feature


class SubscriptionFeatureBase(BaseModel):
    id_subscription: Optional[int] = None
    id_feature: Optional[int] = None


class SubscriptionFeatureCreate(SubscriptionFeatureBase):
    id_subscription: int


class SubscriptionFeatureUpdate(SubscriptionFeatureBase):
    pass


class SubscriptionFeatureInDBBase(SubscriptionFeatureBase):
    id: Optional[int]
    id_subscription: Optional[int]
    id_feature: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class SubscriptionFeature(SubscriptionFeatureInDBBase):
    pass


class SubscriptionFeatureWithRelation(SubscriptionFeatureInDBBase):
    subscription: Optional[Subscription] = None
    feature: Optional[Feature] = None


class SubscriptionFeatureInDB(SubscriptionFeatureInDBBase):
    pass


class ResponseSubscriptionFeature(BaseModel):
    count: int
    data: Optional[List[SubscriptionFeatureWithRelation]]


# begin #
# ---write your code here--- #
# end #

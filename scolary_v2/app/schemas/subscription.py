# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator


class SubscriptionBase(BaseModel):
    name: Optional[str] = None


class SubscriptionCreate(SubscriptionBase):
    name: str


class SubscriptionUpdate(SubscriptionBase):
    pass


class SubscriptionInDBBase(SubscriptionBase):
    id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class Subscription(SubscriptionInDBBase):
    pass


class SubscriptionWithRelation(SubscriptionInDBBase):
    pass


class SubscriptionInDB(SubscriptionInDBBase):
    pass


class ResponseSubscription(BaseModel):
    count: int
    data: Optional[List[SubscriptionWithRelation]]


# begin #
# ---write your code here--- #
# end #

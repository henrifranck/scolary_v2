# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from .subscription import Subscription
from .annual_register import AnnualRegister


class StudentSubscriptionBase(BaseModel):
    id_subscription: Optional[int] = None
    id_annual_register: Optional[int] = None


class StudentSubscriptionCreate(StudentSubscriptionBase):
    pass


class StudentSubscriptionUpdate(StudentSubscriptionBase):
    pass


class StudentSubscriptionInDBBase(StudentSubscriptionBase):
    id: Optional[int]
    id_subscription: Optional[int]
    id_annual_register: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class StudentSubscription(StudentSubscriptionInDBBase):
    pass


class StudentSubscriptionWithRelation(StudentSubscriptionInDBBase):
    subscription: Optional[Subscription] = None
    anual_register: Optional[AnnualRegister] = None


class StudentSubscriptionInDB(StudentSubscriptionInDBBase):
    pass


class ResponseStudentSubscription(BaseModel):
    count: int
    data: Optional[List[StudentSubscriptionWithRelation]]


# begin #
# ---write your code here--- #
# end #

# begin #
# ---write your code here--- #
# end #

from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class AvailableServiceBase(BaseModel):
    name: Optional[str] = None


class AvailableServiceCreate(AvailableServiceBase):
    name: str


class AvailableServiceUpdate(AvailableServiceBase):
    pass


class AvailableServiceInDBBase(AvailableServiceBase):
    id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class AvailableService(AvailableServiceInDBBase):
    pass


class AvailableServiceWithRelation(AvailableServiceInDBBase):
    pass


class AvailableServiceInDB(AvailableServiceInDBBase):
    pass


class ResponseAvailableService(BaseModel):
    count: int
    data: Optional[List[AvailableServiceWithRelation]]


# begin #
# ---write your code here--- #
# end #

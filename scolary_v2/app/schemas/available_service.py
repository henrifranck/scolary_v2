# begin #
# ---write your code here--- #
# end #

from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict


class AvailableServiceBase(BaseModel):
    name: Optional[str] = None
    route_ui: Optional[str] = None


class AvailableServiceCreate(AvailableServiceBase):
    name: str
    route_ui: str


class AvailableServiceUpdate(AvailableServiceBase):
    pass


class AvailableServiceInDBBase(AvailableServiceBase):
    id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class AvailableService(AvailableServiceInDBBase):
    pass


class AvailableServiceWithRelation(AvailableServiceInDBBase):
    available_service_required_document: Optional[Any] = None


class AvailableServiceInDB(AvailableServiceInDBBase):
    pass


class ResponseAvailableService(BaseModel):
    count: int
    data: Optional[List[AvailableServiceWithRelation]]


# begin #
# ---write your code here--- #
# end #

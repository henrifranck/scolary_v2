# begin #
# ---write your code here--- #
# end #

from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class AvailableModelBase(BaseModel):
    name: Optional[str] = None


class AvailableModelCreate(AvailableModelBase):
    name: str


class AvailableModelUpdate(AvailableModelBase):
    pass


class AvailableModelInDBBase(AvailableModelBase):
    id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class AvailableModel(AvailableModelInDBBase):
    pass


class AvailableModelWithRelation(AvailableModelInDBBase):
    pass


class AvailableModelInDB(AvailableModelInDBBase):
    pass


class ResponseAvailableModel(BaseModel):
    count: int
    data: Optional[List[AvailableModelWithRelation]]


# begin #
# ---write your code here--- #
# end #

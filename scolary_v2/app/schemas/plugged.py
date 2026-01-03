# begin #
# ---write your code here--- #
# end #

from typing import List, Optional

from pydantic import BaseModel


class PluggedBase(BaseModel):
    name: Optional[str] = None


class PluggedCreate(PluggedBase):
    name: Optional[str]


class PluggedUpdate(PluggedBase):
    pass


class PluggedInDBBase(PluggedBase):
    id: Optional[int]


class Plugged(PluggedInDBBase):
    pass


class PluggedWithRelation(PluggedInDBBase):
    pass


class PluggedInDB(PluggedInDBBase):
    pass


class ResponsePlugged(BaseModel):
    count: int
    data: Optional[List[PluggedWithRelation]]


# begin #
# ---write your code here--- #
# end #

# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator


class PermissionBase(BaseModel):
    name: Optional[str] = None
    method: Optional[str] = None
    model_name: Optional[str] = None


class PermissionCreate(PermissionBase):
    name: str
    method: str
    model_name: str


class PermissionUpdate(PermissionBase):
    pass


class PermissionInDBBase(PermissionBase):
    id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class Permission(PermissionInDBBase):
    pass


class PermissionWithRelation(PermissionInDBBase):
    pass


class PermissionInDB(PermissionInDBBase):
    pass


class ResponsePermission(BaseModel):
    count: int
    data: Optional[List[PermissionWithRelation]]


# begin #
# ---write your code here--- #
# end #

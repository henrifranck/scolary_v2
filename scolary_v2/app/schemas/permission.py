# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator

from .model_has_permission import ModelHasPermission

class PermissionBase(BaseModel):
    name: Optional[str] = None

    model_config = ConfigDict(protected_namespaces=())


class PermissionCreate(PermissionBase):
    name: str


class PermissionUpdate(PermissionBase):
    pass


class PermissionInDBBase(PermissionBase):
    id: Optional[int]

    model_config = ConfigDict(from_attributes=True, protected_namespaces=())


class Permission(PermissionInDBBase):
    model_has_permission: Optional[List[ModelHasPermission]] = None


class PermissionWithRelation(PermissionInDBBase):
    model_has_permission: Optional[List[ModelHasPermission]] = None


class PermissionInDB(PermissionInDBBase):
    pass


class ResponsePermission(BaseModel):
    count: int
    data: Optional[List[PermissionWithRelation]]


# begin #
# ---write your code here--- #
# end #

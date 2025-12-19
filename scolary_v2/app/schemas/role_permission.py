# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from .role import Role
from .permission import Permission


class RolePermissionBase(BaseModel):
    id_role: Optional[int] = None
    id_permission: Optional[int] = None


class RolePermissionCreate(RolePermissionBase):
    pass


class RolePermissionUpdate(RolePermissionBase):
    pass


class RolePermissionInDBBase(RolePermissionBase):
    id: Optional[int]
    id_role: Optional[int]
    id_permission: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class RolePermission(RolePermissionInDBBase):
    pass


class RolePermissionWithRelation(RolePermissionInDBBase):
    role: Optional[Role] = None
    permission: Optional[Permission] = None


class RolePermissionInDB(RolePermissionInDBBase):
    pass


class ResponseRolePermission(BaseModel):
    count: int
    data: Optional[List[RolePermissionWithRelation]]


# begin #
# ---write your code here--- #
# end #

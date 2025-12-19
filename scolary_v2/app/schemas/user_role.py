# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from .user import User
from .role import Role


class UserRoleBase(BaseModel):
    id_user: Optional[int] = None
    id_role: Optional[int] = None


class UserRoleCreate(UserRoleBase):
    id_user: int
    id_role: int


class UserRoleUpdate(UserRoleBase):
    pass


class UserRoleInDBBase(UserRoleBase):
    id: Optional[int]
    id_user: Optional[int]
    id_role: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class UserRole(UserRoleInDBBase):
    pass


class UserRoleWithRelation(UserRoleInDBBase):
    user: Optional[User] = None
    role: Optional[Role] = None


class UserRoleInDB(UserRoleInDBBase):
    pass


class ResponseUserRole(BaseModel):
    count: int
    data: Optional[List[UserRoleWithRelation]]


# begin #
# ---write your code here--- #
# end #

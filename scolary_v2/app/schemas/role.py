# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator


class RoleBase(BaseModel):
    name: Optional[str] = None
    permission_ids: List[int] = None
    use_for_card: Optional[bool] = False


class RoleCreate(RoleBase):
    name: str
    permission_ids: List[int] = None


class RoleUpdate(RoleBase):
    permission_ids: List[int] = None


class RoleInDBBase(RoleBase):
    id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class Role(RoleInDBBase):
    use_for_card: Optional[bool] = False


class RoleWithRelation(RoleInDBBase):
    role_permission: Optional[List[Any]] = None
    use_for_card: Optional[bool] = False


class RoleInDB(RoleInDBBase):
    use_for_card: Optional[bool] = False


class ResponseRole(BaseModel):
    count: int
    data: Optional[List[RoleWithRelation]]


# begin #
# ---write your code here--- #
# end #

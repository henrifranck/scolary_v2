# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator


class UserBase(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    is_superuser: Optional[bool] = None
    picture: Optional[str] = None
    is_active: Optional[bool] = None


class UserCreate(UserBase):
    email: str
    last_name: str
    password: str
    role_ids: Optional[List[int]] = None
    mention_ids: Optional[List[int]] = None


class UserUpdate(UserBase):
    role_ids: Optional[List[int]] = None
    mention_ids: Optional[List[int]] = None


class UserInDBBase(UserBase):
    id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class User(UserInDBBase):
    pass


class UserWithRelation(UserInDBBase):
    permissions: Optional[dict] = None
    user_role: Optional[Any] = None
    user_mention: Optional[Any] = None


class UserInDB(UserInDBBase):
    pass


class ResponseUser(BaseModel):
    count: int
    data: Optional[List[UserWithRelation]]


# begin #
# ---write your code here--- #
# end #

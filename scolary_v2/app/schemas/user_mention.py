# begin #
# ---write your code here--- #
# end #

from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from .mention import Mention
from .user import User


class UserMentionBase(BaseModel):
    id_user: Optional[int] = None
    id_mention: Optional[int] = None


class UserMentionCreate(UserMentionBase):
    id_user: int
    id_mention: int


class UserMentionUpdate(UserMentionBase):
    pass


class UserMentionInDBBase(UserMentionBase):
    id: Optional[int]
    id_user: Optional[int]
    id_mention: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class UserMention(UserMentionInDBBase):
    pass


class UserMentionWithRelation(UserMentionInDBBase):
    user: Optional[User] = None
    mention: Optional[Mention] = None


class UserMentionInDB(UserMentionInDBBase):
    pass


class ResponseUserMention(BaseModel):
    count: int
    data: Optional[List[UserMentionWithRelation]]


# begin #
# ---write your code here--- #
# end #

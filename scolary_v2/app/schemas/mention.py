# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator

from .plugged import Plugged


class MentionBase(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    abbreviation: Optional[str] = None
    id_plugged: Optional[int] = None
    background: Optional[str] = None


class MentionCreate(MentionBase):
    name: str
    slug: str
    abbreviation: str
    id_plugged: int


class MentionUpdate(MentionBase):
    pass


class MentionInDBBase(MentionBase):
    id: Optional[int]
    id_plugged: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class Mention(MentionInDBBase):
    pass


class MentionWithRelation(MentionInDBBase):
    plugged: Optional[Plugged] = None


class MentionInDB(MentionInDBBase):
    pass


class ResponseMention(BaseModel):
    count: int
    data: Optional[List[MentionWithRelation]]


# begin #
# ---write your code here--- #
# end #

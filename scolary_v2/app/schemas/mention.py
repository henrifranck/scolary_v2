# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator


class MentionBase(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    abbreviation: Optional[str] = None
    plugged: Optional[str] = None
    background: Optional[str] = None


class MentionCreate(MentionBase):
    name: str
    slug: str
    abbreviation: str
    plugged: str


class MentionUpdate(MentionBase):
    pass


class MentionInDBBase(MentionBase):
    id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class Mention(MentionInDBBase):
    pass


class MentionWithRelation(MentionInDBBase):
    pass


class MentionInDB(MentionInDBBase):
    pass


class ResponseMention(BaseModel):
    count: int
    data: Optional[List[MentionWithRelation]]


# begin #
# ---write your code here--- #
# end #

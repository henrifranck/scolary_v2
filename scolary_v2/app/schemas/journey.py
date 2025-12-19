# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from .mention import Mention


class JourneyBase(BaseModel):
    name: Optional[str] = None
    abbreviation: Optional[str] = None
    id_mention: Optional[int] = None
    semester_list: Optional[List[Any]] = None


class JourneyCreate(JourneyBase):
    name: str
    abbreviation: str
    semester_list: Optional[List[str]] = None


class JourneyUpdate(JourneyBase):
    semester_list: Optional[List[str]] = None


class JourneyInDBBase(JourneyBase):
    id: Optional[int]
    id_mention: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class Journey(JourneyInDBBase):
    pass


class JourneyWithRelation(JourneyInDBBase):
    mention: Optional[Mention] = None
    semester_list: Optional[Any] = None


class JourneyInDB(JourneyInDBBase):
    pass


class ResponseJourney(BaseModel):
    count: int
    data: Optional[List[JourneyWithRelation]]


# begin #
# ---write your code here--- #
# end #

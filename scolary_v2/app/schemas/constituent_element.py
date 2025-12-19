# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from .journey import Journey


class ConstituentElementBase(BaseModel):
    name: Optional[str] = None
    semester: Optional[str] = None
    id_journey: Optional[int] = None
    color: Optional[str] = None


class ConstituentElementCreate(ConstituentElementBase):
    name: str


class ConstituentElementUpdate(ConstituentElementBase):
    pass


class ConstituentElementInDBBase(ConstituentElementBase):
    id: Optional[int]
    id_journey: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class ConstituentElement(ConstituentElementInDBBase):
    pass


class ConstituentElementWithRelation(ConstituentElementInDBBase):
    journey: Optional[Journey] = None


class ConstituentElementInDB(ConstituentElementInDBBase):
    pass


class ResponseConstituentElement(BaseModel):
    count: int
    data: Optional[List[ConstituentElementWithRelation]]


# begin #
# ---write your code here--- #
# end #

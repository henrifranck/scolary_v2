# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from .journey import Journey


class TeachingUnitBase(BaseModel):
    name: Optional[str] = None
    semester: Optional[str] = None
    id_journey: Optional[int] = None


class TeachingUnitCreate(TeachingUnitBase):
    name: str
    semester: str


class TeachingUnitUpdate(TeachingUnitBase):
    pass


class TeachingUnitInDBBase(TeachingUnitBase):
    id: Optional[int]
    id_journey: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class TeachingUnit(TeachingUnitInDBBase):
    pass


class TeachingUnitWithRelation(TeachingUnitInDBBase):
    journey: Optional[Journey] = None


class TeachingUnitInDB(TeachingUnitInDBBase):
    pass


class ResponseTeachingUnit(BaseModel):
    count: int
    data: Optional[List[TeachingUnitWithRelation]]


# begin #
# ---write your code here--- #
# end #

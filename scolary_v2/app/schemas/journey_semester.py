# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from .journey import Journey


class JourneySemesterBase(BaseModel):
    id_journey: Optional[int] = None
    semester: Optional[str] = None


class JourneySemesterCreate(JourneySemesterBase):
    semester: str


class JourneySemesterUpdate(JourneySemesterBase):
    pass


class JourneySemesterInDBBase(JourneySemesterBase):
    id: Optional[int]
    id_journey: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class JourneySemester(JourneySemesterInDBBase):
    pass


class JourneySemesterWithRelation(JourneySemesterInDBBase):
    journey: Optional[Journey] = None


class JourneySemesterInDB(JourneySemesterInDBBase):
    pass


class ResponseJourneySemester(BaseModel):
    count: int
    data: Optional[List[JourneySemesterWithRelation]]


# begin #
# ---write your code here--- #
# end #

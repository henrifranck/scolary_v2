# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator


class AcademicYearBase(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None


class AcademicYearCreate(AcademicYearBase):
    name: str
    code: str


class AcademicYearUpdate(AcademicYearBase):
    pass


class AcademicYearInDBBase(AcademicYearBase):
    id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class AcademicYear(AcademicYearInDBBase):
    pass


class AcademicYearWithRelation(AcademicYearInDBBase):
    pass


class AcademicYearInDB(AcademicYearInDBBase):
    pass


class ResponseAcademicYear(BaseModel):
    count: int
    data: Optional[List[AcademicYearWithRelation]]


# begin #
# ---write your code here--- #
# end #

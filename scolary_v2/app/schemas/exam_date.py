# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from pydantic import field_validator
from .academic_year import AcademicYear


class ExamDateBase(BaseModel):
    id_academic_year: Optional[int] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    session: Optional[str] = None

    @field_validator('date_from', 'date_to', mode='before')
    def parse_date(cls, value):
        if value is None:
            return None
        if isinstance(value, str):
            try:
                return date.fromisoformat(value)
            except ValueError:
                raise ValueError("Invalid date format, expected YYYY-MM-DD")
        return value



class ExamDateCreate(ExamDateBase):
    id_academic_year: int
    date_from: date
    date_to: date


class ExamDateUpdate(ExamDateBase):
    pass


class ExamDateInDBBase(ExamDateBase):
    id: Optional[int]
    id_academic_year: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class ExamDate(ExamDateInDBBase):
    pass


class ExamDateWithRelation(ExamDateInDBBase):
    year: Optional[AcademicYear] = None


class ExamDateInDB(ExamDateInDBBase):
    pass


class ResponseExamDate(BaseModel):
    count: int
    data: Optional[List[ExamDateWithRelation]]


# begin #
# ---write your code here--- #
# end #

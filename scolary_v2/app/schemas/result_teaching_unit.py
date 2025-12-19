# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from pydantic import field_validator
from .register_semester import RegisterSemester


class ResultTeachingUnitBase(BaseModel):
    id_register_semester: Optional[int] = None
    note: Optional[float] = None
    is_valid: Optional[bool] = None
    date_validation: Optional[datetime] = None
    comment: Optional[str] = None

    @field_validator('date_validation', mode='before')
    def parse_datetime(cls, value):
        if value is None:
            return None
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError("Invalid datetime format")
        return value



class ResultTeachingUnitCreate(ResultTeachingUnitBase):
    id_register_semester: int
    note: float
    date_validation: datetime


class ResultTeachingUnitUpdate(ResultTeachingUnitBase):
    pass


class ResultTeachingUnitInDBBase(ResultTeachingUnitBase):
    id: Optional[int]
    id_register_semester: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class ResultTeachingUnit(ResultTeachingUnitInDBBase):
    pass


class ResultTeachingUnitWithRelation(ResultTeachingUnitInDBBase):
    student_year: Optional[RegisterSemester] = None


class ResultTeachingUnitInDB(ResultTeachingUnitInDBBase):
    pass


class ResponseResultTeachingUnit(BaseModel):
    count: int
    data: Optional[List[ResultTeachingUnitWithRelation]]


# begin #
# ---write your code here--- #
# end #

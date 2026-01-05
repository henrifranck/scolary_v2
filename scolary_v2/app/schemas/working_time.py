# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from pydantic import field_validator
from app.enum.working_time_type import WorkingTimeTypeEnum
from app.enum.session_type import SessionTypeEnum
from .classroom import Classroom
from .constituent_element_offering import ConstituentElementOffering
from .group import Group


class WorkingTimeBase(BaseModel):
    id_constituent_element_offering: Optional[int] = None
    working_time_type: Optional[WorkingTimeTypeEnum] = None
    day: Optional[str] = None
    start: Optional[Any] = None
    end: Optional[Any] = None
    id_group: Optional[int] = None
    id_classroom: Optional[int] = None
    date: Optional[datetime] = None
    session: Optional[SessionTypeEnum] = None

    @field_validator('date', mode='before')
    def parse_datetime(cls, value):
        if value is None:
            return None
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError("Invalid datetime format")
        return value

    @field_validator('start', 'end', mode='before')
    def parse_time(cls, value):
        if value is None:
            return None
        if isinstance(value, str):
            try:
                # Handle both "HH:MM:SS" and "HH:MM" formats
                parts = value.split(':')
                if len(parts) == 2:
                    return time.fromisoformat(value + ':00')
                return time.fromisoformat(value)
            except ValueError:
                raise ValueError("Invalid time format, expected HH:MM:SS")
        return value


class WorkingTimeCreate(WorkingTimeBase):
    working_time_type: WorkingTimeTypeEnum


class WorkingTimeUpdate(WorkingTimeBase):
    pass


class WorkingTimeInDBBase(WorkingTimeBase):
    id: Optional[int]
    id_constituent_element_offering: Optional[int] = None
    id_group: Optional[int] = None
    id_classroom: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class WorkingTime(WorkingTimeInDBBase):
    pass


class WorkingTimeWithRelation(WorkingTimeInDBBase):
    constituent_element_offering: Optional[ConstituentElementOffering] = None
    group: Optional[Group] = None
    classroom: Optional[Classroom] = None


class WorkingTimeInDB(WorkingTimeInDBBase):
    pass


class ResponseWorkingTime(BaseModel):
    count: int
    data: Optional[List[WorkingTimeWithRelation]]

# begin #
# ---write your code here--- #
# end #

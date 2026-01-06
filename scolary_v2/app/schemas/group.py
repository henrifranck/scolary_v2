# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator

from .academic_year import AcademicYear
from .journey import Journey


class GroupBase(BaseModel):
    id_journey: Optional[int] = None
    id_academic_year: Optional[int] = None
    semester: Optional[str] = None
    group_number: Optional[int] = None
    start_number: Optional[int] = None
    end_number: Optional[int] = None
    student_count: Optional[int] = None


class GroupCreate(GroupBase):
    id_journey: int
    semester: str
    group_number: int
    start_number: int
    end_number: int
    student_count: int


class GroupUpdate(GroupBase):
    pass


class GroupInDBBase(GroupBase):
    id: Optional[int]
    id_journey: Optional[int]
    id_academic_year: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class Group(GroupInDBBase):
    pass


class GroupWithRelation(GroupInDBBase):
    journey: Optional[Journey] = None
    academic_year: Optional[AcademicYear] = None


class GroupInDB(GroupInDBBase):
    pass


class ResponseGroup(BaseModel):
    count: int
    data: Optional[List[GroupWithRelation]]


# begin #
# ---write your code here--- #
# end #

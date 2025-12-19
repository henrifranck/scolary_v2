# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from app.enum.session_type import SessionTypeEnum
from .classroom import Classroom
from .journey import Journey
from .academic_year import AcademicYear


class ExamGroupBase(BaseModel):
    id_classroom: Optional[int] = None
    id_journey: Optional[int] = None
    semester: Optional[str] = None
    num_from: Optional[int] = None
    num_to: Optional[int] = None
    session: Optional[SessionTypeEnum] = None
    id_accademic_year: Optional[int] = None


class ExamGroupCreate(ExamGroupBase):
    id_classroom: int
    id_journey: int
    semester: str
    num_from: int
    num_to: int
    session: SessionTypeEnum


class ExamGroupUpdate(ExamGroupBase):
    pass


class ExamGroupInDBBase(ExamGroupBase):
    id: Optional[int]
    id_classroom: Optional[int]
    id_journey: Optional[int]
    id_accademic_year: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class ExamGroup(ExamGroupInDBBase):
    pass


class ExamGroupWithRelation(ExamGroupInDBBase):
    classroom: Optional[Classroom] = None
    journey: Optional[Journey] = None
    academic_year: Optional[AcademicYear] = None


class ExamGroupInDB(ExamGroupInDBBase):
    pass


class ResponseExamGroup(BaseModel):
    count: int
    data: Optional[List[ExamGroupWithRelation]]


# begin #
# ---write your code here--- #
# end #

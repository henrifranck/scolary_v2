# begin #
# ---write your code here--- #
# end #

from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from . import User
from ..enum.grade import GradeEnum


class TeacherBase(BaseModel):
    id_user: Optional[int] = None
    grade: Optional[GradeEnum] = GradeEnum.MR
    max_hours_per_day: Optional[float] = None
    max_days_per_week: Optional[float] = None


class TeacherCreate(TeacherBase):
    grade: GradeEnum


class TeacherUpdate(TeacherBase):
    pass


class TeacherInDBBase(TeacherBase):
    id: Optional[int]
    id_user: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class Teacher(TeacherInDBBase):
    pass


class TeacherWithRelation(TeacherInDBBase):
    user: Optional[User] = None


class TeacherInDB(TeacherInDBBase):
    pass


class ResponseTeacher(BaseModel):
    count: int
    data: Optional[List[TeacherWithRelation]]

# begin #
# ---write your code here--- #
# end #

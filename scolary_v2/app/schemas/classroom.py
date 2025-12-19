# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator


class ClassroomBase(BaseModel):
    name: Optional[str] = None
    capacity: Optional[int] = None


class ClassroomCreate(ClassroomBase):
    name: str
    capacity: int


class ClassroomUpdate(ClassroomBase):
    pass


class ClassroomInDBBase(ClassroomBase):
    id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class Classroom(ClassroomInDBBase):
    pass


class ClassroomWithRelation(ClassroomInDBBase):
    pass


class ClassroomInDB(ClassroomInDBBase):
    pass


class ResponseClassroom(BaseModel):
    count: int
    data: Optional[List[ClassroomWithRelation]]


# begin #
# ---write your code here--- #
# end #

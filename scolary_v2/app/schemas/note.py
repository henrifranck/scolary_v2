# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from app.enum.session_type import SessionTypeEnum
from .register_semester import RegisterSemester
from .constituent_element_offering import ConstituentElementOffering
from .user import User


class NoteBase(BaseModel):
    id_register_semester: Optional[int] = None
    id_constituent_element_offering: Optional[int] = None
    session: Optional[SessionTypeEnum] = None
    note: Optional[float] = None
    id_user: Optional[int] = None
    comment: Optional[str] = None


class NoteCreate(NoteBase):
    id_constituent_element_offering: int
    session: SessionTypeEnum


class NoteUpdate(NoteBase):
    pass


class NoteInDBBase(NoteBase):
    id: Optional[int]
    id_register_semester: Optional[int]
    id_constituent_element_offering: Optional[int]
    id_user: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class Note(NoteInDBBase):
    pass


class NoteWithRelation(NoteInDBBase):
    register_semester: Optional[RegisterSemester] = None
    constituent_element_offering: Optional[ConstituentElementOffering] = None
    user: Optional[User] = None


class NoteInDB(NoteInDBBase):
    pass


class ResponseNote(BaseModel):
    count: int
    data: Optional[List[NoteWithRelation]]


# begin #
# ---write your code here--- #
# end #

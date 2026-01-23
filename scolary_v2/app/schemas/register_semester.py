# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from app.enum.repeat_status import RepeatStatusEnum
from .annual_register import AnnualRegister
from .journey import Journey


class RegisterSemesterBase(BaseModel):
    id_annual_register: Optional[int] = None
    semester: Optional[str] = None
    repeat_status: Optional[RepeatStatusEnum] = None
    id_journey: Optional[int] = None
    imported_id: Optional[str] = None
    is_valid: Optional[bool] = None


class RegisterSemesterCreate(RegisterSemesterBase):
    semester: str
    repeat_status: RepeatStatusEnum
    template_vars: Any = None


class RegisterSemesterUpdate(RegisterSemesterBase):
    pass


class RegisterSemesterInDBBase(RegisterSemesterBase):
    id: Optional[int]
    id_annual_register: Optional[int]
    id_journey: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class RegisterSemester(RegisterSemesterInDBBase):
    pass


class RegisterSemesterWithRelation(RegisterSemesterInDBBase):
    annual_register: Optional[AnnualRegister] = None
    journey: Optional[Journey] = None


class RegisterSemesterInDB(RegisterSemesterInDBBase):
    pass


class ResponseRegisterSemester(BaseModel):
    count: int
    data: Optional[List[RegisterSemesterWithRelation]]


# begin #
# ---write your code here--- #
# end #

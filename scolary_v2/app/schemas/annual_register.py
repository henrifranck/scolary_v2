# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from .student import Student
from .academic_year import AcademicYear
from .enrollment_fee import EnrollmentFee


class AnnualRegisterBase(BaseModel):
    num_carte: Optional[str] = None
    id_academic_year: Optional[int] = None
    semester_count: Optional[int] = None
    id_enrollment_fee: Optional[int] = None


class AnnualRegisterCreate(AnnualRegisterBase):
    semester_count: int


class AnnualRegisterUpdate(AnnualRegisterBase):
    pass


class AnnualRegisterInDBBase(AnnualRegisterBase):
    id: Optional[int]
    num_carte: Optional[str]
    id_academic_year: Optional[int]
    id_enrollment_fee: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class AnnualRegister(AnnualRegisterInDBBase):
    pass


class AnnualRegisterWithRelation(AnnualRegisterInDBBase):
    student: Optional[Student] = None
    academic_year: Optional[AcademicYear] = None
    enrollment_fee: Optional[EnrollmentFee] = None
    register_semester: Optional[Any] = None
    payment: Optional[Any] = None


class AnnualRegisterInDB(AnnualRegisterInDBBase):
    pass


class ResponseAnnualRegister(BaseModel):
    count: int
    data: Optional[List[AnnualRegisterWithRelation]]


# begin #
# ---write your code here--- #
# end #

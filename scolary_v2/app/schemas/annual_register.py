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


class AnnualRegisterCreate(AnnualRegisterBase):
    semester_count: int


class AnnualRegisterUpdate(AnnualRegisterBase):
    pass


class AnnualRegisterInDBBase(AnnualRegisterBase):
    id: Optional[int]
    num_carte: Optional[str]
    id_academic_year: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class AnnualRegister(AnnualRegisterInDBBase):
    pass


class AnnualRegisterWithRelation(AnnualRegisterInDBBase):
    student: Optional[Student] = None
    academic_year: Optional[AcademicYear] = None
    register_semester: Optional[Any] = None
    document: Optional[Any] = None
    payment: Optional[Any] = None
    max_semester_number: Optional[int] = None
    level_from_semester: Optional[str] = None
    total_payment: Optional[float] = None
    enrollment_fee_amount: Optional[float] = None
    payment_status: Optional[str] = None


class AnnualRegisterInDB(AnnualRegisterInDBBase):
    pass


class ResponseAnnualRegister(BaseModel):
    count: int
    data: Optional[List[AnnualRegisterWithRelation]]


# begin #
# ---write your code here--- #
# end #

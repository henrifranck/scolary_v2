# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from app.enum.repeat_status import RepeatStatusEnum
from .mention import Mention
from .academic_year import AcademicYear


class EnrollmentFeeBase(BaseModel):
    level: Optional[RepeatStatusEnum] = None
    price: Optional[float] = None
    id_mention: Optional[int] = None
    id_academic_year: Optional[int] = None


class EnrollmentFeeCreate(EnrollmentFeeBase):
    level: RepeatStatusEnum
    price: float


class EnrollmentFeeUpdate(EnrollmentFeeBase):
    pass


class EnrollmentFeeInDBBase(EnrollmentFeeBase):
    id: Optional[int]
    id_mention: Optional[int]
    id_academic_year: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class EnrollmentFee(EnrollmentFeeInDBBase):
    pass


class EnrollmentFeeWithRelation(EnrollmentFeeInDBBase):
    mention: Optional[Mention] = None
    academinc_year: Optional[AcademicYear] = None


class EnrollmentFeeInDB(EnrollmentFeeInDBBase):
    pass


class ResponseEnrollmentFee(BaseModel):
    count: int
    data: Optional[List[EnrollmentFeeWithRelation]]


# begin #
# ---write your code here--- #
# end #

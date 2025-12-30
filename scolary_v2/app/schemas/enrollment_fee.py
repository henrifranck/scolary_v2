# begin #
# ---write your code here--- #
# end #

from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.enum.level import LevelEnum
from .academic_year import AcademicYear
from .mention import Mention
from ..enum.register_type import RegisterTypeEnum


class EnrollmentFeeBase(BaseModel):
    level: Optional[LevelEnum] = None
    price: Optional[float] = None
    id_mention: Optional[int] = None
    id_academic_year: Optional[int] = None
    register_type: Optional[str] = RegisterTypeEnum.REGISTRATION


class EnrollmentFeeCreate(EnrollmentFeeBase):
    level: LevelEnum
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

# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from pydantic import field_validator
from app.enum.sex import SexEnum
from app.enum.marital_status import MaritalStatusEnum
from app.enum.repeat_status import RepeatStatusEnum
from app.enum.level import LevelEnum
from app.enum.enrollment_status import EnrollmentStatusEnum
from .mention import Mention
from .academic_year import AcademicYear
from .nationality import Nationality
from .baccalaureate_serie import BaccalaureateSerie


class StudentBase(BaseModel):
    num_carte: Optional[str] = None
    email: Optional[str] = None
    num_select: Optional[str] = None
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    place_of_birth: Optional[str] = None
    address: Optional[str] = None
    sex: Optional[SexEnum] = None
    martial_status: Optional[MaritalStatusEnum] = None
    phone_number: Optional[str] = None
    num_of_cin: Optional[str] = None
    date_of_cin: Optional[date] = None
    place_of_cin: Optional[str] = None
    repeat_status: Optional[RepeatStatusEnum] = None
    picture: Optional[str] = None
    num_of_baccalaureate: Optional[str] = None
    center_of_baccalaureate: Optional[str] = None
    year_of_baccalaureate: Optional[date] = None
    job: Optional[str] = None
    father_name: Optional[str] = None
    father_job: Optional[str] = None
    mother_name: Optional[str] = None
    mother_job: Optional[str] = None
    parent_address: Optional[str] = None
    level: Optional[LevelEnum] = None
    mean: Optional[float] = None
    enrollment_status: Optional[EnrollmentStatusEnum] = None
    imported_id: Optional[str] = None
    id_mention: Optional[int] = None
    id_enter_year: Optional[int] = None
    id_nationality: Optional[int] = None
    id_baccalaureate_series: Optional[int] = None

    @field_validator('date_of_birth', 'date_of_cin', 'year_of_baccalaureate', mode='before')
    def parse_date(cls, value):
        if value is None:
            return None
        if isinstance(value, str):
            try:
                return date.fromisoformat(value)
            except ValueError:
                raise ValueError("Invalid date format, expected YYYY-MM-DD")
        return value


class StudentCreate(StudentBase):
    num_carte: str
    last_name: str
    date_of_birth: date
    place_of_birth: str
    address: str
    sex: SexEnum
    martial_status: MaritalStatusEnum
    picture: str
    num_of_baccalaureate: str
    center_of_baccalaureate: str
    job: str
    enrollment_status: EnrollmentStatusEnum


class StudentNewCreate(StudentBase):
    last_name: str
    date_of_birth: date
    place_of_birth: str
    address: str
    sex: SexEnum
    martial_status: MaritalStatusEnum
    num_of_baccalaureate: str
    center_of_baccalaureate: str
    job: str
    level: str
    id_mention: int
    enrollment_status: EnrollmentStatusEnum


class StudentUpdate(StudentBase):
    pass


class StudentInDBBase(StudentBase):
    id: Optional[int] = None
    id_mention: Optional[int] = None
    id_enter_year: Optional[int] = None
    id_nationality: Optional[int] = None
    id_baccalaureate_series: Optional[int] = None
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class Student(StudentInDBBase):
    pass


class StudentWithRelation(StudentInDBBase):
    mention: Optional[Mention] = None
    enter_year: Optional[AcademicYear] = None
    nationality: Optional[Nationality] = None
    baccalaureate_serie: Optional[BaccalaureateSerie] = None
    annual_register: Optional[Any] = None
    document_status: Optional[Any] = None
    generated_level: Optional[str] = None



class StudentInDB(StudentInDBBase):
    pass


class ResponseStudent(BaseModel):
    count: int
    data: Optional[List[StudentWithRelation]]


# begin #
# ---write your code here--- #
class StudentCard(BaseModel):
    num_carte: str
    last_name: str
    first_name: str
    date_birth: datetime
    place_birth: str
    num_cin: Optional[str] = None
    date_cin: Optional[datetime] = None
    place_cin: Optional[str] = None
    level: str
    journey: str


class StudentCardNumber(BaseModel):
    num_carte: Optional[List[str]]
# end #

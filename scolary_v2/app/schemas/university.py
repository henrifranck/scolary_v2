# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator


class UniversityBase(BaseModel):
    province: Optional[str] = None
    department_name: Optional[str] = None
    department_other_information: Optional[str] = None
    department_address: Optional[str] = None
    email: Optional[str] = None
    logo_university: Optional[str] = None
    logo_departement: Optional[str] = None
    phone_number: Optional[str] = None
    admin_signature: Optional[str] = None


class UniversityCreate(UniversityBase):
    province: str
    email: str


class UniversityUpdate(UniversityBase):
    pass


class UniversityInDBBase(UniversityBase):
    id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class University(UniversityInDBBase):
    pass


class UniversityWithRelation(UniversityInDBBase):
    pass


class UniversityInDB(UniversityInDBBase):
    pass


class ResponseUniversity(BaseModel):
    count: int
    data: Optional[List[UniversityWithRelation]]


# begin #
# ---write your code here--- #
# end #

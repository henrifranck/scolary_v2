# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator


class NationalityBase(BaseModel):
    name: Optional[str] = None


class NationalityCreate(NationalityBase):
    name: str


class NationalityUpdate(NationalityBase):
    pass


class NationalityInDBBase(NationalityBase):
    id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class Nationality(NationalityInDBBase):
    pass


class NationalityWithRelation(NationalityInDBBase):
    pass


class NationalityInDB(NationalityInDBBase):
    pass


class ResponseNationality(BaseModel):
    count: int
    data: Optional[List[NationalityWithRelation]]


# begin #
# ---write your code here--- #
# end #

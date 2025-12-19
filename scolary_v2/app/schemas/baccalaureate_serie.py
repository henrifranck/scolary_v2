# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator


class BaccalaureateSerieBase(BaseModel):
    name: Optional[str] = None
    value: Optional[str] = None


class BaccalaureateSerieCreate(BaccalaureateSerieBase):
    name: str
    value: str


class BaccalaureateSerieUpdate(BaccalaureateSerieBase):
    pass


class BaccalaureateSerieInDBBase(BaccalaureateSerieBase):
    id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class BaccalaureateSerie(BaccalaureateSerieInDBBase):
    pass


class BaccalaureateSerieWithRelation(BaccalaureateSerieInDBBase):
    pass


class BaccalaureateSerieInDB(BaccalaureateSerieInDBBase):
    pass


class ResponseBaccalaureateSerie(BaseModel):
    count: int
    data: Optional[List[BaccalaureateSerieWithRelation]]


# begin #
# ---write your code here--- #
# end #

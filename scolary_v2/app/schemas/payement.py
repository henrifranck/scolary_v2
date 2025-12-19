# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from pydantic import field_validator
from .annual_register import AnnualRegister


class PayementBase(BaseModel):
    id_annual_register: Optional[int] = None
    payed: Optional[float] = None
    num_receipt: Optional[str] = None
    date_receipt: Optional[date] = None

    @field_validator('date_receipt', mode='before')
    def parse_date(cls, value):
        if value is None:
            return None
        if isinstance(value, str):
            try:
                return date.fromisoformat(value)
            except ValueError:
                raise ValueError("Invalid date format, expected YYYY-MM-DD")
        return value



class PayementCreate(PayementBase):
    payed: float
    num_receipt: str
    date_receipt: date


class PayementUpdate(PayementBase):
    pass


class PayementInDBBase(PayementBase):
    id: Optional[int]
    id_annual_register: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class Payement(PayementInDBBase):
    pass


class PayementWithRelation(PayementInDBBase):
    annual_register: Optional[AnnualRegister] = None


class PayementInDB(PayementInDBBase):
    pass


class ResponsePayement(BaseModel):
    count: int
    data: Optional[List[PayementWithRelation]]


# begin #
# ---write your code here--- #
# end #

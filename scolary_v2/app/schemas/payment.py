# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from .annual_register import AnnualRegister


class PaymentBase(BaseModel):
    id_annual_register: Optional[int] = None
    payed: Optional[float] = None
    num_receipt: Optional[str] = None
    date_receipt: Optional[date] = None
    description: Optional[str] = None

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



class PaymentCreate(PaymentBase):
    payed: float
    num_receipt: str
    date_receipt: date


class PaymentUpdate(PaymentBase):
    pass


class PaymentInDBBase(PaymentBase):
    id: Optional[int]
    id_annual_register: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class Payment(PaymentInDBBase):
    pass


class PaymentWithRelation(PaymentInDBBase):
    annual_register: Optional[AnnualRegister] = None


class PaymentInDB(PaymentInDBBase):
    pass


class ResponsePayment(BaseModel):
    count: int
    data: Optional[List[PaymentWithRelation]]


# begin #
# ---write your code here--- #
# end #

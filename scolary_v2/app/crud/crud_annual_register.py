# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.annual_register import AnnualRegister
from app.schemas.annual_register import AnnualRegisterCreate, AnnualRegisterUpdate


class CRUDAnnualRegister(CRUDBase[AnnualRegister, AnnualRegisterCreate, AnnualRegisterUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[AnnualRegister]:
        return db.query(AnnualRegister).filter(getattr(AnnualRegister, field) == value).first()

annual_register = CRUDAnnualRegister(AnnualRegister)


# begin #
# ---write your code here--- #
# end #

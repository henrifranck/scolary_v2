# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.payement import Payement
from app.schemas.payement import PayementCreate, PayementUpdate


class CRUDPayement(CRUDBase[Payement, PayementCreate, PayementUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[Payement]:
        return db.query(Payement).filter(getattr(Payement, field) == value).first()

payement = CRUDPayement(Payement)


# begin #
# ---write your code here--- #
# end #

# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.nationality import Nationality
from app.schemas.nationality import NationalityCreate, NationalityUpdate


class CRUDNationality(CRUDBase[Nationality, NationalityCreate, NationalityUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[Nationality]:
        return db.query(Nationality).filter(getattr(Nationality, field) == value).first()

nationality = CRUDNationality(Nationality)


# begin #
# ---write your code here--- #
# end #

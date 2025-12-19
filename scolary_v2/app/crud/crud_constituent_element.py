# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.constituent_element import ConstituentElement
from app.schemas.constituent_element import ConstituentElementCreate, ConstituentElementUpdate


class CRUDConstituentElement(CRUDBase[ConstituentElement, ConstituentElementCreate, ConstituentElementUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[ConstituentElement]:
        return db.query(ConstituentElement).filter(getattr(ConstituentElement, field) == value).first()

constituent_element = CRUDConstituentElement(ConstituentElement)


# begin #
# ---write your code here--- #
# end #

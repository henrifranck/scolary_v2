# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.constituent_element_optional_group import ConstituentElementOptionalGroup
from app.schemas.constituent_element_optional_group import ConstituentElementOptionalGroupCreate, ConstituentElementOptionalGroupUpdate


class CRUDConstituentElementOptionalGroup(CRUDBase[ConstituentElementOptionalGroup, ConstituentElementOptionalGroupCreate, ConstituentElementOptionalGroupUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[ConstituentElementOptionalGroup]:
        return db.query(ConstituentElementOptionalGroup).filter(getattr(ConstituentElementOptionalGroup, field) == value).first()

constituent_element_optional_group = CRUDConstituentElementOptionalGroup(ConstituentElementOptionalGroup)


# begin #
# ---write your code here--- #
# end #

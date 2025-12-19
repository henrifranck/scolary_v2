# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.constituent_element_offering import ConstituentElementOffering
from app.schemas.constituent_element_offering import ConstituentElementOfferingCreate, ConstituentElementOfferingUpdate


class CRUDConstituentElementOffering(CRUDBase[ConstituentElementOffering, ConstituentElementOfferingCreate, ConstituentElementOfferingUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[ConstituentElementOffering]:
        return db.query(ConstituentElementOffering).filter(getattr(ConstituentElementOffering, field) == value).first()

constituent_element_offering = CRUDConstituentElementOffering(ConstituentElementOffering)


# begin #
# ---write your code here--- #
# end #

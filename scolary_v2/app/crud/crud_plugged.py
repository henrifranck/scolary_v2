# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.plugged import Plugged
from app.schemas.plugged import PluggedCreate, PluggedUpdate


class CRUDPlugged(CRUDBase[Plugged, PluggedCreate, PluggedUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[Plugged]:
        return db.query(Plugged).filter(getattr(Plugged, field) == value).first()


plugged = CRUDPlugged(Plugged)

# begin #
# ---write your code here--- #
# end #

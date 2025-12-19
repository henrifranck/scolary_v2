# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.baccalaureate_serie import BaccalaureateSerie
from app.schemas.baccalaureate_serie import BaccalaureateSerieCreate, BaccalaureateSerieUpdate


class CRUDBaccalaureateSerie(CRUDBase[BaccalaureateSerie, BaccalaureateSerieCreate, BaccalaureateSerieUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[BaccalaureateSerie]:
        return db.query(BaccalaureateSerie).filter(getattr(BaccalaureateSerie, field) == value).first()

baccalaureate_serie = CRUDBaccalaureateSerie(BaccalaureateSerie)


# begin #
# ---write your code here--- #
# end #

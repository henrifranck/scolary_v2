# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.feature import Feature
from app.schemas.feature import FeatureCreate, FeatureUpdate


class CRUDFeature(CRUDBase[Feature, FeatureCreate, FeatureUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[Feature]:
        return db.query(Feature).filter(getattr(Feature, field) == value).first()

feature = CRUDFeature(Feature)


# begin #
# ---write your code here--- #
# end #

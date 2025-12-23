# begin #
# ---write your code here--- #
# end #

from typing import Optional, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.available_model import AvailableModel
from app.schemas.available_model import AvailableModelCreate, AvailableModelUpdate


class CRUDAvailableModel(CRUDBase[AvailableModel, AvailableModelCreate, AvailableModelUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[AvailableModel]:
        return db.query(AvailableModel).filter(getattr(AvailableModel, field) == value).first()


available_model = CRUDAvailableModel(AvailableModel)


# begin #
# ---write your code here--- #
# end #

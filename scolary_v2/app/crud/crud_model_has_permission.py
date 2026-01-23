# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.model_has_permission import ModelHasPermission
from app.schemas.model_has_permission import ModelHasPermissionCreate, ModelHasPermissionUpdate


class CRUDPermission(CRUDBase[ModelHasPermission, ModelHasPermissionCreate, ModelHasPermissionUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[ModelHasPermission]:
        return db.query(ModelHasPermission).filter(getattr(ModelHasPermission, field) == value).first()


model_has_permission = CRUDPermission(ModelHasPermission)

# begin #
# ---write your code here--- #
# end #

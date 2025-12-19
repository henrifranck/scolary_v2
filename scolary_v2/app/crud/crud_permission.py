# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate


class CRUDPermission(CRUDBase[Permission, PermissionCreate, PermissionUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[Permission]:
        return db.query(Permission).filter(getattr(Permission, field) == value).first()

permission = CRUDPermission(Permission)


# begin #
# ---write your code here--- #
# end #

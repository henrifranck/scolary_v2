# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.role_permission import RolePermission
from app.schemas.role_permission import RolePermissionCreate, RolePermissionUpdate


class CRUDRolePermission(CRUDBase[RolePermission, RolePermissionCreate, RolePermissionUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[RolePermission]:
        return db.query(RolePermission).filter(getattr(RolePermission, field) == value).first()

role_permission = CRUDRolePermission(RolePermission)


# begin #
# ---write your code here--- #
# end #

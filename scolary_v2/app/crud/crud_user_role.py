# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user_role import UserRole
from app.schemas.user_role import UserRoleCreate, UserRoleUpdate


class CRUDUserRole(CRUDBase[UserRole, UserRoleCreate, UserRoleUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[UserRole]:
        return db.query(UserRole).filter(getattr(UserRole, field) == value).first()

user_role = CRUDUserRole(UserRole)


# begin #
# ---write your code here--- #
# end #

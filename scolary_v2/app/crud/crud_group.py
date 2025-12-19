# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.group import Group
from app.schemas.group import GroupCreate, GroupUpdate


class CRUDGroup(CRUDBase[Group, GroupCreate, GroupUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[Group]:
        return db.query(Group).filter(getattr(Group, field) == value).first()

group = CRUDGroup(Group)


# begin #
# ---write your code here--- #
# end #

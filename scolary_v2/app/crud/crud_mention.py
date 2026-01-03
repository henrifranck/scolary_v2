# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.mention import Mention
from app.schemas.mention import MentionCreate, MentionUpdate


class CRUDMention(CRUDBase[Mention, MentionCreate, MentionUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[Mention]:
        return db.query(Mention).filter(getattr(Mention, field) == value).first()


mention = CRUDMention(Mention)

# begin #
# ---write your code here--- #
# end #

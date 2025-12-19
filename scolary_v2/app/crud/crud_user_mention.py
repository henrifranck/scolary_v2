# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user_mention import UserMention
from app.schemas.user_mention import UserMentionCreate, UserMentionUpdate


class CRUDUserMention(CRUDBase[UserMention, UserMentionCreate, UserMentionUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[UserMention]:
        return db.query(UserMention).filter(getattr(UserMention, field) == value).first()

user_mention = CRUDUserMention(UserMention)


# begin #
# ---write your code here--- #
# end #

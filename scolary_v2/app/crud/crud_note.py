# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate


class CRUDNote(CRUDBase[Note, NoteCreate, NoteUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[Note]:
        return db.query(Note).filter(getattr(Note, field) == value).first()

note = CRUDNote(Note)


# begin #
# ---write your code here--- #
# end #

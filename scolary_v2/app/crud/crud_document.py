from typing import Optional, Any

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentUpdate


class CRUDDocument(CRUDBase[Document, DocumentCreate, DocumentUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[Document]:
        return db.query(Document).filter(getattr(Document, field) == value).first()


document = CRUDDocument(Document)

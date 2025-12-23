# begin #
# ---write your code here--- #
# end #

from typing import Optional, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.required_document import RequiredDocument
from app.schemas.required_document import RequiredDocumentCreate, RequiredDocumentUpdate


class CRUDRequiredDocument(CRUDBase[RequiredDocument, RequiredDocumentCreate, RequiredDocumentUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[RequiredDocument]:
        return db.query(RequiredDocument).filter(getattr(RequiredDocument, field) == value).first()


required_document = CRUDRequiredDocument(RequiredDocument)


# begin #
# ---write your code here--- #
# end #

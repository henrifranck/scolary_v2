# begin #
# ---write your code here--- #
# end #

from typing import Optional, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.service_required_document import AvailableServiceRequiredDocument
from app.schemas.available_service_required_document import (
    AvailableServiceRequiredDocumentCreate,
    AvailableServiceRequiredDocumentUpdate,
)


class CRUDAvailableServiceRequiredDocument(
    CRUDBase[
        AvailableServiceRequiredDocument,
        AvailableServiceRequiredDocumentCreate,
        AvailableServiceRequiredDocumentUpdate,
    ]
):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[AvailableServiceRequiredDocument]:
        return db.query(AvailableServiceRequiredDocument).filter(
            getattr(AvailableServiceRequiredDocument, field) == value
        ).first()


available_service_required_document = CRUDAvailableServiceRequiredDocument(AvailableServiceRequiredDocument)


# begin #
# ---write your code here--- #
# end #

# begin #
# ---write your code here--- #
# end #

from typing import Optional, Any
from sqlalchemy.orm import Session, selectinload

from app.crud.base import CRUDBase
from app.models.available_service import AvailableService
from app.schemas.available_service import AvailableServiceCreate, AvailableServiceUpdate


class CRUDAvailableService(CRUDBase[AvailableService, AvailableServiceCreate, AvailableServiceUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[AvailableService]:
        return (
            db.query(AvailableService)
            .filter(getattr(AvailableService, field) == value)
            .options(
                selectinload(AvailableService.available_service_required_document)
            )
            .first()
        )


available_service = CRUDAvailableService(AvailableService)


# begin #
# ---write your code here--- #
# end #

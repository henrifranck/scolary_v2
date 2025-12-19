from typing import Optional, Any

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.card import Card
from app.schemas.card import CardCreate, CardUpdate


class CRUDCard(CRUDBase[Card, CardCreate, CardUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[Card]:
        return db.query(Card).filter(getattr(Card, field) == value).first()


card = CRUDCard(Card)

from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.card_asset import CardAsset
from app.schemas.card_asset import CardAssetCreate


class CRUDCardAsset(CRUDBase[CardAsset, CardAssetCreate, CardAssetCreate]):
  def create_with_user(
    self, db: Session, *, obj_in: CardAssetCreate, uploaded_by_id: Optional[int]
  ) -> CardAsset:
    db_obj = CardAsset(
      filename=obj_in.filename,
      path=obj_in.path,
      uploaded_by_id=uploaded_by_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


card_asset = CRUDCardAsset(CardAsset)

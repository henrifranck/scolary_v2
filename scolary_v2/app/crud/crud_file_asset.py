from typing import Optional, Any

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.file_asset import FileAsset
from app.schemas.file_asset import FileAssetCreate, FileAssetUpdate


class CRUDFileAsset(CRUDBase[FileAsset, FileAssetCreate, FileAssetUpdate]):
  def get_by_path(self, db: Session, *, path: str) -> Optional[FileAsset]:
    return db.query(FileAsset).filter(FileAsset.path == path).first()

  def create_with_uploader(
    self,
    db: Session,
    *,
    obj_in: FileAssetCreate,
    uploaded_by_id: Optional[int]
  ) -> FileAsset:
    db_obj = FileAsset(
      name=obj_in.name,
      path=obj_in.path,
      type=obj_in.type,
      size_bytes=obj_in.size_bytes,
      mime_type=obj_in.mime_type,
      uploaded_by_id=uploaded_by_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


file_asset = CRUDFileAsset(FileAsset)

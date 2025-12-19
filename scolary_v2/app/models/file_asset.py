from pathlib import Path

from sqlalchemy import BigInteger, Column, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.enum.file_type import FileTypeEnum


class FileAsset(Base):
  __tablename__ = "file_asset"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(255), nullable=False)
  path = Column(String(512), nullable=False, unique=True)
  type = Column(Enum(FileTypeEnum), nullable=False, default=FileTypeEnum.OTHER)
  size_bytes = Column(BigInteger, nullable=True)
  mime_type = Column(String(255), nullable=True)
  uploaded_by_id = Column(Integer, ForeignKey("user.id"), nullable=True)

  created_at = Column(DateTime, nullable=False, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
  deleted_at = Column(DateTime, nullable=True)

  uploaded_by = relationship("User", foreign_keys=[uploaded_by_id])

  @property
  def url(self) -> str:
    normalized = str(self.path or "").lstrip("/")
    if normalized.startswith("files/"):
      return f"/{normalized}"
    return f"/files/{normalized}"

  @property
  def absolute_path(self) -> Path:
    root = Path("files")
    return root / self.path

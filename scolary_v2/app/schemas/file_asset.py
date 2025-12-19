from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.enum.file_type import FileTypeEnum


class FileAssetBase(BaseModel):
  name: Optional[str] = None
  type: Optional[FileTypeEnum] = None
  size_bytes: Optional[int] = None
  mime_type: Optional[str] = None
  path: Optional[str] = None


class FileAssetCreate(FileAssetBase):
  name: str
  path: str
  type: FileTypeEnum


class FileAssetUpdate(BaseModel):
  name: Optional[str] = None
  type: Optional[FileTypeEnum] = None


class FileAsset(FileAssetBase):
  id: Optional[int]
  url: Optional[str] = None
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None

  model_config = ConfigDict(from_attributes=True)


class ResponseFileAsset(BaseModel):
  count: int
  data: Optional[List[FileAsset]]

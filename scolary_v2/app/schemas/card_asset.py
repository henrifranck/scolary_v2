from typing import Optional

from pydantic import BaseModel, ConfigDict


class CardAssetBase(BaseModel):
  filename: Optional[str] = None
  path: Optional[str] = None


class CardAssetCreate(CardAssetBase):
  filename: str
  path: str


class CardAsset(CardAssetBase):
  id: Optional[int]
  uploaded_by_id: Optional[int] = None

  model_config = ConfigDict(from_attributes=True)

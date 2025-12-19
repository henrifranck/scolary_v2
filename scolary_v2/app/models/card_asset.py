from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class CardAsset(Base):
  __tablename__ = "card_asset"

  id = Column(Integer, primary_key=True, index=True)
  filename = Column(String(255), nullable=False)
  path = Column(String(512), nullable=False, unique=True)
  uploaded_by_id = Column(Integer, ForeignKey("user.id"), nullable=True)
  created_at = Column(DateTime, nullable=False, server_default=func.now())

  uploaded_by = relationship("User", foreign_keys=[uploaded_by_id])

from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.enum.card_type import CardTypeEnum


class AvailableService(Base):
    __tablename__ = 'available_service'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False)
    route_ui = Column(String(255), nullable=False)

    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    available_service_required_document = relationship('AvailableServiceRequiredDocument')

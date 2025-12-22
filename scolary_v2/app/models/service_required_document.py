from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.enum.card_type import CardTypeEnum


class AvailableServiceRequiredDocument(Base):
    __tablename__ = 'available_service_required_document'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    id_available_service = Column(Integer, ForeignKey('available_service.id'))
    id_required_document = Column(Integer, ForeignKey('required_document.id'))

    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relation
    available_service = relationship('AvailableService', foreign_keys=[id_available_service])
    required_document = relationship('RequiredDocument', foreign_keys=[id_required_document])

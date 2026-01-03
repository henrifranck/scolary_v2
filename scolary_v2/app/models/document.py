from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, column_property
from sqlalchemy import select

from app.enum.card_type import CardTypeEnum
from app.models.required_document import RequiredDocument


class Document(Base):
    __tablename__ = 'document'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    url = Column(String(255), nullable=False)
    id_annual_register = Column(Integer, ForeignKey('annual_register.id'), nullable=True)
    id_required_document = Column(Integer, ForeignKey('required_document.id'), nullable=True)

    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    annual_register = relationship('AnnualRegister', foreign_keys=[id_annual_register], back_populates='document')
    required_document = relationship('RequiredDocument', foreign_keys=[id_required_document])

    required_document_name = column_property(
        select(RequiredDocument.name)
        .where(RequiredDocument.id == id_required_document)
        .correlate_except(RequiredDocument)
        .scalar_subquery()
    )

from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.enum.card_type import CardTypeEnum


class Card(Base):
    __tablename__ = 'card'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    card_type = Column(Enum(CardTypeEnum), nullable=False)
    html_template = Column(Text, nullable=False)
    css_styles = Column(Text, nullable=True)
    id_mention = Column(Integer, ForeignKey('mention.id'), nullable=True)
    id_journey = Column(Integer, ForeignKey('journey.id'), nullable=True)

    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    mention = relationship('Mention', foreign_keys=[id_mention])
    journey = relationship('Journey', foreign_keys=[id_journey])

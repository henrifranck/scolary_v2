# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import String, Integer


class Journey(Base):
    __tablename__ = 'journey'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    abbreviation = Column(String(255), nullable=False)
    id_mention = Column(Integer, ForeignKey('mention.id'))

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations
    mention = relationship('Mention', foreign_keys=[id_mention])
    semester_list = relationship('JourneySemester')


# begin #
# ---write your code here--- #
# end #

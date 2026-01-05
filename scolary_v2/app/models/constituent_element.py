# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_, UniqueConstraint
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import String, Integer


class ConstituentElement(Base):
    __tablename__ = 'constituent_element'
    __table_args__ = (
        UniqueConstraint('name', 'semester', 'id_journey',
                         name='uq_name_semester_journey_constituent_element'),
    )
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    semester = Column(String(255))
    id_journey = Column(Integer, ForeignKey('journey.id'))
    color = Column(String(255))

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations
    journey = relationship('Journey', foreign_keys=[id_journey])


# begin #
# ---write your code here--- #
# end #

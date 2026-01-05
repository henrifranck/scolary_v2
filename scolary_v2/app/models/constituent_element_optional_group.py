# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_, String
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import Text, Integer


class ConstituentElementOptionalGroup(Base):
    __tablename__ = 'constituent_element_optional_group'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    id_teaching_unit_offering = Column(Integer, ForeignKey('teaching_unit_offering.id'))
    name = Column(String(255))
    selection_regle = Column(Text)

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations
    teaching_unit_offering = relationship('TeachingUnitOffering', foreign_keys=[id_teaching_unit_offering])


# begin #
# ---write your code here--- #
# end #

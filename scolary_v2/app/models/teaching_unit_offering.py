# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import Integer


class TeachingUnitOffering(Base):
    __tablename__ = 'teaching_unit_offering'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    id_teaching_unit = Column(Integer, ForeignKey('teaching_unit.id'))
    credit = Column(Integer, nullable=False)
    id_academic_year = Column(Integer, ForeignKey('academic_year.id'))
    id_teaching_unit_goup = Column(Integer, ForeignKey('teaching_unit_optional_group.id'))

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations
    teaching_unit = relationship('TeachingUnit', foreign_keys=[id_teaching_unit])
    academic_year = relationship('AcademicYear', foreign_keys=[id_academic_year])
    teaching_unit_group = relationship('TeachingUnitOptionalGroup', foreign_keys=[id_teaching_unit_goup])


# begin #
# ---write your code here--- #
# end #

# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import Integer, Float


class ConstituentElementOffering(Base):
    __tablename__ = 'constituent_element_offering'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    id_constituent_element = Column(Integer, ForeignKey('constituent_element.id'))
    weight = Column(Float, nullable=False)
    id_academic_year = Column(Integer, ForeignKey('academic_year.id'))
    id_constituent_element_optional_group = Column(Integer, ForeignKey('constituent_element_optional_group.id'))
    id_teching_unit_offering = Column(Integer, ForeignKey('teaching_unit_offering.id'))
    id_teacher = Column(Integer, ForeignKey('teacher.id'))

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations
    constituent_element = relationship('ConstituentElement', foreign_keys=[id_constituent_element])
    teacher = relationship('Teacher', foreign_keys=[id_teacher])
    academic_year = relationship('AcademicYear', foreign_keys=[id_academic_year])
    constituent_element_optional_group = relationship('ConstituentElementOptionalGroup',
                                                      foreign_keys=[id_constituent_element_optional_group])
    teching_unit_offering = relationship('TeachingUnitOffering', foreign_keys=[id_teching_unit_offering])


# begin #
# ---write your code here--- #
# end #

# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import Boolean, Integer, Float, DateTime, Text


class ResultTeachingUnit(Base):
    __tablename__ = 'result_teaching_unit'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    id_register_semester = Column(Integer, ForeignKey('register_semester.id'))
    note = Column(Float, nullable=False)
    is_valid = Column(Boolean)
    date_validation = Column(DateTime, nullable=False)
    comment = Column(Text)

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations
    student_year = relationship('RegisterSemester', foreign_keys=[id_register_semester])


# begin #
# ---write your code here--- #
# end #

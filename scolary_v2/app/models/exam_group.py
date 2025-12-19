# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import String, Enum, Integer
from app.enum.session_type import SessionTypeEnum


class ExamGroup(Base):
    __tablename__ = 'exam_group'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    id_classroom = Column(Integer, ForeignKey('classroom.id'))
    id_journey = Column(Integer, ForeignKey('journey.id'))
    semester = Column(String(255), nullable=False)
    num_from = Column(Integer, nullable=False)
    num_to = Column(Integer, nullable=False)
    session = Column(Enum(SessionTypeEnum), nullable=False)
    id_accademic_year = Column(Integer, ForeignKey('academic_year.id'))

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations
    classroom = relationship('Classroom', foreign_keys=[id_classroom])
    journey = relationship('Journey', foreign_keys=[id_journey])
    academic_year = relationship('AcademicYear', foreign_keys=[id_accademic_year])


# begin #
# ---write your code here--- #
# end #

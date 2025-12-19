# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import String, Integer, Date


class ExamDate(Base):
    __tablename__ = 'exam_date'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    id_academic_year = Column(Integer, ForeignKey('academic_year.id'))
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    session = Column(String(255))

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations
    year = relationship('AcademicYear', foreign_keys=[id_academic_year])


# begin #
# ---write your code here--- #
# end #

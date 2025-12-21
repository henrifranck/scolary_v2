# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import String, Integer


class AnnualRegister(Base):
    __tablename__ = 'annual_register'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    num_carte = Column(String(255), ForeignKey('student.num_carte'))
    id_academic_year = Column(Integer, ForeignKey('academic_year.id'))
    semester_count = Column(Integer, nullable=False)
    id_enrollment_fee = Column(Integer, ForeignKey('enrollment_fee.id'))

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations
    student = relationship('Student', foreign_keys=[num_carte], back_populates="annual_register")
    academic_year = relationship('AcademicYear', foreign_keys=[id_academic_year])
    enrollment_fee = relationship('EnrollmentFee', foreign_keys=[id_enrollment_fee])
    register_semester = relationship('RegisterSemester')
    payment = relationship('Payement')

# begin #
# ---write your code here--- #
# end #

# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import String, Integer, Date, Float, Enum, Text
from app.enum.sex import SexEnum
from app.enum.marital_status import MaritalStatusEnum
from app.enum.repeat_status import RepeatStatusEnum
from app.enum.level import LevelEnum
from app.enum.enrollment_status import EnrollmentStatusEnum


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    num_carte = Column(String(255), nullable=False, unique=True, index=True)
    email = Column(String(255), unique=True)
    num_select = Column(String(255), unique=True)
    last_name = Column(String(255), nullable=False)
    first_name = Column(String(255))
    date_of_birth = Column(Date, nullable=False)
    place_of_birth = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    sex = Column(Enum(SexEnum), nullable=False)
    martial_status = Column(Enum(MaritalStatusEnum), nullable=False)
    phone_number = Column(String(255))
    num_of_cin = Column(String(255), unique=True)
    date_of_cin = Column(Date)
    place_of_cin = Column(String(255))
    repeat_status = Column(Enum(RepeatStatusEnum))
    picture = Column(String(255), nullable=True)
    num_of_baccalaureate = Column(String(255), nullable=False, unique=True)
    center_of_baccalaureate = Column(String(255), nullable=False)
    year_of_baccalaureate = Column(Date)
    job = Column(String(255), nullable=False)
    father_name = Column(String(255))
    father_job = Column(String(255))
    mother_name = Column(String(255))
    mother_job = Column(String(255))
    parent_address = Column(Text)
    level = Column(Enum(LevelEnum))
    mean = Column(Float)
    enrollment_status = Column(Enum(EnrollmentStatusEnum), nullable=False)
    imported_id = Column(String(255))
    id_mention = Column(Integer, ForeignKey('mention.id'))
    id_enter_year = Column(Integer, ForeignKey('academic_year.id'))
    id_nationality = Column(Integer, ForeignKey('nationality.id'))
    id_baccalaureate_series = Column(Integer, ForeignKey('baccalaureate_serie.id'))

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations
    mention = relationship('Mention', foreign_keys=[id_mention])
    enter_year = relationship('AcademicYear', foreign_keys=[id_enter_year])
    nationality = relationship('Nationality', foreign_keys=[id_nationality])
    baccalaureate_serie = relationship('BaccalaureateSerie', foreign_keys=[id_baccalaureate_series])
    annual_register = relationship('AnnualRegister')


# begin #
# ---write your code here--- #
# end #

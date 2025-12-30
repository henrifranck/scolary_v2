# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_, UniqueConstraint
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import Enum, Integer, Float
from app.enum.level import LevelEnum
from app.enum.register_type import RegisterTypeEnum


class EnrollmentFee(Base):
    __tablename__ = 'enrollment_fee'
    __table_args__ = (
        UniqueConstraint('level', 'id_academic_year', 'id_mention', 'register_type',
                         name='uq_annual_renrollment_level_mention'),
    )
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    level = Column(Enum(LevelEnum), nullable=False)
    price = Column(Float, nullable=False)
    id_mention = Column(Integer, ForeignKey('mention.id'))
    register_type = Column(Enum(RegisterTypeEnum), default=RegisterTypeEnum.REGISTRATION)
    id_academic_year = Column(Integer, ForeignKey('academic_year.id'))

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations
    mention = relationship('Mention', foreign_keys=[id_mention])
    academinc_year = relationship('AcademicYear', foreign_keys=[id_academic_year])


# begin #
# ---write your code here--- #
# end #

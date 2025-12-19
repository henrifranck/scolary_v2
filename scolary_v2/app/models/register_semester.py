# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import String, Boolean, Enum, Integer
from app.enum.repeat_status import RepeatStatusEnum


class RegisterSemester(Base):
    __tablename__ = 'register_semester'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    id_annual_register = Column(Integer, ForeignKey('annual_register.id'))
    semester = Column(String(255), nullable=False)
    repeat_status = Column(Enum(RepeatStatusEnum), nullable=False)
    id_journey = Column(Integer, ForeignKey('journey.id'))
    imported_id = Column(String(255))
    is_valid = Column(Boolean)

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations
    annual_register = relationship('AnnualRegister', foreign_keys=[id_annual_register], back_populates="register_semester")
    journey = relationship('Journey', foreign_keys=[id_journey])


# begin #
# ---write your code here--- #
# end #

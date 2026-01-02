# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_, UniqueConstraint
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import Integer, String, Float, Enum

from app.enum.grade import GradeEnum


class Teacher(Base):
    __tablename__ = 'teacher'
    __table_args__ = (
        UniqueConstraint('id_user', name='uq_user_for_teacher'),
    )
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    id_user = Column(Integer, ForeignKey('user.id'))
    grade = Column(Enum(GradeEnum))

    max_hours_per_day = Column(Float)
    max_days_per_week = Column(Float)

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations
    user = relationship('User', foreign_keys=[id_user], back_populates="teacher")


# begin #
# ---write your code here--- #
# end #

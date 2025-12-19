# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import String, Time, Integer, DateTime, Enum
from app.enum.working_time_type import WorkingTimeTypeEnum
from app.enum.session_type import SessionTypeEnum


class WorkingTime(Base):
    __tablename__ = 'working_time'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    id_constituent_element = Column(Integer, ForeignKey('constituent_element_offering.id'))
    working_time_type = Column(Enum(WorkingTimeTypeEnum), nullable=False)
    day = Column(String(255))
    start = Column(Time)
    end = Column(Time)
    id_group = Column(Integer, ForeignKey('group.id'))
    date = Column(DateTime)
    session = Column(Enum(SessionTypeEnum))

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations
    constituent_element = relationship('ConstituentElementOffering', foreign_keys=[id_constituent_element])
    group = relationship('Group', foreign_keys=[id_group])


# begin #
# ---write your code here--- #
# end #

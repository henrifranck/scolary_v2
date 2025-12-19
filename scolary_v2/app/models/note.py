# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import Enum, Text, Integer, Float
from app.enum.session_type import SessionTypeEnum


class Note(Base):
    __tablename__ = 'note'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    id_register_semester = Column(Integer, ForeignKey('register_semester.id'))
    id_constituent_element_offering = Column(Integer, ForeignKey('constituent_element_offering.id'))
    session = Column(Enum(SessionTypeEnum), nullable=False)
    note = Column(Float)
    id_user = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations
    register_semester = relationship('RegisterSemester', foreign_keys=[id_register_semester])
    constituent_element_offering = relationship('ConstituentElementOffering', foreign_keys=[id_constituent_element_offering])
    user = relationship('User', foreign_keys=[id_user])


# begin #
# ---write your code here--- #
# end #

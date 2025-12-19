# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import String, Text, Integer


class University(Base):
    __tablename__ = 'university'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    province = Column(String(255), nullable=False)
    department_name = Column(String(255))
    department_other_information = Column(String(255))
    department_address = Column(Text)
    email = Column(String(255), nullable=False, unique=True, index=True)
    logo_university = Column(String(255))
    logo_departement = Column(String(255))
    phone_number = Column(String(255))
    admin_signature = Column(String(255))

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations


# begin #
# ---write your code here--- #
# end #

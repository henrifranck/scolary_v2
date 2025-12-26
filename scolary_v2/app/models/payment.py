# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import String, Date, Integer, Float, Text


class Payment(Base):
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    id_annual_register = Column(Integer, ForeignKey('annual_register.id'))
    payed = Column(Float, nullable=False)
    num_receipt = Column(String(255), nullable=False, unique=True)
    date_receipt = Column(Date, nullable=False)
    description = Column(Text)

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations
    annual_register = relationship('AnnualRegister', foreign_keys=[id_annual_register], back_populates="payment")


# begin #
# ---write your code here--- #
# end #

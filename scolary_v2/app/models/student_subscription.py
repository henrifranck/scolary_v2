# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import Integer


class StudentSubscription(Base):
    __tablename__ = 'student_subscription'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    id_subscription = Column(Integer, ForeignKey('subscription.id'))
    id_annual_register = Column(Integer, ForeignKey('annual_register.id'))

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations
    subscription = relationship('Subscription', foreign_keys=[id_subscription])
    anual_register = relationship('AnnualRegister', foreign_keys=[id_annual_register])


# begin #
# ---write your code here--- #
# end #

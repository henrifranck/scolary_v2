# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import Integer


class SubscriptionFeature(Base):
    __tablename__ = 'subscription_feature'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    id_subscription = Column(Integer, ForeignKey('subscription.id'))
    id_feature = Column(Integer, ForeignKey('feature.id'))

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations
    subscription = relationship('Subscription', foreign_keys=[id_subscription])
    feature = relationship('Feature', foreign_keys=[id_feature])


# begin #
# ---write your code here--- #
# end #

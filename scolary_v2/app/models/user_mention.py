# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import Integer


class UserMention(Base):
    __tablename__ = 'user_mention'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    id_user = Column(Integer, ForeignKey('user.id'))
    id_mention = Column(Integer, ForeignKey('mention.id'))

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations
    user = relationship('User', foreign_keys=[id_user], back_populates="user_mention")
    mention = relationship('Mention', foreign_keys=[id_mention])


# begin #
# ---write your code here--- #
# end #

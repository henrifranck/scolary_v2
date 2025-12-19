# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import String, Boolean, Integer


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_superuser = Column(Boolean)
    picture = Column(String(255))
    is_active = Column(Boolean)

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations
    user_role = relationship('UserRole', back_populates="user")
    user_mention = relationship('UserMention', back_populates="user")

# begin #
# ---write your code here--- #
# end #

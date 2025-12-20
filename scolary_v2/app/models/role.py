# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import String, Integer, Boolean


class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    use_for_card = Column(Boolean, nullable=False, default=False)

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations
    role_permission = relationship('RolePermission', back_populates="role")


# begin #
# ---write your code here--- #
# end #

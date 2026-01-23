# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_, Boolean
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import String, Integer


class Permission(Base):
    __tablename__ = 'permission'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations

    model_has_permission = relationship('ModelHasPermission', back_populates="permission")

# begin #
# ---write your code here--- #
# end #

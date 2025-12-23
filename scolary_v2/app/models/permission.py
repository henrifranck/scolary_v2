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
    model_name = Column(String(255), nullable=False)
    method_post = Column(Boolean(), default=False)
    method_get = Column(Boolean(), default=False)
    method_put = Column(Boolean(), default=False)
    method_delete = Column(Boolean(), default=False)

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations


# begin #
# ---write your code here--- #
# end #

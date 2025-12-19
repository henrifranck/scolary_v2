# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import Integer


class RolePermission(Base):
    __tablename__ = 'role_permission'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    id_role = Column(Integer, ForeignKey('role.id'))
    id_permission = Column(Integer, ForeignKey('permission.id'))

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations
    role = relationship('Role', foreign_keys=[id_role], back_populates="role_permission")
    permission = relationship('Permission', foreign_keys=[id_permission])


# begin #
# ---write your code here--- #
# end #

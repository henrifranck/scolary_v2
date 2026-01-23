# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_, Boolean
from sqlalchemy.orm import relationship, column_property, aliased
from sqlalchemy import String, Integer


class ModelHasPermission(Base):
    __tablename__ = 'model_has_permission'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    id_permission = Column(Integer, ForeignKey('permission.id'))

    id_available_model = Column(Integer, ForeignKey('available_model.id'))
    show_from_menu = Column(Boolean(), default=False)
    method_post = Column(Boolean(), default=False)
    method_get = Column(Boolean(), default=False)
    method_put = Column(Boolean(), default=False)
    method_delete = Column(Boolean(), default=False)

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations
    permission = relationship('Permission', foreign_keys=[id_permission], back_populates="model_has_permission")
    available_model = relationship('AvailableModel', foreign_keys=[id_available_model],
                                   back_populates="model_has_permission")

# begin #
# ---write your code here--- #
# end #

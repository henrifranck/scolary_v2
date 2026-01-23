# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator

from .available_model import AvailableModel


class ModelHasPermissionBase(BaseModel):
    id_permission: Optional[int] = None
    id_available_model: Optional[int] = None
    show_from_menu: Optional[bool] = False
    method_post: Optional[bool] = False
    method_get: Optional[bool] = False
    method_put: Optional[bool] = False
    method_delete: Optional[bool] = False

    model_config = ConfigDict(protected_namespaces=())


class ModelHasPermissionCreate(ModelHasPermissionBase):
    id_permission: int
    id_available_model: int
    show_from_menu: Optional[bool] = True


class ModelHasPermissionUpdate(ModelHasPermissionBase):
    pass


class ModelHasPermissionInDBBase(ModelHasPermissionBase):
    id: Optional[int]
    id_permission: int
    id_available_model: int

    model_config = ConfigDict(from_attributes=True, protected_namespaces=())


class ModelHasPermission(ModelHasPermissionInDBBase):
    pass


class ModelHasPermissionWithRelation(ModelHasPermissionInDBBase):
    available_model: Optional[AvailableModel]


class ModelHasPermissionInDB(ModelHasPermissionInDBBase):
    pass


class ResponseModelHasPermission(BaseModel):
    count: int
    data: Optional[List[ModelHasPermissionWithRelation]]

# begin #
# ---write your code here--- #
# end #

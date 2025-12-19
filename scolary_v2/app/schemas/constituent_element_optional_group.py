# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from .teaching_unit_offering import TeachingUnitOffering


class ConstituentElementOptionalGroupBase(BaseModel):
    id_teaching_unit_offering: Optional[int] = None
    selection_regle: Optional[str] = None


class ConstituentElementOptionalGroupCreate(ConstituentElementOptionalGroupBase):
    pass


class ConstituentElementOptionalGroupUpdate(ConstituentElementOptionalGroupBase):
    pass


class ConstituentElementOptionalGroupInDBBase(ConstituentElementOptionalGroupBase):
    id: Optional[int]
    id_teaching_unit_offering: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class ConstituentElementOptionalGroup(ConstituentElementOptionalGroupInDBBase):
    pass


class ConstituentElementOptionalGroupWithRelation(ConstituentElementOptionalGroupInDBBase):
    teaching_unit: Optional[TeachingUnitOffering] = None


class ConstituentElementOptionalGroupInDB(ConstituentElementOptionalGroupInDBBase):
    pass


class ResponseConstituentElementOptionalGroup(BaseModel):
    count: int
    data: Optional[List[ConstituentElementOptionalGroupWithRelation]]


# begin #
# ---write your code here--- #
# end #

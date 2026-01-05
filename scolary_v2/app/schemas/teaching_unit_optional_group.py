# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from .journey import Journey


class TeachingUnitOptionalGroupBase(BaseModel):
    id_journey: Optional[int] = None
    semester: Optional[str] = None
    name: Optional[str] = None
    selection_regle: Optional[str] = None


class TeachingUnitOptionalGroupCreate(TeachingUnitOptionalGroupBase):
    pass


class TeachingUnitOptionalGroupUpdate(TeachingUnitOptionalGroupBase):
    pass


class TeachingUnitOptionalGroupInDBBase(TeachingUnitOptionalGroupBase):
    id: Optional[int]
    id_journey: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class TeachingUnitOptionalGroup(TeachingUnitOptionalGroupInDBBase):
    pass


class TeachingUnitOptionalGroupWithRelation(TeachingUnitOptionalGroupInDBBase):
    journey: Optional[Journey] = None


class TeachingUnitOptionalGroupInDB(TeachingUnitOptionalGroupInDBBase):
    pass


class ResponseTeachingUnitOptionalGroup(BaseModel):
    count: int
    data: Optional[List[TeachingUnitOptionalGroupWithRelation]]


# begin #
# ---write your code here--- #
# end #

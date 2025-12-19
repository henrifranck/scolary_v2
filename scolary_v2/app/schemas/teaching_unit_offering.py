# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator
from .teaching_unit import TeachingUnit
from .academic_year import AcademicYear
from .teaching_unit_optional_group import TeachingUnitOptionalGroup


class TeachingUnitOfferingBase(BaseModel):
    id_teaching_unit: Optional[int] = None
    credit: Optional[int] = None
    id_academic_year: Optional[int] = None
    id_teaching_unit_goup: Optional[int] = None


class TeachingUnitOfferingCreate(TeachingUnitOfferingBase):
    credit: int


class TeachingUnitOfferingUpdate(TeachingUnitOfferingBase):
    pass


class TeachingUnitOfferingInDBBase(TeachingUnitOfferingBase):
    id: Optional[int]
    id_teaching_unit: Optional[int]
    id_academic_year: Optional[int]
    id_teaching_unit_goup: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class TeachingUnitOffering(TeachingUnitOfferingInDBBase):
    pass


class TeachingUnitOfferingWithRelation(TeachingUnitOfferingInDBBase):
    teaching_unit: Optional[TeachingUnit] = None
    academic_year: Optional[AcademicYear] = None
    teaching_unit_group: Optional[TeachingUnitOptionalGroup] = None


class TeachingUnitOfferingInDB(TeachingUnitOfferingInDBBase):
    pass


class ResponseTeachingUnitOffering(BaseModel):
    count: int
    data: Optional[List[TeachingUnitOfferingWithRelation]]


# begin #
# ---write your code here--- #
# end #

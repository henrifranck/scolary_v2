# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator

from .teacher import TeacherWithRelation
from .constituent_element import ConstituentElement
from .academic_year import AcademicYear
from .constituent_element_optional_group import ConstituentElementOptionalGroup
from .teaching_unit_offering import TeachingUnitOffering


class ConstituentElementOfferingBase(BaseModel):
    id_constituent_element: Optional[int] = None
    weight: Optional[float] = None
    id_academic_year: Optional[int] = None
    id_teacher: Optional[int] = None
    id_constituent_element_optional_group: Optional[int] = None
    id_teching_unit_offering: Optional[int] = None


class ConstituentElementOfferingCreate(ConstituentElementOfferingBase):
    weight: float


class ConstituentElementOfferingUpdate(ConstituentElementOfferingBase):
    pass


class ConstituentElementOfferingInDBBase(ConstituentElementOfferingBase):
    id: Optional[int]
    id_teacher: Optional[int]
    id_constituent_element: Optional[int]
    id_academic_year: Optional[int]
    id_constituent_element_optional_group: Optional[int]
    id_teching_unit_offering: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class ConstituentElementOffering(ConstituentElementOfferingInDBBase):
    pass


class ConstituentElementOfferingWithRelation(ConstituentElementOfferingInDBBase):
    constituent_element: Optional[ConstituentElement] = None
    academic_year: Optional[AcademicYear] = None
    teacher: Optional[TeacherWithRelation] = None
    constituent_element_optional_group: Optional[ConstituentElementOptionalGroup] = None
    teching_unit_offering: Optional[TeachingUnitOffering] = None


class ConstituentElementOfferingInDB(ConstituentElementOfferingInDBBase):
    pass


class ResponseConstituentElementOffering(BaseModel):
    count: int
    data: Optional[List[ConstituentElementOfferingWithRelation]]


# begin #
# ---write your code here--- #
# end #

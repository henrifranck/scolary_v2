# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator


class FeatureBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class FeatureCreate(FeatureBase):
    name: str


class FeatureUpdate(FeatureBase):
    pass


class FeatureInDBBase(FeatureBase):
    id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class Feature(FeatureInDBBase):
    pass


class FeatureWithRelation(FeatureInDBBase):
    pass


class FeatureInDB(FeatureInDBBase):
    pass


class ResponseFeature(BaseModel):
    count: int
    data: Optional[List[FeatureWithRelation]]


# begin #
# ---write your code here--- #
# end #

# begin #
# ---write your code here--- #
# end #

from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class CmsPageBase(BaseModel):
    slug: Optional[str] = None
    title: Optional[str] = None
    content_json: Optional[str] = None
    meta_json: Optional[str] = None
    status: Optional[str] = None


class CmsPageCreate(CmsPageBase):
    slug: str


class CmsPageUpdate(CmsPageBase):
    pass


class CmsPageInDBBase(CmsPageBase):
    id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class CmsPage(CmsPageInDBBase):
    pass


class CmsPageWithRelation(CmsPageInDBBase):
    pass


class CmsPageInDB(CmsPageInDBBase):
    pass


class ResponseCmsPage(BaseModel):
    count: int
    data: Optional[List[CmsPageWithRelation]]


# begin #
# ---write your code here--- #
# end #

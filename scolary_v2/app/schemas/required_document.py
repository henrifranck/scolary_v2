# begin #
# ---write your code here--- #
# end #

from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class RequiredDocumentBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class RequiredDocumentCreate(RequiredDocumentBase):
    name: str


class RequiredDocumentUpdate(RequiredDocumentBase):
    pass


class RequiredDocumentInDBBase(RequiredDocumentBase):
    id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class RequiredDocument(RequiredDocumentInDBBase):
    pass


class RequiredDocumentWithRelation(RequiredDocumentInDBBase):
    pass


class RequiredDocumentInDB(RequiredDocumentInDBBase):
    pass


class ResponseRequiredDocument(BaseModel):
    count: int
    data: Optional[List[RequiredDocumentWithRelation]]


# begin #
# ---write your code here--- #
# end #

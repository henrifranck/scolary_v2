# begin #
# ---write your code here--- #
# end #

from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from .available_service import AvailableService
from .required_document import RequiredDocument


class AvailableServiceRequiredDocumentBase(BaseModel):
    id_available_service: Optional[int] = None
    id_required_document: Optional[int] = None


class AvailableServiceRequiredDocumentCreate(AvailableServiceRequiredDocumentBase):
    id_available_service: int
    id_required_document: int


class AvailableServiceRequiredDocumentUpdate(AvailableServiceRequiredDocumentBase):
    pass


class AvailableServiceRequiredDocumentInDBBase(AvailableServiceRequiredDocumentBase):
    id: Optional[int]
    id_available_service: Optional[int]
    id_required_document: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class AvailableServiceRequiredDocument(AvailableServiceRequiredDocumentInDBBase):
    pass


class AvailableServiceRequiredDocumentWithRelation(AvailableServiceRequiredDocumentInDBBase):
    available_service: Optional[AvailableService] = None
    required_document: Optional[RequiredDocument] = None


class AvailableServiceRequiredDocumentInDB(AvailableServiceRequiredDocumentInDBBase):
    pass


class ResponseAvailableServiceRequiredDocument(BaseModel):
    count: int
    data: Optional[List[AvailableServiceRequiredDocumentWithRelation]]


# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Any, Dict

from pydantic import BaseModel, ConfigDict

from .annual_register import AnnualRegister


class DocumentBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    id_annual_register: Optional[int] = None
    id_required_document: Optional[int] = None
    url: Optional[str] = None


class DocumentCreate(DocumentBase):
    name: str
    id_annual_register: int
    id_required_document: Optional[int] = None
    url: str


class DocumentUpdate(DocumentBase):
    pass


class DocumentInDBBase(DocumentBase):
    id: Optional[int]
    id_annual_register: Optional[int]
    model_config = ConfigDict(from_attributes=True)


class Document(DocumentInDBBase):
    pass


class DocumentWithRelation(DocumentInDBBase):
    annual_register: Optional[AnnualRegister] = None


class DocumentInDB(DocumentInDBBase):
    pass


class ResponseDocument(BaseModel):
    count: int
    data: Optional[List[DocumentWithRelation]]

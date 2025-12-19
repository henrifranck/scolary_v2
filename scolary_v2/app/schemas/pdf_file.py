from pydantic import BaseModel


class PdfFileResponse(BaseModel):
    path: str
    filename: str
    url: str

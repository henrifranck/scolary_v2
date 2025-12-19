from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str
    is_superuser: bool


class TokenPayload(BaseModel):
    id: Optional[int] = None
    email: Optional[EmailStr]
    role: Optional[str] = None
    permissions: Optional[str] = None

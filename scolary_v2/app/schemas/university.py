# begin #
# ---write your code here--- #
# end #

from datetime import datetime, time, date
from typing import Any
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator


class UniversityBase(BaseModel):
    province: Optional[str] = None
    department_name: Optional[str] = None
    department_other_information: Optional[str] = None
    department_address: Optional[str] = None
    email: Optional[str] = None
    logo_university: Optional[str] = None
    logo_departement: Optional[str] = None
    phone_number: Optional[str] = None
    admin_signature: Optional[str] = None

    @staticmethod
    def _normalize_asset_path(value: Optional[str]) -> Optional[str]:
        if value is None or value == "":
            return value

        normalized = str(value).strip()
        normalized = normalized.lstrip("/")

        if normalized.startswith("../"):
            return normalized

        if normalized.startswith("files/"):
            normalized = normalized[len("files/"):]

        return f"../{normalized}"

    @field_validator("logo_university", "logo_departement", "admin_signature", mode="before")
    @classmethod
    def normalize_logo_paths(cls, value: Optional[str]) -> Optional[str]:
        return cls._normalize_asset_path(value)


class UniversityCreate(UniversityBase):
    province: str
    email: str


class UniversityUpdate(UniversityBase):
    pass


class UniversityInDBBase(UniversityBase):
    id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class University(UniversityInDBBase):
    pass


class UniversityWithRelation(UniversityInDBBase):
    pass


class UniversityInDB(UniversityInDBBase):
    pass


class ResponseUniversity(BaseModel):
    count: int
    data: Optional[List[UniversityWithRelation]]


# begin #
# ---write your code here--- #
# end #

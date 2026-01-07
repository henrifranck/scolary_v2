import os
import secrets
from typing import Any, Dict, List, Optional, Union
from dotenv import load_dotenv
from pydantic import AnyHttpUrl, EmailStr, HttpUrl, field_validator
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = os.getenv("BACKEND_CORS_ORIGINS")

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    MYSQL_HOST: str = os.getenv("MYSQL_HOST")
    MYSQL_PORT: int = os.getenv("MYSQL_PORT")
    MYSQL_USER: str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE")

    SQLALCHEMY_DATABASE_URI: Any = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

    # Authentication settings
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 7 days = 7 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr = os.getenv("FIRST_SUPERUSER")
    LAST_NAME_SUPERUSER: str = os.getenv("LAST_NAME_SUPERUSER")
    FIRST_NAME_SUPERUSER: str = os.getenv("FIRST_NAME_SUPERUSER")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD")
    MONGO_URI: str | None = os.getenv("MONGO_URI")
    MONGO_HOST: str | None = os.getenv("MONGO_HOST")
    MONGO_PORT: int | None = int(os.getenv("MONGO_PORT", "27017"))
    MONGO_USER: str | None = os.getenv("MONGO_USER")
    MONGO_PASSWORD: str | None = os.getenv("MONGO_PASSWORD")
    MONGO_DATABASE: str = os.getenv("MONGO_DATABASE", "scolary")

    @property
    def mongo_uri(self) -> str | None:
        if self.MONGO_URI:
            return self.MONGO_URI
        if not self.MONGO_HOST:
            return None
        auth_part = ""
        if self.MONGO_USER and self.MONGO_PASSWORD:
            auth_part = f"{self.MONGO_USER}:{self.MONGO_PASSWORD}@"
        return f"mongodb://{auth_part}{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DATABASE}?authSource=admin"

    class Config:
        case_sensitive = True


settings = Settings()

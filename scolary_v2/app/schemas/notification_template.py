from pydantic import BaseModel, Field


class NotificationTemplateBase(BaseModel):
    key: str
    title: str
    template: str
    target_roles: list[str] | None = Field(default_factory=list)


class NotificationTemplateCreate(NotificationTemplateBase):
    pass


class NotificationTemplateUpdate(BaseModel):
    key: str | None = None
    template: str | None = None
    title: str | None = None
    target_roles: list[str] | None = None


class NotificationTemplateOut(NotificationTemplateBase):
    id: int

    class Config:
        from_attributes = True

from pydantic import BaseModel


class NotificationTemplateBase(BaseModel):
    key: str
    title: str
    template: str


class NotificationTemplateCreate(NotificationTemplateBase):
    pass


class NotificationTemplateUpdate(BaseModel):
    key: str | None = None
    template: str | None = None
    title: str | None = None


class NotificationTemplateOut(NotificationTemplateBase):
    id: int

    class Config:
        from_attributes = True

from typing import Optional

from app.crud.base import CRUDBase
from app.models.notification_template import NotificationTemplate
from app.schemas.notification_template import (
    NotificationTemplateCreate,
    NotificationTemplateUpdate,
)


class CRUDNotificationTemplate(
    CRUDBase[
        NotificationTemplate,
        NotificationTemplateCreate,
        NotificationTemplateUpdate
    ]
):
    def get_by_key(self, db, *, key: str) -> Optional[NotificationTemplate]:
        return (
            db.query(NotificationTemplate)
            .filter(NotificationTemplate.key == key)
            .first()
        )


notification_template = CRUDNotificationTemplate(NotificationTemplate)

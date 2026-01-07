from sqlalchemy import Column, Integer, String, Text, DateTime, func

from app.db.base_class import Base


class NotificationTemplate(Base):
    __tablename__ = "notification_template"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    key = Column(String(100), unique=True, nullable=False, index=True)
    title = Column(String(256))
    template = Column(Text, nullable=False)

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

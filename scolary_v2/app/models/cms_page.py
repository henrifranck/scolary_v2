# begin #
# ---write your code here--- #
# end #

from app.db.base_class import Base
from sqlalchemy import Column, DateTime, Integer, String, Text, func


class CmsPage(Base):
    __tablename__ = 'cms_page'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    title = Column(String(255))
    content_json = Column(Text)
    draft_content = Column(Text)
    meta_json = Column(Text)
    status = Column(String(50), default="published")

    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)


# begin #
# ---write your code here--- #
# end #

# begin #
# ---write your code here--- #
# end #

from typing import Any, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.cms_page import CmsPage
from app.schemas.cms_page import CmsPageCreate, CmsPageUpdate


class CRUDCmsPage(CRUDBase[CmsPage, CmsPageCreate, CmsPageUpdate]):
    def get_by_slug(self, db: Session, *, slug: str) -> Optional[CmsPage]:
        return db.query(CmsPage).filter(CmsPage.slug == slug).first()


cms_page = CRUDCmsPage(CmsPage)


# begin #
# ---write your code here--- #
# end #

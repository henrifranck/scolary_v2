# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.academic_year import AcademicYear
from app.schemas.academic_year import AcademicYearCreate, AcademicYearUpdate


class CRUDAcademicYear(CRUDBase[AcademicYear, AcademicYearCreate, AcademicYearUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[AcademicYear]:
        return db.query(AcademicYear).filter(getattr(AcademicYear, field) == value).first()

academic_year = CRUDAcademicYear(AcademicYear)


# begin #
# ---write your code here--- #
# end #

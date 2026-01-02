# begin #
# ---write your code here--- #
# end #

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app.crud.base import CRUDBase
from app.models.student import Student
from app.models.register_semester import RegisterSemester
from app.models.annual_register import AnnualRegister
from app.models.journey import Journey
from app.schemas.student import StudentCreate, StudentUpdate
from app.enum.enrollment_status import EnrollmentStatusEnum


class CRUDStudent(CRUDBase[Student, StudentCreate, StudentUpdate]):
    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[Student]:
        return db.query(Student).filter(getattr(Student, field) == value).first()

    def get_for_carte(
            self,
            db: Session,
            *,
            id_mention: int,
            semester: str = "",
            semester2: str = "",
            id_year: int,
    ) -> List[Dict[str, Any]]:
        """
        Return students by mention and academic year with their latest semester registration.
        """
        subquery = (
            db.query(
                AnnualRegister.num_carte.label("num_carte"),
                RegisterSemester.id_journey.label("id_journey"),
                func.max(RegisterSemester.semester).label("max_semester"),
            )
            .join(RegisterSemester, RegisterSemester.id_annual_register == AnnualRegister.id)
            .join(Journey, Journey.id == RegisterSemester.id_journey)
            .filter(AnnualRegister.id_academic_year == id_year, Journey.id_mention == id_mention)
            .group_by(AnnualRegister.num_carte, RegisterSemester.id_journey)
            .subquery()
        )

        results = (
            db.query(
                Student.num_carte,
                Student.first_name,
                Student.last_name,
                Student.date_of_birth.label("date_birth"),
                Student.place_of_birth.label("place_birth"),
                Student.picture.label("photo"),
                Student.date_of_cin.label("date_cin"),
                Student.place_of_cin.label("place_cin"),
                Student.num_of_cin.label("num_cin"),
                Student.sex,
                Student.level,
                Journey.abbreviation,
                Journey.name,
                subquery.c.max_semester,
            )
            .join(subquery, subquery.c.num_carte == Student.num_carte)
            .join(Journey, Journey.id == subquery.c.id_journey)
            .filter(
                and_(
                    (subquery.c.max_semester == semester) | (subquery.c.max_semester == semester2),
                )
            )
        ).all()

        return [dict(row._mapping) for row in results]

    def get_selected_by_mention_year(
            self, db: Session, *, id_mention: int, id_year: int
    ) -> List[Student]:
        """
        Return students admitted by dossier selection for a mention and entry year.
        """
        return (
            db.query(Student)
            .filter(
                Student.id_mention == id_mention,
                Student.id_enter_year == id_year,
                Student.enrollment_status == EnrollmentStatusEnum.selected,
                Student.deleted_at.is_(None),
            )
            .order_by(Student.last_name.asc(), Student.first_name.asc())
            .all()
        )


student = CRUDStudent(Student)

# begin #
# ---write your code here--- #
# end #

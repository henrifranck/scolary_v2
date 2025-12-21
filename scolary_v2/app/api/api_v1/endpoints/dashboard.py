from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api import deps
from app import crud, models, schemas

router = APIRouter()


@router.get("/", response_model=schemas.DashboardStats)
def get_dashboard_summary(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Aggregate high-level counts for the dashboard.
    """
    latest_academic_year_ids = (
        db.query(models.AcademicYear.id)
        .order_by(models.AcademicYear.id.desc())
        .limit(5)
        .subquery()
    )

    mention_rows = (
        db.query(
            models.Mention.id.label("id"),
            models.Mention.name.label("name"),
            func.count(models.Student.id).label("count"),
        )
        .outerjoin(models.Student, models.Student.id_mention == models.Mention.id)
        .group_by(models.Mention.id, models.Mention.name)
        .all()
    )

    year_rows = (
        db.query(
            models.AcademicYear.id.label("id"),
            models.AcademicYear.name.label("name"),
            func.count(models.RegisterSemester.id).label("count"),
        )
        .select_from(models.RegisterSemester)
        .join(
            models.AnnualRegister,
            models.AnnualRegister.id == models.RegisterSemester.id_annual_register,
        )
        .join(
            models.AcademicYear,
            models.AcademicYear.id == models.AnnualRegister.id_academic_year,
        )
        .filter(models.AcademicYear.id.in_(latest_academic_year_ids))
        .group_by(models.AcademicYear.id, models.AcademicYear.name)
        .order_by(models.AcademicYear.name.asc())
        .all()
    )

    mention_rows_by_year = (
        db.query(
            models.AcademicYear.id.label("academic_year_id"),
            models.AcademicYear.name.label("academic_year_name"),
            models.Mention.id.label("mention_id"),
            models.Mention.name.label("mention_name"),
            func.count(models.RegisterSemester.id).label("count"),
        )
        .select_from(models.RegisterSemester)
        .join(
            models.AnnualRegister,
            models.AnnualRegister.id == models.RegisterSemester.id_annual_register,
        )
        .join(
            models.AcademicYear,
            models.AcademicYear.id == models.AnnualRegister.id_academic_year,
        )
        .join(models.Student, models.Student.num_carte == models.AnnualRegister.num_carte)
        .join(models.Mention, models.Mention.id == models.Student.id_mention)
        .filter(models.AcademicYear.id.in_(latest_academic_year_ids))
        .group_by(
            models.AcademicYear.id,
            models.AcademicYear.name,
            models.Mention.id,
            models.Mention.name,
        )
        .order_by(models.AcademicYear.name.asc(), models.Mention.name)
        .all()
    )

    return schemas.DashboardStats(
        total_students=crud.student.get_count_where_array(db=db),
        total_mentions=crud.mention.get_count_where_array(db=db),
        total_journeys=crud.journey.get_count_where_array(db=db),
        total_users=crud.user.get_count_where_array(db=db),
        mention_counts=[
            schemas.MentionCount(id=row.id, name=row.name or "", count=row.count)
            for row in mention_rows
        ],
        academic_year_counts=[
            schemas.AcademicYearCount(id=row.id, name=row.name or "", count=row.count)
            for row in year_rows
        ],
        mention_enrollments=[
            schemas.MentionEnrollment(
                academic_year_id=row.academic_year_id,
                academic_year_name=row.academic_year_name or "",
                mention_id=row.mention_id,
                mention_name=row.mention_name or "",
                count=row.count,
            )
            for row in mention_rows_by_year
        ],
    )

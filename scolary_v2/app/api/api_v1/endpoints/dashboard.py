from typing import Any
from datetime import datetime, date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, literal_column, and_, select

from app.api import deps
from app import crud, models, schemas

router = APIRouter()


def compute_summary(db: Session, academic_year_id: int | None = None) -> schemas.DashboardSummary:
    if academic_year_id:
        total_students = (
            db.query(func.count(func.distinct(models.Student.id)))
            .join(models.AnnualRegister, models.AnnualRegister.num_carte == models.Student.num_carte)
            .filter(models.AnnualRegister.id_academic_year == academic_year_id)
            .scalar()
            or 0
        )
    else:
        total_students = crud.student.get_count_where_array(db=db)

    today = date.today()
    start_of_current_year = date(today.year, 1, 1)
    start_of_next_year = date(today.year + 1, 1, 1)
    start_of_previous_year = date(today.year - 1, 1, 1)

    start_of_current_month = date(today.year, today.month, 1)
    start_of_next_month = (
        date(today.year + 1, 1, 1)
        if today.month == 12
        else date(today.year, today.month + 1, 1)
    )
    start_of_previous_month = (
        date(today.year - 1, 12, 1)
        if today.month == 1
        else date(today.year, today.month - 1, 1)
    )

    students_this_year = (
        db.query(func.count(models.Student.id))
        .filter(
            models.Student.created_at >= start_of_current_year,
            models.Student.created_at < start_of_next_year,
        )
        .scalar()
        or 0
    )
    students_previous_year = (
        db.query(func.count(models.Student.id))
        .filter(
            models.Student.created_at >= start_of_previous_year,
            models.Student.created_at < start_of_current_year,
        )
        .scalar()
        or 0
    )

    teachers_this_month = (
        db.query(func.count(models.Teacher.id))
        .filter(
            models.Teacher.created_at >= start_of_current_month,
            models.Teacher.created_at < start_of_next_month,
        )
        .scalar()
        or 0
    )
    teachers_previous_month = (
        db.query(func.count(models.Teacher.id))
        .filter(
            models.Teacher.created_at >= start_of_previous_month,
            models.Teacher.created_at < start_of_current_month,
        )
        .scalar()
        or 0
    )

    return schemas.DashboardSummary(
        total_students=total_students,
        total_mentions=crud.mention.get_count_where_array(db=db),
        total_journeys=crud.journey.get_count_where_array(db=db),
        total_users=crud.user.get_count_where_array(db=db),
        total_teachers=crud.teacher.get_count_where_array(db=db),
        students_this_year=students_this_year,
        students_previous_year=students_previous_year,
        teachers_this_month=teachers_this_month,
        teachers_previous_month=teachers_previous_month,
    )


def compute_chart_data(
        db: Session,
        *,
        min_age: int,
        max_age: int,
        mention_id: int | None,
        academic_year_id: int | None,
        journey_id: int | None,
) -> schemas.DashboardCharts:
    latest_academic_year_ids = (
        select(models.AcademicYear.id)
        .order_by(models.AcademicYear.name.desc())
        .limit(5)
        .subquery()
    )
    latest_academic_year_ids_select = select(latest_academic_year_ids.c.id)

    mention_rows = (
        db.query(
            models.Mention.id.label("id"),
            models.Mention.name.label("name"),
            func.count(func.distinct(models.Student.id)).label("count"),
        )
        .outerjoin(models.Student, models.Student.id_mention == models.Mention.id)
        .outerjoin(models.AnnualRegister, models.AnnualRegister.num_carte == models.Student.num_carte)
        .filter(*([] if not academic_year_id else [models.AnnualRegister.id_academic_year == academic_year_id]))
        .group_by(models.Mention.id, models.Mention.name)
        .all()
    )

    nationality_rows = (
        db.query(
            models.Nationality.id.label("id"),
            models.Nationality.name.label("name"),
            func.count(models.Student.id).label("count"),
        )
        .outerjoin(models.Student, models.Student.id_nationality == models.Nationality.id)
        .outerjoin(models.AnnualRegister, models.AnnualRegister.num_carte == models.Student.num_carte)
        .filter(*([] if not academic_year_id else [models.AnnualRegister.id_academic_year == academic_year_id]))
        .group_by(models.Nationality.id, models.Nationality.name)
        .order_by(func.count(models.Student.id).desc())
        .all()
    )

    role_rows = (
        db.query(
            models.Role.name.label("role"),
            func.count(func.distinct(models.User.id)).label("count"),
        )
        .select_from(models.User)
        .join(models.UserRole, models.UserRole.id_user == models.User.id)
        .join(models.Role, models.Role.id == models.UserRole.id_role)
        .group_by(models.Role.name)
        .all()
    )

    year_rows = (
        db.query(
            models.AcademicYear.id.label("id"),
            models.AcademicYear.name.label("name"),
            func.count(func.distinct(models.AnnualRegister.num_carte)).label("count"),
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
        .filter(
            models.AcademicYear.id.in_(latest_academic_year_ids_select)
            if not academic_year_id
            else models.AcademicYear.id == academic_year_id
        )
        .group_by(models.AcademicYear.id, models.AcademicYear.name)
        .order_by(models.AcademicYear.name.asc())
        .all()
    )

    new_student_year_rows = (
        db.query(
            models.AcademicYear.id.label("id"),
            models.AcademicYear.name.label("name"),
            func.count(func.distinct(models.AnnualRegister.num_carte)).label("count"),
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
        .filter(
            models.AcademicYear.id.in_(latest_academic_year_ids_select),
            models.Student.id_enter_year.in_(latest_academic_year_ids_select),
        )
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
            func.count(func.distinct(models.AnnualRegister.num_carte)).label("count"),
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
        .filter(models.AcademicYear.id.in_(latest_academic_year_ids_select))
        .group_by(
            models.AcademicYear.id,
            models.AcademicYear.name,
            models.Mention.id,
            models.Mention.name,
        )
        .order_by(models.AcademicYear.name.asc(), models.Mention.name)
        .all()
    )

    new_student_mention_rows_by_year = (
        db.query(
            models.AcademicYear.id.label("academic_year_id"),
            models.AcademicYear.name.label("academic_year_name"),
            models.Mention.id.label("mention_id"),
            models.Mention.name.label("mention_name"),
            func.count(func.distinct(models.AnnualRegister.num_carte)).label("count"),
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
        .filter(
            and_(
                models.AcademicYear.id.in_(latest_academic_year_ids_select),
                models.Student.id_enter_year.in_(latest_academic_year_ids_select),
            )
        )
        .group_by(
            models.AcademicYear.id,
            models.AcademicYear.name,
            models.Mention.id,
            models.Mention.name,
        )
        .order_by(models.AcademicYear.name.asc(), models.Mention.name)
        .all()
    )

    age_expr = func.timestampdiff(literal_column("YEAR"), models.Student.date_of_birth, func.current_date())
    age_query = (
        db.query(age_expr.label("age"), func.count(func.distinct(models.Student.id)).label("count"))
        .join(models.AnnualRegister, models.AnnualRegister.num_carte == models.Student.num_carte)
        .join(models.RegisterSemester, models.RegisterSemester.id_annual_register == models.AnnualRegister.id, isouter=True)
    )

    if mention_id:
        age_query = age_query.filter(models.Student.id_mention == mention_id)
    if academic_year_id:
        age_query = age_query.filter(models.AnnualRegister.id_academic_year == academic_year_id)
    if journey_id:
        age_query = age_query.filter(models.RegisterSemester.id_journey == journey_id)

    age_rows = (
        age_query.filter(age_expr >= min_age, age_expr <= max_age)
        .group_by("age")
        .order_by("age")
        .all()
    )
    age_map = {row.age: row.count for row in age_rows}
    age_distribution = [
        schemas.AgeBucket(age=age, count=age_map.get(age, 0))
        for age in range(min_age, max_age + 1)
    ]

    sex_query = (
        db.query(
            models.Student.sex.label("sex"),
            func.count(func.distinct(models.Student.id)).label("count"),
        )
        .join(models.AnnualRegister, models.AnnualRegister.num_carte == models.Student.num_carte)
        .join(models.RegisterSemester, models.RegisterSemester.id_annual_register == models.AnnualRegister.id, isouter=True)
    )
    if mention_id:
        sex_query = sex_query.filter(models.Student.id_mention == mention_id)
    if academic_year_id:
        sex_query = sex_query.filter(models.AnnualRegister.id_academic_year == academic_year_id)
    if journey_id:
        sex_query = sex_query.filter(models.RegisterSemester.id_journey == journey_id)
    sex_rows = sex_query.group_by(models.Student.sex).all()

    mention_sex_query = (
        db.query(
            models.Mention.id.label("mention_id"),
            models.Mention.name.label("mention_name"),
            models.Student.sex.label("sex"),
            func.count(func.distinct(models.Student.id)).label("count"),
        )
        .join(models.Student, models.Student.id_mention == models.Mention.id)
        .join(models.AnnualRegister, models.AnnualRegister.num_carte == models.Student.num_carte)
        .join(models.RegisterSemester, models.RegisterSemester.id_annual_register == models.AnnualRegister.id, isouter=True)
    )
    if mention_id:
        mention_sex_query = mention_sex_query.filter(models.Mention.id == mention_id)
    if academic_year_id:
        mention_sex_query = mention_sex_query.filter(models.AnnualRegister.id_academic_year == academic_year_id)
    if journey_id:
        mention_sex_query = mention_sex_query.filter(models.RegisterSemester.id_journey == journey_id)
    mention_sex_rows = mention_sex_query.group_by(
        models.Mention.id, models.Mention.name, models.Student.sex
    ).all()

    return schemas.DashboardCharts(
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
        new_student_mention_enrollments=[
            schemas.MentionEnrollment(
                academic_year_id=row.academic_year_id,
                academic_year_name=row.academic_year_name or "",
                mention_id=row.mention_id,
                mention_name=row.mention_name or "",
                count=row.count,
            )
            for row in new_student_mention_rows_by_year
        ],
        age_distribution=age_distribution,
        sex_counts=[
            schemas.SexCount(
                sex=row.sex.value if hasattr(row.sex, "value") else str(row.sex or ""),
                count=row.count,
            )
            for row in sex_rows
        ],
        mention_sex_counts=[
            schemas.MentionSexCount(
                mention_id=row.mention_id,
                mention_name=row.mention_name or "",
                sex=row.sex.value if hasattr(row.sex, "value") else str(row.sex or ""),
                count=row.count,
            )
            for row in mention_sex_rows
        ],
        nationality_counts=[
            schemas.NationalityCount(id=row.id, name=row.name or "", count=row.count)
            for row in nationality_rows
        ],
        role_counts=[
            schemas.RoleCount(role=row.role or "", count=row.count)
            for row in role_rows
        ],
    )


@router.get("/", response_model=schemas.DashboardStats)
def get_dashboard_all(
        *,
        min_age: int = 16,
        max_age: int = 32,
        mention_id: int | None = None,
        academic_year_id: int | None = None,
        journey_id: int | None = None,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Aggregate full dashboard (backward compatibility).
    """
    summary = compute_summary(db, academic_year_id)
    charts = compute_chart_data(
        db,
        min_age=min_age,
        max_age=max_age,
        mention_id=mention_id,
        academic_year_id=academic_year_id,
        journey_id=journey_id,
    )
    return schemas.DashboardStats(**summary.dict(), **charts.dict())


@router.get("/summary", response_model=schemas.DashboardSummary)
def get_dashboard_summary_only(
        *,
        academic_year_id: int | None = None,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Lightweight endpoint for summary KPIs.
    """
    return compute_summary(db, academic_year_id)


@router.get("/charts", response_model=schemas.DashboardCharts)
def get_dashboard_charts(
        *,
        min_age: int = 16,
        max_age: int = 32,
        mention_id: int | None = None,
        academic_year_id: int | None = None,
        journey_id: int | None = None,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Endpoint for heavy chart data.
    """
    return compute_chart_data(
        db,
        min_age=min_age,
        max_age=max_age,
        mention_id=mention_id,
        academic_year_id=academic_year_id,
        journey_id=journey_id,
    )

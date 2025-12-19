from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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
    return schemas.DashboardStats(
        total_students=crud.student.get_count_where_array(db=db),
        total_mentions=crud.mention.get_count_where_array(db=db),
        total_journeys=crud.journey.get_count_where_array(db=db),
        total_users=crud.user.get_count_where_array(db=db),
    )

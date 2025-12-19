from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_students: int
    total_mentions: int
    total_journeys: int
    total_users: int

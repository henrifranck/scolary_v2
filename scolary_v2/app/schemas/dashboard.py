from pydantic import BaseModel


class MentionCount(BaseModel):
    id: int
    name: str
    count: int

class AcademicYearCount(BaseModel):
    id: int
    name: str
    count: int

class MentionEnrollment(BaseModel):
    academic_year_id: int
    academic_year_name: str
    mention_id: int
    mention_name: str
    count: int


class DashboardStats(BaseModel):
    total_students: int
    total_mentions: int
    total_journeys: int
    total_users: int
    mention_counts: list[MentionCount]
    academic_year_counts: list[AcademicYearCount]
    mention_enrollments: list[MentionEnrollment]
    

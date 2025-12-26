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


class AgeBucket(BaseModel):
    age: int
    count: int


class SexCount(BaseModel):
    sex: str
    count: int


class MentionSexCount(BaseModel):
    mention_id: int
    mention_name: str
    sex: str
    count: int


class NationalityCount(BaseModel):
    id: int
    name: str
    count: int


class RoleCount(BaseModel):
    role: str
    count: int


class DashboardStats(BaseModel):
    total_students: int
    total_mentions: int
    total_journeys: int
    total_users: int
    mention_counts: list[MentionCount]
    academic_year_counts: list[AcademicYearCount]
    mention_enrollments: list[MentionEnrollment]
    new_student_mention_enrollments: list[MentionEnrollment]
    age_distribution: list[AgeBucket]
    sex_counts: list[SexCount]
    mention_sex_counts: list[MentionSexCount]
    nationality_counts: list[NationalityCount]
    role_counts: list[RoleCount]

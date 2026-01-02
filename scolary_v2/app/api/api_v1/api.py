from fastapi import APIRouter

from app.api.api_v1.endpoints import subscription_features
from app.api.api_v1.endpoints import dashboard
from app.api.api_v1.endpoints import academic_years
from app.api.api_v1.endpoints import users
from app.api.api_v1.endpoints import documents
from app.api.api_v1.endpoints import roles
from app.api.api_v1.endpoints import journey_semesters
from app.api.api_v1.endpoints import annual_registers
from app.api.api_v1.endpoints import constituent_element_optional_groups
from app.api.api_v1.endpoints import nationalitys
from app.api.api_v1.endpoints import journeys
from app.api.api_v1.endpoints import subscriptions
from app.api.api_v1.endpoints import features
from app.api.api_v1.endpoints import user_mentions
from app.api.api_v1.endpoints import result_teaching_units
from app.api.api_v1.endpoints import groups
from app.api.api_v1.endpoints import exam_dates
from app.api.api_v1.endpoints import notes
from app.api.api_v1.endpoints import exam_groups
from app.api.api_v1.endpoints import user_roles
from app.api.api_v1.endpoints import register_semesters
from app.api.api_v1.endpoints import teaching_units
from app.api.api_v1.endpoints import enrollment_fees
from app.api.api_v1.endpoints import role_permissions
from app.api.api_v1.endpoints import permissions
from app.api.api_v1.endpoints import working_times
from app.api.api_v1.endpoints import student_subscriptions
from app.api.api_v1.endpoints import classrooms
from app.api.api_v1.endpoints import teaching_unit_optional_groups
from app.api.api_v1.endpoints import mentions
from app.api.api_v1.endpoints import baccalaureate_series
from app.api.api_v1.endpoints import login
from app.api.api_v1.endpoints import constituent_elements
from app.api.api_v1.endpoints import students
from app.api.api_v1.endpoints import constituent_element_offerings
from app.api.api_v1.endpoints import teaching_unit_offerings
from app.api.api_v1.endpoints import universitys
from app.api.api_v1.endpoints import payments
from app.api.api_v1.endpoints import files
from app.api.api_v1.endpoints import pdfs
from app.api.api_v1.endpoints import liste
from app.api.api_v1.endpoints import carte
from app.api.api_v1.endpoints import required_documents
from app.api.api_v1.endpoints import available_services
from app.api.api_v1.endpoints import available_models
from app.api.api_v1.endpoints import available_service_required_documents
from app.api.api_v1.endpoints import cms_pages
from app.api.api_v1.endpoints import teacher

api_router = APIRouter()
api_router.include_router(classrooms.router, prefix="/classrooms", tags=["classrooms"])
api_router.include_router(nationalitys.router, prefix="/nationalitys", tags=["nationalitys"])
api_router.include_router(baccalaureate_series.router, prefix="/baccalaureate_series", tags=["baccalaureate_series"])
api_router.include_router(universitys.router, prefix="/universitys", tags=["universitys"])

api_router.include_router(academic_years.router, prefix="/academic_years", tags=["academic_years"])
api_router.include_router(mentions.router, prefix="/mentions", tags=["mentions"])
api_router.include_router(journeys.router, prefix="/journey", tags=["journey"])

api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(teacher.router, prefix="/teacher", tags=["teacher"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(user_roles.router, prefix="/user_roles", tags=["user_roles"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(permissions.router, prefix="/permissions", tags=["permissions"])
api_router.include_router(role_permissions.router, prefix="/role_permissions", tags=["role_permissions"])
api_router.include_router(user_mentions.router, prefix="/user_mentions", tags=["user_mentions"])

api_router.include_router(features.router, prefix="/features", tags=["features"])
api_router.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])
api_router.include_router(subscription_features.router, prefix="/subscription_features", tags=["subscription_features"])
api_router.include_router(student_subscriptions.router, prefix="/student_subscriptions", tags=["student_subscriptions"])

api_router.include_router(journey_semesters.router, prefix="/journey_semesters", tags=["journey_semesters"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])
api_router.include_router(annual_registers.router, prefix="/annual_registers", tags=["annual_registers"])
api_router.include_router(register_semesters.router, prefix="/register_semesters", tags=["register_semesters"])
api_router.include_router(required_documents.router, prefix="/required_documents", tags=["required_documents"])
api_router.include_router(available_services.router, prefix="/available_services", tags=["available_services"])
api_router.include_router(
    available_service_required_documents.router,
    prefix="/available_service_required_documents",
    tags=["available_service_required_documents"],
)

api_router.include_router(available_models.router, prefix="/available_models", tags=["available_models"])
api_router.include_router(cms_pages.router, prefix="/cms_pages", tags=["cms_pages"])
api_router.include_router(exam_dates.router, prefix="/exam_dates", tags=["exam_dates"])
api_router.include_router(exam_groups.router, prefix="/exam_groups", tags=["exam_groups"])
api_router.include_router(groups.router, prefix="/groups", tags=["groups"])
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])
api_router.include_router(result_teaching_units.router, prefix="/result_teaching_units", tags=["result_teaching_units"])
api_router.include_router(teaching_units.router, prefix="/teaching_units", tags=["teaching_units"])
api_router.include_router(enrollment_fees.router, prefix="/enrollment_fees", tags=["enrollment_fees"])
api_router.include_router(working_times.router, prefix="/working_times", tags=["working_times"])
api_router.include_router(teaching_unit_optional_groups.router, prefix="/teaching_unit_optional_groups", tags=["teaching_unit_optional_groups"])
api_router.include_router(constituent_elements.router, prefix="/constituent_elements", tags=["constituent_elements"])
api_router.include_router(constituent_element_offerings.router, prefix="/constituent_element_offerings", tags=["constituent_element_offerings"])
api_router.include_router(teaching_unit_offerings.router, prefix="/teaching_unit_offerings", tags=["teaching_unit_offerings"])

api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(pdfs.router, prefix="/pdf", tags=["pdf"])
api_router.include_router(liste.router, prefix="/liste", tags=["liste"])
api_router.include_router(carte.router, prefix="/carte", tags=["carte"])

api_router.include_router(constituent_element_optional_groups.router, prefix="/constituent_element_optional_groups",
                          tags=["constituent_element_optional_groups"])
api_router.include_router(files.router, prefix="/files", tags=["files"])

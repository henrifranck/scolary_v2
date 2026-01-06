from .teaching_unit_offering import (
    TeachingUnitOffering,
    TeachingUnitOfferingCreate,
    TeachingUnitOfferingUpdate,
    ResponseTeachingUnitOffering
)
from .role_permission import (
    RolePermission,
    RolePermissionCreate,
    RolePermissionUpdate,
    ResponseRolePermission
)
from .exam_group import (
    ExamGroup,
    ExamGroupCreate,
    ExamGroupUpdate,
    ResponseExamGroup
)
from .journey_semester import (
    JourneySemester,
    JourneySemesterCreate,
    JourneySemesterUpdate,
    ResponseJourneySemester
)
from .university import (
    University,
    UniversityCreate,
    UniversityUpdate,
    ResponseUniversity
)
from .user import (
    User,
    UserCreate,
    UserUpdate,
    ResponseUser
)
from .user_role import (
    UserRole,
    UserRoleCreate,
    UserRoleUpdate,
    ResponseUserRole
)
from .student_subscription import (
    StudentSubscription,
    StudentSubscriptionCreate,
    StudentSubscriptionUpdate,
    ResponseStudentSubscription
)
from .teaching_unit import (
    TeachingUnit,
    TeachingUnitCreate,
    TeachingUnitUpdate,
    ResponseTeachingUnit
)
from .token import Token, TokenPayload
from .result_teaching_unit import (
    ResultTeachingUnit,
    ResultTeachingUnitCreate,
    ResultTeachingUnitUpdate,
    ResponseResultTeachingUnit
)
from .subscription import (
    Subscription,
    SubscriptionCreate,
    SubscriptionUpdate,
    ResponseSubscription
)
from .permission import (
    Permission,
    PermissionCreate,
    PermissionUpdate,
    ResponsePermission
)
from .cms_page import (
    CmsPage,
    CmsPageCreate,
    CmsPageUpdate,
    ResponseCmsPage
)
from .classroom import (
    Classroom,
    ClassroomCreate,
    ClassroomUpdate,
    ResponseClassroom
)
from .academic_year import (
    AcademicYear,
    AcademicYearCreate,
    AcademicYearUpdate,
    ResponseAcademicYear
)
from .subscription_feature import (
    SubscriptionFeature,
    SubscriptionFeatureCreate,
    SubscriptionFeatureUpdate,
    ResponseSubscriptionFeature
)
from .role import (
    Role,
    RoleCreate,
    RoleUpdate,
    ResponseRole
)
from .feature import (
    Feature,
    FeatureCreate,
    FeatureUpdate,
    ResponseFeature
)
from .user_mention import (
    UserMention,
    UserMentionCreate,
    UserMentionUpdate,
    ResponseUserMention
)
from .annual_register import (
    AnnualRegister,
    AnnualRegisterCreate,
    AnnualRegisterUpdate,
    ResponseAnnualRegister
)
from .working_time import (
    WorkingTime,
    WorkingTimeCreate,
    WorkingTimeUpdate,
    ResponseWorkingTime
)
from .journey import (
    Journey,
    JourneyCreate,
    JourneyUpdate,
    ResponseJourney
)
from .register_semester import (
    RegisterSemester,
    RegisterSemesterCreate,
    RegisterSemesterUpdate,
    ResponseRegisterSemester
)
from .constituent_element import (
    ConstituentElement,
    ConstituentElementCreate,
    ConstituentElementUpdate,
    ResponseConstituentElement
)
from .group import (
    Group,
    GroupCreate,
    GroupUpdate,
    ResponseGroup
)
from .teaching_unit_optional_group import (
    TeachingUnitOptionalGroup,
    TeachingUnitOptionalGroupCreate,
    TeachingUnitOptionalGroupUpdate,
    ResponseTeachingUnitOptionalGroup
)
from .student import (
    Student,
    StudentCreate,
    StudentUpdate,
    ResponseStudent,
    StudentWithRelation,
    StudentCard,
    StudentCardNumber,
    StudentNewCreate
)
from .constituent_element_optional_group import (
    ConstituentElementOptionalGroup,
    ConstituentElementOptionalGroupCreate,
    ConstituentElementOptionalGroupUpdate,
    ResponseConstituentElementOptionalGroup
)
from .baccalaureate_serie import (
    BaccalaureateSerie,
    BaccalaureateSerieCreate,
    BaccalaureateSerieUpdate,
    ResponseBaccalaureateSerie
)
from .mention import (
    Mention,
    MentionCreate,
    MentionUpdate,
    ResponseMention
)
from .exam_date import (
    ExamDate,
    ExamDateCreate,
    ExamDateUpdate,
    ResponseExamDate
)
from .msg import Msg
from .constituent_element_offering import (
    ConstituentElementOffering,
    ConstituentElementOfferingCreate,
    ConstituentElementOfferingUpdate,
    ResponseConstituentElementOffering
)
from .note import (
    Note,
    NoteCreate,
    NoteUpdate,
    ResponseNote
)
from .nationality import (
    Nationality,
    NationalityCreate,
    NationalityUpdate,
    ResponseNationality
)
from .card_asset import CardAsset, CardAssetCreate
from .pdf_file import PdfFileResponse
from .document import (
    Document,
    DocumentCreate,
    DocumentUpdate,
    ResponseDocument,
)
from .dashboard import (
    DashboardStats,
    MentionCount,
    AcademicYearCount,
    MentionEnrollment,
    AgeBucket,
    SexCount,
    MentionSexCount,
    NationalityCount,
    RoleCount,
    DashboardCharts,
    DashboardSummary
)
from .enrollment_fee import (
    EnrollmentFee,
    EnrollmentFeeCreate,
    EnrollmentFeeUpdate,
    ResponseEnrollmentFee
)
from .payment import (
    Payment,
    PaymentCreate,
    PaymentUpdate,
    ResponsePayment
)

from .file_asset import (
    FileAsset,
    ResponseFileAsset,
    FileAssetUpdate,
    FileAssetCreate
)
from .available_service import (
    AvailableService,
    AvailableServiceCreate,
    AvailableServiceUpdate,
    ResponseAvailableService
)

from .available_model import (
    AvailableModel,
    AvailableModelCreate,
    AvailableModelUpdate,
    ResponseAvailableModel
)

from .required_document import (
    RequiredDocument,
    RequiredDocumentCreate,
    RequiredDocumentUpdate,
    ResponseRequiredDocument
)
from .available_service_required_document import (
    AvailableServiceRequiredDocument,
    AvailableServiceRequiredDocumentCreate,
    AvailableServiceRequiredDocumentUpdate,
    ResponseAvailableServiceRequiredDocument
)

from .teacher import (
    Teacher,
    TeacherCreate,
    TeacherUpdate,
    TeacherWithRelation,
    ResponseTeacher
)

from .plugged import (
    Plugged,
    PluggedCreate,
    PluggedUpdate,
    ResponsePlugged
)

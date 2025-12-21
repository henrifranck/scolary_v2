from enum import Enum


class EnrollmentStatusEnum(Enum):
    pending = "pending"
    rejected = "rejected"
    selected = "selected"
    registered = "registered"
    former = "former"

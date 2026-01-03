# begin #
# ---write your code here--- #
# end #
from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, Integer, cast, Enum
from sqlalchemy.orm import relationship, column_property
from sqlalchemy import String, UniqueConstraint
from app.enum.register_type import RegisterTypeEnum
from app.models.enrollment_fee import EnrollmentFee
from app.models.journey import Journey
from app.models.payment import Payment
from app.models.register_semester import RegisterSemester
from app.enum.level import LevelEnum


class AnnualRegister(Base):
    __tablename__ = 'annual_register'
    __table_args__ = (
        UniqueConstraint('num_carte', 'id_academic_year', 'register_type',
                         name='uq_annual_register_student_year'),
        UniqueConstraint('num_select', 'id_academic_year', 'register_type',
                         name='uq_annual_seletion_student_year'),
    )
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    num_carte = Column(String(255), ForeignKey('student.num_carte'))
    num_select = Column(String(255), ForeignKey('student.num_select'))
    id_academic_year = Column(Integer, ForeignKey('academic_year.id'))
    register_type = Column(Enum(RegisterTypeEnum), default=RegisterTypeEnum.REGISTRATION)
    semester_count = Column(Integer, nullable=False)
    registration_code = Column(String(100), nullable=True)
    verified_by = Column(Integer, ForeignKey('user.id'))
    verified_at = Column(DateTime)

    # default column
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relations
    student = relationship('Student', foreign_keys=[num_carte], back_populates="annual_register")
    student_selection = relationship('Student', foreign_keys=[num_select])
    academic_year = relationship('AcademicYear', foreign_keys=[id_academic_year])
    register_semester = relationship('RegisterSemester')
    payment = relationship('Payment')
    document = relationship('Document', back_populates='annual_register')
    user = relationship('User')

# Computed properties declared after class definition to avoid mapper warnings
max_semester_number_expr = (
    select(
        func.max(
            cast(func.replace(RegisterSemester.semester, "S", ""), Integer)
        )
    )
    .where(RegisterSemester.id_annual_register == AnnualRegister.id)
    .correlate_except(RegisterSemester)
    .scalar_subquery()
)

AnnualRegister.max_semester_number = column_property(max_semester_number_expr)

AnnualRegister.level_from_semester = column_property(
    case(
        (max_semester_number_expr <= 2, LevelEnum.L1.value),
        (max_semester_number_expr <= 4, LevelEnum.L2.value),
        (max_semester_number_expr <= 6, LevelEnum.L3.value),
        (max_semester_number_expr <= 8, LevelEnum.M1.value),
        (max_semester_number_expr <= 10, LevelEnum.M2.value),
        else_="",
    )
)

total_payment_expr = (
    select(func.coalesce(func.sum(Payment.payed), 0.0))
    .where(Payment.id_annual_register == AnnualRegister.id)
    .correlate_except(Payment)
    .scalar_subquery()
)

AnnualRegister.total_payment = column_property(total_payment_expr)

max_semester_journey_id_expr = (
    select(RegisterSemester.id_journey)
    .where(
        RegisterSemester.id_annual_register == AnnualRegister.id,
        cast(func.replace(RegisterSemester.semester, "S", ""), Integer) == max_semester_number_expr,
    )
    .limit(1)
    .correlate_except(RegisterSemester)
    .scalar_subquery()
)

AnnualRegister.max_semester_journey_id = column_property(max_semester_journey_id_expr)

AnnualRegister.mention_id_from_max_semester = column_property(
    select(Journey.id_mention)
    .where(Journey.id == max_semester_journey_id_expr)
    .correlate_except(Journey)
    .scalar_subquery()
)

enrollment_fee_amount_expr = (
    select(EnrollmentFee.price)
    .where(
        EnrollmentFee.level == AnnualRegister.level_from_semester,
        EnrollmentFee.id_academic_year == AnnualRegister.id_academic_year,
        EnrollmentFee.id_mention == AnnualRegister.mention_id_from_max_semester,
    )
    .limit(1)
    .correlate_except(EnrollmentFee)
    .scalar_subquery()
)

AnnualRegister.enrollment_fee_amount = column_property(enrollment_fee_amount_expr)

AnnualRegister.payment_status = column_property(
    case(
        (enrollment_fee_amount_expr.is_(None), "not_applicable"),
        (total_payment_expr >= enrollment_fee_amount_expr, "complete"),
        (total_payment_expr == 0, "none"),
        else_="partial",
    )
)

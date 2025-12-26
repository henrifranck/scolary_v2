# begin #
# ---write your code here--- #
# end #
from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, DateTime, func, select, case, or_, and_, Integer, cast, Enum
from sqlalchemy.orm import relationship, column_property, aliased, deferred
from sqlalchemy import String, UniqueConstraint
from app.enum.register_type import RegisterTypeEnum


class AnnualRegister(Base):
    __tablename__ = 'annual_register'
    __table_args__ = (
        UniqueConstraint('num_carte', 'id_academic_year', 'register_type',
                         name='uq_annual_register_student_year'),
    )
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    num_carte = Column(String(255), ForeignKey('student.num_carte'))
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
    academic_year = relationship('AcademicYear', foreign_keys=[id_academic_year])
    register_semester = relationship('RegisterSemester')
    payment = relationship('Payment')
    document = relationship('Document')
    user = relationship('User')

# begin #
# ---write your code here--- #
    # Max semester number across related register_semester (S1 -> 1, etc.)
    from app.models.register_semester import RegisterSemester
    from app.models.payment import Payment
    from app.models.enrollment_fee import EnrollmentFee
    from app.models.journey import Journey
    from app.enum.level import LevelEnum

    _max_semester_expr = (
        select(
            func.max(
                cast(func.replace(RegisterSemester.semester, "S", ""), Integer)
            )
        )
        .where(RegisterSemester.id_annual_register == id)
        .correlate_except(RegisterSemester)
        .scalar_subquery()
    )

    max_semester_number = column_property(_max_semester_expr)

    # Derived level based on max semester
    level_from_semester = column_property(
        case(
            (_max_semester_expr <= 2, LevelEnum.L1.value),
            (_max_semester_expr <= 4, LevelEnum.L2.value),
            (_max_semester_expr <= 6, LevelEnum.L3.value),
            (_max_semester_expr <= 8, LevelEnum.M1.value),
            else_=LevelEnum.M2.value,
        )
    )

    _total_payment_expr = (
        select(func.coalesce(func.sum(Payment.payed), 0.0))
        .where(Payment.id_annual_register == id)
        .correlate_except(Payment)
        .scalar_subquery()
    )

    total_payment = column_property(_total_payment_expr)

    # resolve journey + mention from the semester with highest number
    _max_semester_journey_id = (
        select(RegisterSemester.id_journey)
        .where(
            RegisterSemester.id_annual_register == id,
            cast(func.replace(RegisterSemester.semester, "S", ""), Integer) == _max_semester_expr,
        )
        .limit(1)
        .correlate_except(RegisterSemester)
        .scalar_subquery()
    )

    mention_id_from_max_semester = column_property(
        select(Journey.id_mention)
        .where(Journey.id == _max_semester_journey_id)
        .correlate_except(Journey)
        .scalar_subquery()
    )

    _enrollment_fee_amount_expr = (
        select(EnrollmentFee.price)
        .where(
            EnrollmentFee.level == level_from_semester,
            EnrollmentFee.id_academic_year == id_academic_year,
            EnrollmentFee.id_mention == mention_id_from_max_semester,
        )
        .limit(1)
        .correlate_except(EnrollmentFee)
        .scalar_subquery()
    )

    enrollment_fee_amount = column_property(_enrollment_fee_amount_expr)

    payment_status = column_property(
        case(
            (_enrollment_fee_amount_expr.is_(None), "not_applicable"),
            (_total_payment_expr >= _enrollment_fee_amount_expr, "complete"),
            (_total_payment_expr == 0, "none"),
            else_="partial",
        )
    )
# end #

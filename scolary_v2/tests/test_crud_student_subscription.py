# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from sqlalchemy.orm import Session
from typing import Any, Dict
import pytest
from datetime import datetime, date, time, timedelta
import uuid
import random
"""Tests for CRUD operations on StudentSubscription model."""


def test_create_student_subscription(db: Session):
    """Test create operation for StudentSubscription."""
    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='tzgQs',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='tp4mk',
        slug='54Jny',
        abbreviation='dFRzp',
        plugged='cd5PO',
        background='4iMQ4',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='AA1jP',
        code='KH5mp',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='Co7OA',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='No4E6',
        value='e87px',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='KyTrO',
        email='5mahM@p9dai.com',
        num_select='5VHXn',
        last_name='5Ht5b',
        first_name='L1KDf',
        date_of_birth='2025-11-15',
        place_of_birth='JndBQ',
        address='utJe9H82GdMGxckKRYhG4oyxs',
        sex='Féminin',
        martial_status='Célibataire',
        phone_number='qpaFZ',
        num_of_cin='a5mpo',
        date_of_cin='2025-11-15',
        place_of_cin='0H3qQ',
        repeat_status='1',
        picture='aeJqs',
        num_of_baccalaureate='aHgls',
        center_of_baccalaureate='mS4wW',
        year_of_baccalaureate='2025-11-15',
        job='e6OY8',
        father_name='w472k',
        father_job='ksA5q',
        mother_name='xYGlN',
        mother_job='mg3HD',
        parent_address='Zwhxi133e1g',
        level='L3',
        mean=3.702162395377593,
        enrollment_status='Sélectionné(e)',
        imported_id='l2w26',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=3.50282599548759,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=0,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for StudentSubscription
    student_subscription_data = schemas.StudentSubscriptionCreate(
        id_subscription=subscription.id,
        id_annual_register=annual_register.id,
    )

    student_subscription = crud.student_subscription.create(db=db, obj_in=student_subscription_data)

    # Assertions
    assert student_subscription.id is not None
    assert student_subscription.id_subscription == student_subscription_data.id_subscription
    assert student_subscription.id_annual_register == student_subscription_data.id_annual_register


def test_update_student_subscription(db: Session):
    """Test update operation for StudentSubscription."""
    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='TeAIC',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='jECZr',
        slug='goy6R',
        abbreviation='ntE6u',
        plugged='mKXh9',
        background='3PwG2',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='bbWIr',
        code='ZKHIh',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='tCsUU',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='pjTMJ',
        value='IaKLi',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='8zrlv',
        email='AS5MM@7rtev.com',
        num_select='QSHiv',
        last_name='HzRuV',
        first_name='1dmGc',
        date_of_birth='2025-11-15',
        place_of_birth='9zWq4',
        address='xErHhXT4l',
        sex='Masculin',
        martial_status='Célibataire',
        phone_number='kNwTG',
        num_of_cin='wLMHJ',
        date_of_cin='2025-11-15',
        place_of_cin='a5qHT',
        repeat_status='1',
        picture='sEtpM',
        num_of_baccalaureate='7QcUz',
        center_of_baccalaureate='sDhr9',
        year_of_baccalaureate='2025-11-15',
        job='Vrvzm',
        father_name='zaIKj',
        father_job='TvLug',
        mother_name='0qCsR',
        mother_job='qoi4g',
        parent_address='57GKgSaXizJIMmGMK7lUbAh4FVAjhN2gRk14JTEh2x6EGWlTCnQciDMurk36A3ewnB2mLVjiDDBXTsx',
        level='L3',
        mean=2.927805018663762,
        enrollment_status='Inscrit(e)',
        imported_id='WXzL5',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=5.172991544135492,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=0,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for StudentSubscription
    student_subscription_data = schemas.StudentSubscriptionCreate(
        id_subscription=subscription.id,
        id_annual_register=annual_register.id,
    )

    student_subscription = crud.student_subscription.create(db=db, obj_in=student_subscription_data)

    # Precompute enum values for update
    enum_values_map = {}

    # Helper to compute a new value different from the current one
    def _updated_value(k, v):
        from decimal import Decimal

        # bool -> invert
        if isinstance(v, bool):
            return not v

        # numeric -> +1 (int, float, Decimal)
        if isinstance(v, (int, float, Decimal)):
            return v + 1

        # enum -> next value from enum_values_map
        if k in enum_values_map:
            current = v.value if hasattr(v, 'value') else v
            values = enum_values_map[k]
            try:
                idx = values.index(current)
                if len(values) > 1:
                    return values[(idx + 1) % len(values)]
                else:
                    return current
            except ValueError:
                # If current not in list, fallback to first value
                return values[0] if values else v

        # datetime +1 day
        if k in [] and isinstance(v, str):
            return (datetime.fromisoformat(v) + timedelta(days=1)).isoformat()
        if k in [] and isinstance(v, datetime):
            return v + timedelta(days=1)

        # date +1 day
        if k in [] and isinstance(v, str):
            return (date.fromisoformat(v) + timedelta(days=1)).isoformat()
        if k in [] and isinstance(v, date):
            return v + timedelta(days=1)

        # time +1 hour
        if k in [] and isinstance(v, str):
            return (datetime.strptime(v, '%H:%M:%S') + timedelta(hours=1)).time().strftime('%H:%M:%S')
        if k in [] and isinstance(v, time):
            return (datetime.combine(date.today(), v) + timedelta(hours=1)).time()

        # fallback -> prefix 'updated_'
        return f'updated_{v}'

    # Update data
    update_data = schemas.StudentSubscriptionUpdate(**{
        k: _updated_value(k, v)
        for k, v in student_subscription_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_student_subscription = crud.student_subscription.update(
        db=db, db_obj=student_subscription, obj_in=update_data
    )

    # Assertions
    assert updated_student_subscription.id == student_subscription.id


def test_get_student_subscription(db: Session):
    """Test get operation for StudentSubscription."""
    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='wCnKF',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='V2jZW',
        slug='RqXiN',
        abbreviation='KHPR7',
        plugged='rZnZi',
        background='b9Rxq',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='M671b',
        code='XiEOD',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='etwj4',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='OVMTY',
        value='ZZEfU',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='63Dpo',
        email='DOx0C@n4zn9.com',
        num_select='2eVGV',
        last_name='MbDhK',
        first_name='Bigak',
        date_of_birth='2025-11-15',
        place_of_birth='l7HQz',
        address='MGDgV4iWxVPe7PE3FbAgHjlQ8WSMsp29toUf718izBNqM8BK7gIG7SYNS',
        sex='Féminin',
        martial_status='Célibataire',
        phone_number='JjWtP',
        num_of_cin='mZqGX',
        date_of_cin='2025-11-15',
        place_of_cin='Zww8q',
        repeat_status='0',
        picture='hZL8o',
        num_of_baccalaureate='wZMm0',
        center_of_baccalaureate='HHmEg',
        year_of_baccalaureate='2025-11-15',
        job='kGp6Q',
        father_name='JpXId',
        father_job='gJSJj',
        mother_name='y9kpa',
        mother_job='IYepo',
        parent_address='WmNjGRDRjgBfPuHPQewQl74WEkk9qpYj1KxsYNKLVzmGA',
        level='L3',
        mean=2.407816927083449,
        enrollment_status='ancien(ne)',
        imported_id='b1deS',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=2.3636920708421414,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=4,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for StudentSubscription
    student_subscription_data = schemas.StudentSubscriptionCreate(
        id_subscription=subscription.id,
        id_annual_register=annual_register.id,
    )

    student_subscription = crud.student_subscription.create(db=db, obj_in=student_subscription_data)

    # Get all records
    records = crud.student_subscription.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == student_subscription.id for r in records)


def test_get_by_id_student_subscription(db: Session):
    """Test get_by_id operation for StudentSubscription."""
    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='8jfAn',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='QMqxI',
        slug='mALKJ',
        abbreviation='6Z4Kp',
        plugged='HaloK',
        background='3GDH4',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='fyeid',
        code='u6gA0',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='X56Hh',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='YuyYV',
        value='zVgvK',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='iOMNL',
        email='cN1mX@aiasf.com',
        num_select='ei0SU',
        last_name='uO9g4',
        first_name='8bZAb',
        date_of_birth='2025-11-15',
        place_of_birth='5ObSE',
        address='Z5J1DEY4Zofg0uZJayzP6KKTc1rSjGSb4R64nY8ch3DLDGZinxBqNLqwkvOp',
        sex='Féminin',
        martial_status='Veuf/Veuve',
        phone_number='JB6Al',
        num_of_cin='SNfFj',
        date_of_cin='2025-11-15',
        place_of_cin='scNM6',
        repeat_status='2',
        picture='7P3Io',
        num_of_baccalaureate='OplTJ',
        center_of_baccalaureate='Ddy35',
        year_of_baccalaureate='2025-11-15',
        job='deSbe',
        father_name='JrH4i',
        father_job='0MeKW',
        mother_name='zB4ii',
        mother_job='Q0y50',
        parent_address='jBKrsXAk7SlV2ff4AHNqgZ0FMSpEflkMuT0ZJDPBoz0hLjR',
        level='M1',
        mean=3.575271257158105,
        enrollment_status='Inscrit(e)',
        imported_id='9JgCJ',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=4.408182092966163,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=5,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for StudentSubscription
    student_subscription_data = schemas.StudentSubscriptionCreate(
        id_subscription=subscription.id,
        id_annual_register=annual_register.id,
    )

    student_subscription = crud.student_subscription.create(db=db, obj_in=student_subscription_data)

    # Get by ID
    retrieved_student_subscription = crud.student_subscription.get(db=db, id=student_subscription.id)

    # Assertions
    assert retrieved_student_subscription is not None
    assert retrieved_student_subscription.id == student_subscription.id
    assert retrieved_student_subscription.id_subscription == student_subscription.id_subscription
    assert retrieved_student_subscription.id_annual_register == student_subscription.id_annual_register


def test_delete_student_subscription(db: Session):
    """Test delete operation for StudentSubscription."""
    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='fNV96',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='5cMQ7',
        slug='H46cb',
        abbreviation='WKSey',
        plugged='uVRz5',
        background='tcniO',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='9uupC',
        code='8M5jF',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='4WtBk',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='U339l',
        value='KUzT1',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='okE7b',
        email='AA0Gg@nkayh.com',
        num_select='EsFHP',
        last_name='0uWUG',
        first_name='4bQMI',
        date_of_birth='2025-11-15',
        place_of_birth='Hka6U',
        address='qj228NpVP01muywKavwyQ7ylCYaAIORua1BTHhzPGtLPPE1YwYMGiRWFhGOsZPsS2TOgcZrmrnyHt5A72I29UpsIbAh',
        sex='Masculin',
        martial_status='Célibataire',
        phone_number='66mdl',
        num_of_cin='b3Che',
        date_of_cin='2025-11-15',
        place_of_cin='ByQya',
        repeat_status='2',
        picture='Sokib',
        num_of_baccalaureate='bvh9f',
        center_of_baccalaureate='uL3B4',
        year_of_baccalaureate='2025-11-15',
        job='iMLmq',
        father_name='nErJk',
        father_job='VPf2x',
        mother_name='5jW0a',
        mother_job='cqZdy',
        parent_address='ZXV2RJuvTHN1RYV2gYd12Fx2rm3niH9yQLCSNbuVGg23CrTOHXn5Y8uCzwrMExVlqum9YvqIlkIhy8W5dvYEAxc1E',
        level='L1',
        mean=2.3589999785414797,
        enrollment_status='Inscrit(e)',
        imported_id='rNh0y',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=4.307237968687277,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=4,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for StudentSubscription
    student_subscription_data = schemas.StudentSubscriptionCreate(
        id_subscription=subscription.id,
        id_annual_register=annual_register.id,
    )

    student_subscription = crud.student_subscription.create(db=db, obj_in=student_subscription_data)

    # Delete record
    deleted_student_subscription = crud.student_subscription.remove(db=db, id=student_subscription.id)

    # Assertions
    assert deleted_student_subscription is not None
    assert deleted_student_subscription.id == student_subscription.id

    # Verify deletion
    assert crud.student_subscription.get(db=db, id=student_subscription.id) is None

# begin #
# ---write your code here--- #
# end #

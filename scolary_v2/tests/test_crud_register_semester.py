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
"""Tests for CRUD operations on RegisterSemester model."""


def test_create_register_semester(db: Session):
    """Test create operation for RegisterSemester."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='v1pVE',
        slug='D0txh',
        abbreviation='wFAXM',
        plugged='E72T0',
        background='4wFDR',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='vudKi',
        code='LMVWt',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='PvQhK',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='MkJis',
        value='OUXBH',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='W676Q',
        email='Cav4X@myicg.com',
        num_select='xgNB3',
        last_name='h4MqN',
        first_name='NAh3A',
        date_of_birth='2025-11-15',
        place_of_birth='rWqai',
        address='JUCcj5UKfKXPQSrjZFJ4pndmlZ3e',
        sex='Masculin',
        martial_status='Célibataire',
        phone_number='FtdJX',
        num_of_cin='4Ey3N',
        date_of_cin='2025-11-15',
        place_of_cin='uVsof',
        repeat_status='1',
        picture='djVrH',
        num_of_baccalaureate='iJWyL',
        center_of_baccalaureate='VDPTh',
        year_of_baccalaureate='2025-11-15',
        job='Zu7yk',
        father_name='1YCNt',
        father_job='LWAy2',
        mother_name='37Eht',
        mother_job='35nTw',
        parent_address='Fk5duxp9IKxdnHmKDDxoQUV6Bf',
        level='L2',
        mean=4.796856500058565,
        enrollment_status='Sélectionné(e)',
        imported_id='fVdqD',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=5.135636683012923,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=16,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='wN0eI',
        abbreviation='Z62vP',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='daSUt',
        repeat_status='0',
        id_journey=journey.id,
        imported_id='PjsUO',
        is_valid=True,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    # Assertions
    assert register_semester.id is not None
    assert register_semester.id_annual_register == register_semester_data.id_annual_register
    assert register_semester.semester == register_semester_data.semester
    assert register_semester.repeat_status == register_semester_data.repeat_status
    assert register_semester.id_journey == register_semester_data.id_journey
    assert register_semester.imported_id == register_semester_data.imported_id
    assert register_semester.is_valid == register_semester_data.is_valid


def test_update_register_semester(db: Session):
    """Test update operation for RegisterSemester."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='Ns4jZ',
        slug='8VM3Z',
        abbreviation='Arr1o',
        plugged='YHt60',
        background='ZzrA3',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='K50sx',
        code='UxQMF',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='2j2Ba',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='q9lhp',
        value='mEGXh',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='9Gti9',
        email='lBZfq@losmo.com',
        num_select='aTcux',
        last_name='3uhZr',
        first_name='oFsqV',
        date_of_birth='2025-11-15',
        place_of_birth='cDgH8',
        address='4mFgALWJcSH7f2Vm90R',
        sex='Féminin',
        martial_status='Veuf/Veuve',
        phone_number='z4GoM',
        num_of_cin='SIiTq',
        date_of_cin='2025-11-15',
        place_of_cin='TsmIt',
        repeat_status='1',
        picture='xQAyC',
        num_of_baccalaureate='Kkfjd',
        center_of_baccalaureate='vq728',
        year_of_baccalaureate='2025-11-15',
        job='qA7lx',
        father_name='wb0DJ',
        father_job='TjQmH',
        mother_name='W1mGc',
        mother_job='y5Zwq',
        parent_address='UJsJE4mESz5ls8JEPTBakGiQPZPxGhUJBD6MZ8',
        level='M2',
        mean=1.5518896006897185,
        enrollment_status='En attente',
        imported_id='QXXMz',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=5.213924996731265,
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

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='IvhOS',
        abbreviation='7QSE6',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='63k0j',
        repeat_status='1',
        id_journey=journey.id,
        imported_id='mkqf7',
        is_valid=True,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    # Precompute enum values for update
    enum_values_map = {}
    enum_values_map['repeat_status'] = ['0', '1', '2']

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
    semester_value = register_semester.semester
    repeat_status_value = register_semester.repeat_status
    imported_id_value = register_semester.imported_id
    is_valid_value = register_semester.is_valid
    update_data = schemas.RegisterSemesterUpdate(**{
        k: _updated_value(k, v)
        for k, v in register_semester_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_register_semester = crud.register_semester.update(
        db=db, db_obj=register_semester, obj_in=update_data
    )

    # Assertions
    assert updated_register_semester.id == register_semester.id
    assert updated_register_semester.semester != semester_value
    assert updated_register_semester.repeat_status != repeat_status_value
    assert updated_register_semester.imported_id != imported_id_value
    assert updated_register_semester.is_valid != is_valid_value


def test_get_register_semester(db: Session):
    """Test get operation for RegisterSemester."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='EhajI',
        slug='vyKNW',
        abbreviation='uJmr7',
        plugged='tbLzR',
        background='qSzep',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='ODu6z',
        code='Oht8s',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='50fWG',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='yXXK2',
        value='lZhh9',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='Omfb3',
        email='ZhyD7@o3bh8.com',
        num_select='kszmg',
        last_name='MKZSR',
        first_name='VZOlH',
        date_of_birth='2025-11-15',
        place_of_birth='67PGV',
        address='rf1XI5cxXqVZcRU4d6AiscboSVtRilQZJ0Z3UwlOUDyWUv74v97I5joMrhbenhor9fSxWJPMk0',
        sex='Féminin',
        martial_status='Divorcé(e)',
        phone_number='Ss0fd',
        num_of_cin='WvhzN',
        date_of_cin='2025-11-15',
        place_of_cin='t09Ue',
        repeat_status='0',
        picture='FqgJ1',
        num_of_baccalaureate='lKXxk',
        center_of_baccalaureate='a91Oz',
        year_of_baccalaureate='2025-11-15',
        job='bPbgo',
        father_name='Dybqg',
        father_job='mv6s4',
        mother_name='oWv64',
        mother_job='AGtxi',
        parent_address='MyP',
        level='L3',
        mean=3.150240280389133,
        enrollment_status='Inscrit(e)',
        imported_id='SQNVw',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=4.707795483917968,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=3,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='N7K6u',
        abbreviation='hKPzR',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='fQg0s',
        repeat_status='2',
        id_journey=journey.id,
        imported_id='ZmgZT',
        is_valid=True,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    # Get all records
    records = crud.register_semester.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == register_semester.id for r in records)


def test_get_by_id_register_semester(db: Session):
    """Test get_by_id operation for RegisterSemester."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='REbyM',
        slug='3r9rG',
        abbreviation='o9LBC',
        plugged='AjARD',
        background='dlh3K',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='oexXI',
        code='Frr4z',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='87wbm',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='5zZGI',
        value='nqe3Y',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='hYUQP',
        email='s2jZF@5vxxa.com',
        num_select='79Zv6',
        last_name='UqB4n',
        first_name='oxLwM',
        date_of_birth='2025-11-15',
        place_of_birth='Wreqr',
        address='zhLqX7Ri8BdGff5m7f9MmFItgeX2unWCL2XTJigaFX8rWHY7RH0kseEXfl02E0QZxMM',
        sex='Masculin',
        martial_status='Marié(e)',
        phone_number='XRda1',
        num_of_cin='izLys',
        date_of_cin='2025-11-15',
        place_of_cin='J4BRM',
        repeat_status='2',
        picture='xTnHD',
        num_of_baccalaureate='BYidk',
        center_of_baccalaureate='dp5J1',
        year_of_baccalaureate='2025-11-15',
        job='jvwyI',
        father_name='mWy66',
        father_job='ixFR7',
        mother_name='9vE6T',
        mother_job='ef4DX',
        parent_address='52Lro8ebg0ZFBzPzYY9UYO5HUXsXLSZBbrzkoNffvBTDFmD3RrhzgjoXXvGdKPA7SO10',
        level='M1',
        mean=4.616328905586313,
        enrollment_status='Inscrit(e)',
        imported_id='LE5NL',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=4.976539809678362,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=10,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='zW6ZI',
        abbreviation='qdLB3',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='ykIop',
        repeat_status='2',
        id_journey=journey.id,
        imported_id='EdwFc',
        is_valid=False,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    # Get by ID
    retrieved_register_semester = crud.register_semester.get(db=db, id=register_semester.id)

    # Assertions
    assert retrieved_register_semester is not None
    assert retrieved_register_semester.id == register_semester.id
    assert retrieved_register_semester.id_annual_register == register_semester.id_annual_register
    assert retrieved_register_semester.semester == register_semester.semester
    assert retrieved_register_semester.repeat_status == register_semester.repeat_status
    assert retrieved_register_semester.id_journey == register_semester.id_journey
    assert retrieved_register_semester.imported_id == register_semester.imported_id
    assert retrieved_register_semester.is_valid == register_semester.is_valid


def test_delete_register_semester(db: Session):
    """Test delete operation for RegisterSemester."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='o2odu',
        slug='6GoL8',
        abbreviation='bSSJV',
        plugged='21B9r',
        background='8mdIE',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='pkMOe',
        code='NtZLR',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='9cQOH',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='3wyIg',
        value='aVjuP',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='p7CvD',
        email='jIXEW@phqc7.com',
        num_select='sI6Qj',
        last_name='PQU6R',
        first_name='mBgQl',
        date_of_birth='2025-11-15',
        place_of_birth='qCERo',
        address='EtEW06H7qi2GBX7UDPCfyw5eNImTTX9trAqeK2pfffBX',
        sex='Féminin',
        martial_status='Divorcé(e)',
        phone_number='PnowD',
        num_of_cin='14LXQ',
        date_of_cin='2025-11-15',
        place_of_cin='tg4Jy',
        repeat_status='0',
        picture='RSWWt',
        num_of_baccalaureate='nZITI',
        center_of_baccalaureate='TsylI',
        year_of_baccalaureate='2025-11-15',
        job='sX4Yn',
        father_name='F3TCG',
        father_job='ROO1K',
        mother_name='czG55',
        mother_job='xwOKN',
        parent_address='hRO8COd9Hg',
        level='L2',
        mean=4.3280606127494785,
        enrollment_status='Inscrit(e)',
        imported_id='ZBYFR',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=3.2825326262591408,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=19,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='yAG3k',
        abbreviation='xv8ER',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='xZYBW',
        repeat_status='1',
        id_journey=journey.id,
        imported_id='CeGCJ',
        is_valid=False,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    # Delete record
    deleted_register_semester = crud.register_semester.remove(db=db, id=register_semester.id)

    # Assertions
    assert deleted_register_semester is not None
    assert deleted_register_semester.id == register_semester.id

    # Verify deletion
    assert crud.register_semester.get(db=db, id=register_semester.id) is None

# begin #
# ---write your code here--- #
# end #

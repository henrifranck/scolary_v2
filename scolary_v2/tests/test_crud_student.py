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
"""Tests for CRUD operations on Student model."""


def test_create_student(db: Session):
    """Test create operation for Student."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='0Dpga',
        slug='DPhx5',
        abbreviation='j2Sso',
        plugged='F1bgE',
        background='rV3S0',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='RogtE',
        code='q2dBU',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='mnXVV',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='a6SKt',
        value='UMKe2',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='wQ1Er',
        email='0UVdS@zpeps.com',
        num_select='YKJQn',
        last_name='tNwgv',
        first_name='A2ofx',
        date_of_birth='2025-11-15',
        place_of_birth='BNByy',
        address='av48vIsfNKBXOEI4Yp8KwVPb1D23CHkufPoozBC2vMJTHXAI68pHXXKeZ7V91XKLgXii31lI6X1E8Ec5Kqi6JeAO7sLQVhjTx0s',
        sex='Féminin',
        martial_status='Célibataire',
        phone_number='UtQnY',
        num_of_cin='NNCpH',
        date_of_cin='2025-11-15',
        place_of_cin='srk0b',
        repeat_status='1',
        picture='bHoqx',
        num_of_baccalaureate='PAb5E',
        center_of_baccalaureate='mv9Ma',
        year_of_baccalaureate='2025-11-15',
        job='J3qXm',
        father_name='rOYbw',
        father_job='FZn2i',
        mother_name='HILYO',
        mother_job='tUaXJ',
        parent_address='MMqzCTTXnqySy3diwulJmwx7X7JhnsLXxvv67ghNcEfqGYq6Go2ZqGz3iVNt56cbuhTDO3LCuwWfflKwGtTZP6FEim85U',
        level='L1',
        mean=3.1512962275098753,
        enrollment_status='Inscrit(e)',
        imported_id='GCqPj',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Assertions
    assert student.id is not None
    assert student.num_carte == student_data.num_carte
    assert student.email == student_data.email
    assert student.num_select == student_data.num_select
    assert student.last_name == student_data.last_name
    assert student.first_name == student_data.first_name
    assert student.date_of_birth == student_data.date_of_birth
    assert student.place_of_birth == student_data.place_of_birth
    assert student.address == student_data.address
    assert student.sex == student_data.sex
    assert student.martial_status == student_data.martial_status
    assert student.phone_number == student_data.phone_number
    assert student.num_of_cin == student_data.num_of_cin
    assert student.date_of_cin == student_data.date_of_cin
    assert student.place_of_cin == student_data.place_of_cin
    assert student.repeat_status == student_data.repeat_status
    assert student.picture == student_data.picture
    assert student.num_of_baccalaureate == student_data.num_of_baccalaureate
    assert student.center_of_baccalaureate == student_data.center_of_baccalaureate
    assert student.year_of_baccalaureate == student_data.year_of_baccalaureate
    assert student.job == student_data.job
    assert student.father_name == student_data.father_name
    assert student.father_job == student_data.father_job
    assert student.mother_name == student_data.mother_name
    assert student.mother_job == student_data.mother_job
    assert student.parent_address == student_data.parent_address
    assert student.level == student_data.level
    assert student.mean == student_data.mean
    assert student.enrollment_status == student_data.enrollment_status
    assert student.imported_id == student_data.imported_id
    assert student.id_mention == student_data.id_mention
    assert student.id_enter_year == student_data.id_enter_year
    assert student.id_nationality == student_data.id_nationality
    assert student.id_baccalaureate_series == student_data.id_baccalaureate_series


def test_update_student(db: Session):
    """Test update operation for Student."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='lEq5t',
        slug='j68MG',
        abbreviation='wK9ed',
        plugged='EmuW2',
        background='Mgcv4',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='wIn0A',
        code='etz52',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='JmBAk',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='Syif6',
        value='oACsA',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='pXJtk',
        email='OW7Xj@urp2k.com',
        num_select='B8rHN',
        last_name='2ioPW',
        first_name='eIUsI',
        date_of_birth='2025-11-15',
        place_of_birth='K44zQ',
        address='P8SS4w7krJJ8wuIYMMTB1vpobH0Rwt4obkMCmmsJyiP23ZvdhOkSuERiQAc1Tu7ewcPredD3Y',
        sex='Féminin',
        martial_status='Divorcé(e)',
        phone_number='6tWji',
        num_of_cin='htqBx',
        date_of_cin='2025-11-15',
        place_of_cin='lg2DB',
        repeat_status='2',
        picture='PJXjJ',
        num_of_baccalaureate='Dr6X1',
        center_of_baccalaureate='Vnfgt',
        year_of_baccalaureate='2025-11-15',
        job='G8Hee',
        father_name='HzyLO',
        father_job='jprSP',
        mother_name='uDP0Q',
        mother_job='vAXRN',
        parent_address='9zcTP0gKILerleukliD8FyUWXUW8uPi9iMfi5kUL58zMbJGt9kLbYe5MFamw0o3DWw5l2FSDMXXmtca',
        level='M2',
        mean=3.2415434184446226,
        enrollment_status='En attente',
        imported_id='BVF3J',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Precompute enum values for update
    enum_values_map = {}
    enum_values_map['sex'] = ['Masculin', 'Féminin']
    enum_values_map['martial_status'] = ['Célibataire', 'Marié(e)', 'Divorcé(e)', 'Veuf/Veuve']
    enum_values_map['repeat_status'] = ['0', '1', '2']
    enum_values_map['level'] = ['L1', 'L2', 'L3', 'M1', 'M2']
    enum_values_map['enrollment_status'] = ['En attente', 'Sélectionné(e)', 'Inscrit(e)', 'ancien(ne)']

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
        if k in ['date_of_birth', 'date_of_cin', 'year_of_baccalaureate'] and isinstance(v, str):
            return (date.fromisoformat(v) + timedelta(days=1)).isoformat()
        if k in ['date_of_birth', 'date_of_cin', 'year_of_baccalaureate'] and isinstance(v, date):
            return v + timedelta(days=1)

        # time +1 hour
        if k in [] and isinstance(v, str):
            return (datetime.strptime(v, '%H:%M:%S') + timedelta(hours=1)).time().strftime('%H:%M:%S')
        if k in [] and isinstance(v, time):
            return (datetime.combine(date.today(), v) + timedelta(hours=1)).time()

        # fallback -> prefix 'updated_'
        return f'updated_{v}'

    # Update data
    num_carte_value = student.num_carte
    email_value = student.email
    num_select_value = student.num_select
    last_name_value = student.last_name
    first_name_value = student.first_name
    date_of_birth_value = student.date_of_birth
    place_of_birth_value = student.place_of_birth
    address_value = student.address
    sex_value = student.sex
    martial_status_value = student.martial_status
    phone_number_value = student.phone_number
    num_of_cin_value = student.num_of_cin
    date_of_cin_value = student.date_of_cin
    place_of_cin_value = student.place_of_cin
    repeat_status_value = student.repeat_status
    picture_value = student.picture
    num_of_baccalaureate_value = student.num_of_baccalaureate
    center_of_baccalaureate_value = student.center_of_baccalaureate
    year_of_baccalaureate_value = student.year_of_baccalaureate
    job_value = student.job
    father_name_value = student.father_name
    father_job_value = student.father_job
    mother_name_value = student.mother_name
    mother_job_value = student.mother_job
    parent_address_value = student.parent_address
    level_value = student.level
    mean_value = student.mean
    enrollment_status_value = student.enrollment_status
    imported_id_value = student.imported_id
    update_data = schemas.StudentUpdate(**{
        k: _updated_value(k, v)
        for k, v in student_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_student = crud.student.update(
        db=db, db_obj=student, obj_in=update_data
    )

    # Assertions
    assert updated_student.id == student.id
    assert updated_student.num_carte != num_carte_value
    assert updated_student.email != email_value
    assert updated_student.num_select != num_select_value
    assert updated_student.last_name != last_name_value
    assert updated_student.first_name != first_name_value
    assert updated_student.date_of_birth != date_of_birth_value
    assert updated_student.place_of_birth != place_of_birth_value
    assert updated_student.address != address_value
    assert updated_student.sex != sex_value
    assert updated_student.martial_status != martial_status_value
    assert updated_student.phone_number != phone_number_value
    assert updated_student.num_of_cin != num_of_cin_value
    assert updated_student.date_of_cin != date_of_cin_value
    assert updated_student.place_of_cin != place_of_cin_value
    assert updated_student.repeat_status != repeat_status_value
    assert updated_student.picture != picture_value
    assert updated_student.num_of_baccalaureate != num_of_baccalaureate_value
    assert updated_student.center_of_baccalaureate != center_of_baccalaureate_value
    assert updated_student.year_of_baccalaureate != year_of_baccalaureate_value
    assert updated_student.job != job_value
    assert updated_student.father_name != father_name_value
    assert updated_student.father_job != father_job_value
    assert updated_student.mother_name != mother_name_value
    assert updated_student.mother_job != mother_job_value
    assert updated_student.parent_address != parent_address_value
    assert updated_student.level != level_value
    assert updated_student.mean != mean_value
    assert updated_student.enrollment_status != enrollment_status_value
    assert updated_student.imported_id != imported_id_value


def test_get_student(db: Session):
    """Test get operation for Student."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='ZhaUC',
        slug='IVSbD',
        abbreviation='wxzAq',
        plugged='kN4Ig',
        background='LfeEM',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='2CHk5',
        code='C19tk',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='6B69T',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='VEs0d',
        value='vQ6KR',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='x1P7o',
        email='o22SH@yeatv.com',
        num_select='emdGX',
        last_name='C01lb',
        first_name='ZhRKY',
        date_of_birth='2025-11-15',
        place_of_birth='2B8iF',
        address='sGwiTFZT6p0jRXLGZjRm0LB53Gd7EaqGuYH0vmE3PYItcf6fZ9i6a15OYDF7q7PUGCjnF6GQDHYKsXQeNWRY9uzE7CEzfVCG72iq',
        sex='Masculin',
        martial_status='Marié(e)',
        phone_number='ZCj2n',
        num_of_cin='1kgBD',
        date_of_cin='2025-11-15',
        place_of_cin='KYnoF',
        repeat_status='1',
        picture='8jWqY',
        num_of_baccalaureate='BTVWN',
        center_of_baccalaureate='AZBug',
        year_of_baccalaureate='2025-11-15',
        job='Lkf1S',
        father_name='3L0u6',
        father_job='Yc4i7',
        mother_name='3z1jt',
        mother_job='9kBXh',
        parent_address='NHzWAnbTwnzaLEQ9j4bbJ',
        level='M2',
        mean=2.079384828267035,
        enrollment_status='Sélectionné(e)',
        imported_id='JZ8fD',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Get all records
    records = crud.student.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == student.id for r in records)


def test_get_by_id_student(db: Session):
    """Test get_by_id operation for Student."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='Fgbfr',
        slug='ou64d',
        abbreviation='dJNtl',
        plugged='9MFld',
        background='N63Dr',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='ZLLHb',
        code='LR8ZM',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='eXZpS',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='YSDl7',
        value='6DIXF',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='4DsGl',
        email='LwD9f@iznqs.com',
        num_select='Hf94i',
        last_name='LKeoK',
        first_name='QHhCg',
        date_of_birth='2025-11-15',
        place_of_birth='3RuEq',
        address='DkLVekFFzJE6FWkoW2DsEr5SKnst14qR2eO9oWC30amJh02kGUxdnI8MfwnMm8v5of3mE7UBUxJegLJ5mitqDfwQLsBf3wSO',
        sex='Masculin',
        martial_status='Célibataire',
        phone_number='KRo0w',
        num_of_cin='6PhRL',
        date_of_cin='2025-11-15',
        place_of_cin='WWLQO',
        repeat_status='0',
        picture='qKoeu',
        num_of_baccalaureate='KJBLR',
        center_of_baccalaureate='Ei8J5',
        year_of_baccalaureate='2025-11-15',
        job='ZOuxK',
        father_name='KjSGE',
        father_job='DALHU',
        mother_name='XD3zE',
        mother_job='NqVJE',
        parent_address='XOJ2M4fbT3FM7FmHtf27ucvWZch1oSQFMZ',
        level='L2',
        mean=5.0120639520004,
        enrollment_status='En attente',
        imported_id='oUZJ5',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Get by ID
    retrieved_student = crud.student.get(db=db, id=student.id)

    # Assertions
    assert retrieved_student is not None
    assert retrieved_student.id == student.id
    assert retrieved_student.num_carte == student.num_carte
    assert retrieved_student.email == student.email
    assert retrieved_student.num_select == student.num_select
    assert retrieved_student.last_name == student.last_name
    assert retrieved_student.first_name == student.first_name
    assert retrieved_student.date_of_birth == student.date_of_birth
    assert retrieved_student.place_of_birth == student.place_of_birth
    assert retrieved_student.address == student.address
    assert retrieved_student.sex == student.sex
    assert retrieved_student.martial_status == student.martial_status
    assert retrieved_student.phone_number == student.phone_number
    assert retrieved_student.num_of_cin == student.num_of_cin
    assert retrieved_student.date_of_cin == student.date_of_cin
    assert retrieved_student.place_of_cin == student.place_of_cin
    assert retrieved_student.repeat_status == student.repeat_status
    assert retrieved_student.picture == student.picture
    assert retrieved_student.num_of_baccalaureate == student.num_of_baccalaureate
    assert retrieved_student.center_of_baccalaureate == student.center_of_baccalaureate
    assert retrieved_student.year_of_baccalaureate == student.year_of_baccalaureate
    assert retrieved_student.job == student.job
    assert retrieved_student.father_name == student.father_name
    assert retrieved_student.father_job == student.father_job
    assert retrieved_student.mother_name == student.mother_name
    assert retrieved_student.mother_job == student.mother_job
    assert retrieved_student.parent_address == student.parent_address
    assert retrieved_student.level == student.level
    assert retrieved_student.mean == student.mean
    assert retrieved_student.enrollment_status == student.enrollment_status
    assert retrieved_student.imported_id == student.imported_id
    assert retrieved_student.id_mention == student.id_mention
    assert retrieved_student.id_enter_year == student.id_enter_year
    assert retrieved_student.id_nationality == student.id_nationality
    assert retrieved_student.id_baccalaureate_series == student.id_baccalaureate_series


def test_delete_student(db: Session):
    """Test delete operation for Student."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='VOi9u',
        slug='pJ3qv',
        abbreviation='xZ1gH',
        plugged='2MD5m',
        background='OdcZD',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='KItre',
        code='y93eU',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='HrpDB',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='QNZhF',
        value='vYOw8',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='2dwYR',
        email='rFtHJ@ud33k.com',
        num_select='23gAv',
        last_name='g0Gqy',
        first_name='HVM7a',
        date_of_birth='2025-11-15',
        place_of_birth='oUubs',
        address='sJnODdf1pJlnazWBPFU0oCgGl2wq92JiVqc530sLljQLR3cXfYwuAWBLGDTdH1OSjZisrsddh5OwCgdcod046j13kqOO3nhP5J',
        sex='Féminin',
        martial_status='Célibataire',
        phone_number='2baWp',
        num_of_cin='VsF9K',
        date_of_cin='2025-11-15',
        place_of_cin='nXCMa',
        repeat_status='0',
        picture='cAojS',
        num_of_baccalaureate='BeGRy',
        center_of_baccalaureate='4EXgV',
        year_of_baccalaureate='2025-11-15',
        job='UPqES',
        father_name='3yPKZ',
        father_job='DASrE',
        mother_name='sVsMA',
        mother_job='LFQip',
        parent_address='EzvIiyji0rYq4Z7kMPajvfqN2ZsaDuYnRv8X5aYWIsNHPwAoi76UEbpQJCDaFfew1tuV3coUyK',
        level='L2',
        mean=2.9768066214630986,
        enrollment_status='Inscrit(e)',
        imported_id='H8g9A',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Delete record
    deleted_student = crud.student.remove(db=db, id=student.id)

    # Assertions
    assert deleted_student is not None
    assert deleted_student.id == student.id

    # Verify deletion
    assert crud.student.get(db=db, id=student.id) is None

# begin #
# ---write your code here--- #
# end #

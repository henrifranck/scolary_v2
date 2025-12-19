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
"""Tests for CRUD operations on AnnualRegister model."""


def test_create_annual_register(db: Session):
    """Test create operation for AnnualRegister."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='Oqhw4',
        slug='mpaSo',
        abbreviation='heSqR',
        plugged='uCAn0',
        background='JSFKj',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='ZBNQF',
        code='lT1gY',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='BATh7',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='M9I3t',
        value='3PoN3',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='o2ena',
        email='810F2@c6t2n.com',
        num_select='c8rR4',
        last_name='MpnXj',
        first_name='lfe68',
        date_of_birth='2025-11-15',
        place_of_birth='ZYfYX',
        address='BoUbSX6t6U2iCVHK242TwfP6ILf55GGu1e3TDL4VpNf4Mgnkn62hwmXhaaNhlZscqRFN7FtO3capeZfFyfNAyh',
        sex='Féminin',
        martial_status='Veuf/Veuve',
        phone_number='mPqRC',
        num_of_cin='AMt66',
        date_of_cin='2025-11-15',
        place_of_cin='Ubf3K',
        repeat_status='2',
        picture='NLdx6',
        num_of_baccalaureate='sWnkN',
        center_of_baccalaureate='CpMEY',
        year_of_baccalaureate='2025-11-15',
        job='KOnzO',
        father_name='N4mLt',
        father_job='rIlZZ',
        mother_name='y7yNP',
        mother_job='fpk0h',
        parent_address='G2ZcdgF8g35kh78312KuIwonWZdnBIEetNQfhpCxz3j3nEwjSy',
        level='M1',
        mean=2.2517662829549168,
        enrollment_status='En attente',
        imported_id='s802X',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=3.1737867670031306,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=13,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Assertions
    assert annual_register.id is not None
    assert annual_register.num_carte == annual_register_data.num_carte
    assert annual_register.id_academic_year == annual_register_data.id_academic_year
    assert annual_register.semester_count == annual_register_data.semester_count
    assert annual_register.id_enrollment_fee == annual_register_data.id_enrollment_fee


def test_update_annual_register(db: Session):
    """Test update operation for AnnualRegister."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='XJ9bz',
        slug='UDngU',
        abbreviation='nAI1w',
        plugged='7SmFR',
        background='5NuLS',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='tlJXB',
        code='uUsFW',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='hHcwV',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='3Nu9F',
        value='kgUav',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='Mt1TF',
        email='7MI2h@uyvga.com',
        num_select='ZeYHj',
        last_name='5foXN',
        first_name='YH71d',
        date_of_birth='2025-11-15',
        place_of_birth='ctht6',
        address='doS5j3X2uDUNTaPCo6vhRMJ2aP6to9lPRAXnFKwDgYf7PCa8F4TDq5oFICyjxEhykNGfLEsatPowqNfPikLDCXuVBhUK5r',
        sex='Masculin',
        martial_status='Divorcé(e)',
        phone_number='4zFkP',
        num_of_cin='30Qdh',
        date_of_cin='2025-11-15',
        place_of_cin='tYrpt',
        repeat_status='0',
        picture='8v89y',
        num_of_baccalaureate='mmsGq',
        center_of_baccalaureate='IZGAV',
        year_of_baccalaureate='2025-11-15',
        job='Afm4y',
        father_name='Hy8u6',
        father_job='SkhlC',
        mother_name='LJP5w',
        mother_job='Bql2A',
        parent_address='6xylV5FbH664Ym67BIbha4yZMSRAclEVs6X',
        level='L1',
        mean=2.8985553202785046,
        enrollment_status='Inscrit(e)',
        imported_id='L1xRW',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=2.8965450258001226,
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
    semester_count_value = annual_register.semester_count
    update_data = schemas.AnnualRegisterUpdate(**{
        k: _updated_value(k, v)
        for k, v in annual_register_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_annual_register = crud.annual_register.update(
        db=db, db_obj=annual_register, obj_in=update_data
    )

    # Assertions
    assert updated_annual_register.id == annual_register.id
    assert updated_annual_register.semester_count != semester_count_value


def test_get_annual_register(db: Session):
    """Test get operation for AnnualRegister."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='AnG5H',
        slug='NtC9r',
        abbreviation='CZlHS',
        plugged='HagSa',
        background='xi6RT',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='XFuLs',
        code='So1HQ',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='d7r9v',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='sSmJ5',
        value='hL0cf',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='mvAWF',
        email='2mA5q@s2lu7.com',
        num_select='WSHyA',
        last_name='we58t',
        first_name='V6U7C',
        date_of_birth='2025-11-15',
        place_of_birth='jRn3J',
        address='2hpnAKBDWlygts6qC3q9EvOfeoYqAcDBlHYSsscEsI9WJr7WhtjIJ7ASPDXlsmd6Ado8YaXDQu5gKN',
        sex='Féminin',
        martial_status='Marié(e)',
        phone_number='BO6Mj',
        num_of_cin='HhPPC',
        date_of_cin='2025-11-15',
        place_of_cin='zasPH',
        repeat_status='1',
        picture='qzx7V',
        num_of_baccalaureate='gsUpi',
        center_of_baccalaureate='0seik',
        year_of_baccalaureate='2025-11-15',
        job='K07PY',
        father_name='SHMMc',
        father_job='wdSNS',
        mother_name='CJJDW',
        mother_job='Id55L',
        parent_address='1A55NJWWwzCs40xdDR7cD7RHBoa0CEnmsYXS9nY3yr3VMjYweIsr5GVqTe2vnON89AqINQmDBRcHDvIRZ',
        level='L1',
        mean=5.389616570384422,
        enrollment_status='ancien(ne)',
        imported_id='jiGQU',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=3.8895558675355217,
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

    # Get all records
    records = crud.annual_register.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == annual_register.id for r in records)


def test_get_by_id_annual_register(db: Session):
    """Test get_by_id operation for AnnualRegister."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='uHwzt',
        slug='GhE38',
        abbreviation='BeF8T',
        plugged='UiItX',
        background='cbsmX',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='Xyqcb',
        code='V2Iwy',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='USULI',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='CY9VO',
        value='H4fiG',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='tIPcu',
        email='bytvt@mazj8.com',
        num_select='I0MiT',
        last_name='ez2qR',
        first_name='6L6eK',
        date_of_birth='2025-11-15',
        place_of_birth='ie5kF',
        address='x4dUZ3VxBMauTXFeLWxQgAEVb9joCit3hYkIB16QSZtwU1nwwwAk2cc0qAi',
        sex='Masculin',
        martial_status='Marié(e)',
        phone_number='SPO5A',
        num_of_cin='zlcx0',
        date_of_cin='2025-11-15',
        place_of_cin='IH8Rw',
        repeat_status='1',
        picture='FPahy',
        num_of_baccalaureate='bcBPx',
        center_of_baccalaureate='5h2nw',
        year_of_baccalaureate='2025-11-15',
        job='jAKo7',
        father_name='qG03d',
        father_job='U6AyG',
        mother_name='FTn65',
        mother_job='iZX9G',
        parent_address='d',
        level='L3',
        mean=4.874015577159204,
        enrollment_status='En attente',
        imported_id='S3sTF',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='1',
        price=4.361999024447295,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=8,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Get by ID
    retrieved_annual_register = crud.annual_register.get(db=db, id=annual_register.id)

    # Assertions
    assert retrieved_annual_register is not None
    assert retrieved_annual_register.id == annual_register.id
    assert retrieved_annual_register.num_carte == annual_register.num_carte
    assert retrieved_annual_register.id_academic_year == annual_register.id_academic_year
    assert retrieved_annual_register.semester_count == annual_register.semester_count
    assert retrieved_annual_register.id_enrollment_fee == annual_register.id_enrollment_fee


def test_delete_annual_register(db: Session):
    """Test delete operation for AnnualRegister."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='OC3IK',
        slug='08yB5',
        abbreviation='qqt5l',
        plugged='90IHh',
        background='QxVZP',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='8YlrU',
        code='oPTkE',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='S4cxM',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='5cEqc',
        value='fi7XF',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='mJ1m0',
        email='tDmFE@fpzib.com',
        num_select='eQtpo',
        last_name='BzmTW',
        first_name='02eJL',
        date_of_birth='2025-11-15',
        place_of_birth='XNE7y',
        address='MsIoXmmJUeSQ0SlAfsYcINFtHGG4Ij2lejbuyUIV3Hn9BtHqOUBazF2NtuNs0WwSACw',
        sex='Masculin',
        martial_status='Veuf/Veuve',
        phone_number='ljG0e',
        num_of_cin='EUpRK',
        date_of_cin='2025-11-15',
        place_of_cin='hKWqJ',
        repeat_status='0',
        picture='2IpD3',
        num_of_baccalaureate='GASK2',
        center_of_baccalaureate='1akZl',
        year_of_baccalaureate='2025-11-15',
        job='OwpY3',
        father_name='eq4n7',
        father_job='fSN5v',
        mother_name='9nCjD',
        mother_job='l7eQX',
        parent_address='eorQZtajnyuXdNCx6ara7G9b7',
        level='M2',
        mean=2.7350431819952963,
        enrollment_status='ancien(ne)',
        imported_id='d1Hr0',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='1',
        price=2.7183226511875374,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=2,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Delete record
    deleted_annual_register = crud.annual_register.remove(db=db, id=annual_register.id)

    # Assertions
    assert deleted_annual_register is not None
    assert deleted_annual_register.id == annual_register.id

    # Verify deletion
    assert crud.annual_register.get(db=db, id=annual_register.id) is None

# begin #
# ---write your code here--- #
# end #

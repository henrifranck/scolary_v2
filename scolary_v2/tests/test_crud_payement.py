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
"""Tests for CRUD operations on Payement model."""


def test_create_payement(db: Session):
    """Test create operation for Payement."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='y86eK',
        slug='FD08X',
        abbreviation='G8UCS',
        plugged='i4TLH',
        background='ElDFb',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='sFmJq',
        code='EhHeO',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='Kv66O',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='AxMOv',
        value='5awzm',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='X46sO',
        email='7qTWQ@gmxc8.com',
        num_select='XyQmS',
        last_name='jLIeC',
        first_name='cfw6K',
        date_of_birth='2025-11-15',
        place_of_birth='czznw',
        address='tSpZbT4B5iLy5VJP3G2DHNWFJ8vfY2rNQDHwmOM9Bg2xLNWRTBJPFSCHZ',
        sex='Féminin',
        martial_status='Veuf/Veuve',
        phone_number='4NoIu',
        num_of_cin='WeJKj',
        date_of_cin='2025-11-15',
        place_of_cin='n0eeU',
        repeat_status='0',
        picture='iqOLz',
        num_of_baccalaureate='I8OEr',
        center_of_baccalaureate='UONFI',
        year_of_baccalaureate='2025-11-15',
        job='ypKyB',
        father_name='woZ0X',
        father_job='c57Xb',
        mother_name='zetQp',
        mother_job='u6EpZ',
        parent_address='czaIUpP2Ir9akZAcwDk9j2nxzobUA',
        level='L3',
        mean=3.974132588150625,
        enrollment_status='Inscrit(e)',
        imported_id='IEZ6x',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=3.606685835038129,
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

    # Test data for Payement
    payement_data = schemas.PayementCreate(
        id_annual_register=annual_register.id,
        payed=4.697861906051045,
        num_receipt='vstJl',
        date_receipt='2025-11-15',
    )

    payement = crud.payement.create(db=db, obj_in=payement_data)

    # Assertions
    assert payement.id is not None
    assert payement.id_annual_register == payement_data.id_annual_register
    assert payement.payed == payement_data.payed
    assert payement.num_receipt == payement_data.num_receipt
    assert payement.date_receipt == payement_data.date_receipt


def test_update_payement(db: Session):
    """Test update operation for Payement."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='slwKN',
        slug='a3QeM',
        abbreviation='q4Nps',
        plugged='2APb3',
        background='uYkk1',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='crshG',
        code='DsiVd',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='FZgTi',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='ALUih',
        value='Y7uqR',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='7Qiwp',
        email='JwqPJ@voz9q.com',
        num_select='58NPa',
        last_name='xb7bD',
        first_name='JZMfE',
        date_of_birth='2025-11-15',
        place_of_birth='MFr6m',
        address='6lvMGSrm4dcIvg9frScXbLj7vBgLQigYJ56F4UdviAHIxx1VVjBp5KascIy8uLmPwO0meegOjG4c1Vw3YFjkQ6i26JEUH',
        sex='Masculin',
        martial_status='Veuf/Veuve',
        phone_number='Hc7aB',
        num_of_cin='wJ0Ze',
        date_of_cin='2025-11-15',
        place_of_cin='tQE0N',
        repeat_status='0',
        picture='nnIhp',
        num_of_baccalaureate='d2JQE',
        center_of_baccalaureate='HIo2X',
        year_of_baccalaureate='2025-11-15',
        job='M1Bxp',
        father_name='zXnPg',
        father_job='4c8ld',
        mother_name='MVw5C',
        mother_job='a5Xbs',
        parent_address='eVxPxyjG8Qe',
        level='M1',
        mean=4.665909655869996,
        enrollment_status='En attente',
        imported_id='mxrOH',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='1',
        price=5.405803759735308,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=11,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for Payement
    payement_data = schemas.PayementCreate(
        id_annual_register=annual_register.id,
        payed=4.492715566555516,
        num_receipt='Y08WS',
        date_receipt='2025-11-15',
    )

    payement = crud.payement.create(db=db, obj_in=payement_data)

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
        if k in ['date_receipt'] and isinstance(v, str):
            return (date.fromisoformat(v) + timedelta(days=1)).isoformat()
        if k in ['date_receipt'] and isinstance(v, date):
            return v + timedelta(days=1)

        # time +1 hour
        if k in [] and isinstance(v, str):
            return (datetime.strptime(v, '%H:%M:%S') + timedelta(hours=1)).time().strftime('%H:%M:%S')
        if k in [] and isinstance(v, time):
            return (datetime.combine(date.today(), v) + timedelta(hours=1)).time()

        # fallback -> prefix 'updated_'
        return f'updated_{v}'

    # Update data
    payed_value = payement.payed
    num_receipt_value = payement.num_receipt
    date_receipt_value = payement.date_receipt
    update_data = schemas.PayementUpdate(**{
        k: _updated_value(k, v)
        for k, v in payement_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_payement = crud.payement.update(
        db=db, db_obj=payement, obj_in=update_data
    )

    # Assertions
    assert updated_payement.id == payement.id
    assert updated_payement.payed != payed_value
    assert updated_payement.num_receipt != num_receipt_value
    assert updated_payement.date_receipt != date_receipt_value


def test_get_payement(db: Session):
    """Test get operation for Payement."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='6vnN3',
        slug='AJiAY',
        abbreviation='rYHgl',
        plugged='AQGAt',
        background='dFKF3',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='nluEv',
        code='eE5iY',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='VCGuX',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='3nFKL',
        value='ot6yO',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='N6dH6',
        email='JL7KE@wfbru.com',
        num_select='hFgWi',
        last_name='bgA3W',
        first_name='EjJd6',
        date_of_birth='2025-11-15',
        place_of_birth='GAuEL',
        address='kw',
        sex='Masculin',
        martial_status='Divorcé(e)',
        phone_number='vE9Up',
        num_of_cin='z5xQz',
        date_of_cin='2025-11-15',
        place_of_cin='pPVjy',
        repeat_status='2',
        picture='u7NZo',
        num_of_baccalaureate='K8g9Q',
        center_of_baccalaureate='pnqDs',
        year_of_baccalaureate='2025-11-15',
        job='O4rTL',
        father_name='GSeCs',
        father_job='YcBGW',
        mother_name='73rEJ',
        mother_job='xSzaV',
        parent_address='fQCgIb6THwxSRpKWxUWz46UnsK29P13fpDFefiHiU6xZxuAIvFLg30hihuJ4K8MtXwzOPUseZdesTA',
        level='M1',
        mean=1.9672984823446131,
        enrollment_status='ancien(ne)',
        imported_id='Hz4et',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=3.933120576342602,
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

    # Test data for Payement
    payement_data = schemas.PayementCreate(
        id_annual_register=annual_register.id,
        payed=5.05657272628336,
        num_receipt='rBEqI',
        date_receipt='2025-11-15',
    )

    payement = crud.payement.create(db=db, obj_in=payement_data)

    # Get all records
    records = crud.payement.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == payement.id for r in records)


def test_get_by_id_payement(db: Session):
    """Test get_by_id operation for Payement."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='lSthv',
        slug='Fr0AL',
        abbreviation='tWrsI',
        plugged='khPRZ',
        background='qdcpj',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='nAhV8',
        code='An6dv',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='75aao',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='y1HIR',
        value='DEJys',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='EtfCb',
        email='hBIWy@mdqro.com',
        num_select='reLkN',
        last_name='PGs9n',
        first_name='Wy3fm',
        date_of_birth='2025-11-15',
        place_of_birth='0QOlW',
        address='QFVIVetRvJWyBz3FU1L8ugUspewc3C4riiCDdeW5Ms',
        sex='Féminin',
        martial_status='Célibataire',
        phone_number='HOa6K',
        num_of_cin='bBaxy',
        date_of_cin='2025-11-15',
        place_of_cin='BSD3K',
        repeat_status='0',
        picture='9RsfV',
        num_of_baccalaureate='qJj8N',
        center_of_baccalaureate='fm5Yy',
        year_of_baccalaureate='2025-11-15',
        job='YY9of',
        father_name='5fsV6',
        father_job='SfaRu',
        mother_name='fAbJt',
        mother_job='WVH8W',
        parent_address='mBNn9y62fApxdDRlX0G5I4d4hENowJuUMzpOx1o6oUfGsn5ERN1dO9H5CxXxXO4dHobfrg3v8',
        level='L3',
        mean=4.6533358103973805,
        enrollment_status='En attente',
        imported_id='9nDZ7',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=5.121846821177016,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=1,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for Payement
    payement_data = schemas.PayementCreate(
        id_annual_register=annual_register.id,
        payed=5.162805190433684,
        num_receipt='4iIWx',
        date_receipt='2025-11-15',
    )

    payement = crud.payement.create(db=db, obj_in=payement_data)

    # Get by ID
    retrieved_payement = crud.payement.get(db=db, id=payement.id)

    # Assertions
    assert retrieved_payement is not None
    assert retrieved_payement.id == payement.id
    assert retrieved_payement.id_annual_register == payement.id_annual_register
    assert retrieved_payement.payed == payement.payed
    assert retrieved_payement.num_receipt == payement.num_receipt
    assert retrieved_payement.date_receipt == payement.date_receipt


def test_delete_payement(db: Session):
    """Test delete operation for Payement."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='Ai1mg',
        slug='eboTa',
        abbreviation='rjkYB',
        plugged='2T6CX',
        background='hH8e0',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='ZmfSb',
        code='HlZVH',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='swCfP',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='CBw0e',
        value='4yNcb',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='90bM0',
        email='CFJYw@cjccw.com',
        num_select='821kh',
        last_name='t6uL8',
        first_name='a6aKq',
        date_of_birth='2025-11-15',
        place_of_birth='M7wdx',
        address='6bmh3wsqucHIWTD',
        sex='Masculin',
        martial_status='Marié(e)',
        phone_number='TyIX7',
        num_of_cin='N7VgO',
        date_of_cin='2025-11-15',
        place_of_cin='JKCtJ',
        repeat_status='0',
        picture='vXS1O',
        num_of_baccalaureate='UgzAD',
        center_of_baccalaureate='bcU0U',
        year_of_baccalaureate='2025-11-15',
        job='M7MjM',
        father_name='A2zte',
        father_job='ZKNut',
        mother_name='weKId',
        mother_job='P9DO6',
        parent_address='GUEnAjhT21dB3aiNipPMgSaN0j9yOXhAZAfOtKeLYqHitFUpYA',
        level='M1',
        mean=2.1979323258622743,
        enrollment_status='En attente',
        imported_id='O6uo3',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=5.241783805145127,
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

    # Test data for Payement
    payement_data = schemas.PayementCreate(
        id_annual_register=annual_register.id,
        payed=1.8322540877824212,
        num_receipt='AUbvZ',
        date_receipt='2025-11-15',
    )

    payement = crud.payement.create(db=db, obj_in=payement_data)

    # Delete record
    deleted_payement = crud.payement.remove(db=db, id=payement.id)

    # Assertions
    assert deleted_payement is not None
    assert deleted_payement.id == payement.id

    # Verify deletion
    assert crud.payement.get(db=db, id=payement.id) is None

# begin #
# ---write your code here--- #
# end #

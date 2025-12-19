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
"""Tests for CRUD operations on ResultTeachingUnit model."""


def test_create_result_teaching_unit(db: Session):
    """Test create operation for ResultTeachingUnit."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='wrl04',
        slug='cabXI',
        abbreviation='aR1nl',
        plugged='Nguat',
        background='guwJA',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='tceVr',
        code='Su76t',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='b8IrM',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='H2oc0',
        value='wPTEv',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='IbR2A',
        email='xzyr1@ufvj9.com',
        num_select='xFH3Z',
        last_name='O89sm',
        first_name='4O0Bx',
        date_of_birth='2025-11-15',
        place_of_birth='LnNK7',
        address='lsSl2M0dhVglEQo6xQw0eTv0ZfnRcd0YURtDYoQHHtZODjZiuTmJI36G7jQeMHD',
        sex='Masculin',
        martial_status='Célibataire',
        phone_number='BX0C1',
        num_of_cin='e6qNG',
        date_of_cin='2025-11-15',
        place_of_cin='XMk7X',
        repeat_status='0',
        picture='OD9t9',
        num_of_baccalaureate='bSpvs',
        center_of_baccalaureate='5rgjJ',
        year_of_baccalaureate='2025-11-15',
        job='ewXas',
        father_name='CwPtm',
        father_job='BXyvK',
        mother_name='MEikV',
        mother_job='FVyJf',
        parent_address='U6FXPY2ocJfe2URUObs0KGYMmjgSZyH64vqrXQN8AlMZJ9Ivi5nORvF6ertBtFt3gH7jPt6aaEqc4r',
        level='L1',
        mean=2.9384593308951845,
        enrollment_status='Sélectionné(e)',
        imported_id='GqhCp',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='1',
        price=5.096219556664394,
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
        name='zLQE7',
        abbreviation='RzZnA',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='aqICl',
        repeat_status='1',
        id_journey=journey.id,
        imported_id='azW5j',
        is_valid=False,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    # Test data for ResultTeachingUnit
    result_teaching_unit_data = schemas.ResultTeachingUnitCreate(
        id_register_semester=register_semester.id,
        note=3.316976124508733,
        is_valid=False,
        date_validation='2025-11-15T18:57:07.985241',
        comment='5iFBI5xroJTJ4CQEXswK0UPY1PM9y7DYbhVkEVuWwB',
    )

    result_teaching_unit = crud.result_teaching_unit.create(db=db, obj_in=result_teaching_unit_data)

    # Assertions
    assert result_teaching_unit.id is not None
    assert result_teaching_unit.id_register_semester == result_teaching_unit_data.id_register_semester
    assert result_teaching_unit.note == result_teaching_unit_data.note
    assert result_teaching_unit.is_valid == result_teaching_unit_data.is_valid
    assert result_teaching_unit.date_validation == result_teaching_unit_data.date_validation
    assert result_teaching_unit.comment == result_teaching_unit_data.comment


def test_update_result_teaching_unit(db: Session):
    """Test update operation for ResultTeachingUnit."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='yJ87F',
        slug='Ari7u',
        abbreviation='XNgET',
        plugged='cX7Se',
        background='GgZhD',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='wVFBn',
        code='p0AP4',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='dNlDB',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='kKaAj',
        value='hVRCt',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='T3FwJ',
        email='at6M2@chxtc.com',
        num_select='aEDXN',
        last_name='Ftr8Q',
        first_name='2TzyQ',
        date_of_birth='2025-11-15',
        place_of_birth='SKcFv',
        address='paa5zcd6NSswp87gVMChrdPs6jB',
        sex='Féminin',
        martial_status='Marié(e)',
        phone_number='IH6Kb',
        num_of_cin='8autH',
        date_of_cin='2025-11-15',
        place_of_cin='GIDsk',
        repeat_status='0',
        picture='DdF0I',
        num_of_baccalaureate='5gkdT',
        center_of_baccalaureate='Kpn4L',
        year_of_baccalaureate='2025-11-15',
        job='V7nkL',
        father_name='bxRsb',
        father_job='iPLsz',
        mother_name='LOoJO',
        mother_job='ISBbW',
        parent_address='oqdcXyS4YNKNerakA8OGbnpbnA6UtWNqBWSwNhKPkpwrimnDyKf17aGEUjPGFZKpLB',
        level='M1',
        mean=4.363478533346349,
        enrollment_status='Sélectionné(e)',
        imported_id='1ouMy',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=5.3212193821628375,
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
        name='q88g9',
        abbreviation='btg3w',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='GbagX',
        repeat_status='1',
        id_journey=journey.id,
        imported_id='I4F3b',
        is_valid=False,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    # Test data for ResultTeachingUnit
    result_teaching_unit_data = schemas.ResultTeachingUnitCreate(
        id_register_semester=register_semester.id,
        note=1.516266844934083,
        is_valid=False,
        date_validation='2025-11-15T18:57:07.986200',
        comment='cnWbRQWVKrxxQbef52ap85QRHfjuA4M35gALR1IT6Z4B4uoY0i3bNsMWOxoS7QxgHcAE5hT9xUipXmrdL',
    )

    result_teaching_unit = crud.result_teaching_unit.create(db=db, obj_in=result_teaching_unit_data)

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
        if k in ['date_validation'] and isinstance(v, str):
            return (datetime.fromisoformat(v) + timedelta(days=1)).isoformat()
        if k in ['date_validation'] and isinstance(v, datetime):
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
    note_value = result_teaching_unit.note
    is_valid_value = result_teaching_unit.is_valid
    date_validation_value = result_teaching_unit.date_validation
    comment_value = result_teaching_unit.comment
    update_data = schemas.ResultTeachingUnitUpdate(**{
        k: _updated_value(k, v)
        for k, v in result_teaching_unit_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_result_teaching_unit = crud.result_teaching_unit.update(
        db=db, db_obj=result_teaching_unit, obj_in=update_data
    )

    # Assertions
    assert updated_result_teaching_unit.id == result_teaching_unit.id
    assert updated_result_teaching_unit.note != note_value
    assert updated_result_teaching_unit.is_valid != is_valid_value
    assert updated_result_teaching_unit.date_validation.date() != date_validation_value.date()
    assert updated_result_teaching_unit.comment != comment_value


def test_get_result_teaching_unit(db: Session):
    """Test get operation for ResultTeachingUnit."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='GE4Ky',
        slug='mAXrN',
        abbreviation='AO5E0',
        plugged='RkZHR',
        background='JCaY7',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='1dsyn',
        code='2rPso',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='aJUnM',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='KxgaR',
        value='Qsaoy',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='wYkL6',
        email='xlsDy@9mz91.com',
        num_select='LfMxO',
        last_name='l2ihs',
        first_name='jZChv',
        date_of_birth='2025-11-15',
        place_of_birth='WW2Hb',
        address='htUeUh0AtbZHJf4Qw0RA6Y694MTOyj3iS3RCNhDeUQbU9V7WsDoyiDwLrzldlJTjIb252UfeJ',
        sex='Féminin',
        martial_status='Marié(e)',
        phone_number='uaooh',
        num_of_cin='pPaA7',
        date_of_cin='2025-11-15',
        place_of_cin='fpJne',
        repeat_status='2',
        picture='ZqJ2D',
        num_of_baccalaureate='7LBL7',
        center_of_baccalaureate='Ym3Vx',
        year_of_baccalaureate='2025-11-15',
        job='yrnET',
        father_name='hadS8',
        father_job='dYmHu',
        mother_name='gad2K',
        mother_job='wtkWQ',
        parent_address='2eZ6aRpjX1yHOpA6x',
        level='L2',
        mean=4.641552462566777,
        enrollment_status='Inscrit(e)',
        imported_id='YopwT',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=1.5673002065602701,
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
        name='V8xR6',
        abbreviation='HpYbZ',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='C9YAc',
        repeat_status='0',
        id_journey=journey.id,
        imported_id='ejP21',
        is_valid=True,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    # Test data for ResultTeachingUnit
    result_teaching_unit_data = schemas.ResultTeachingUnitCreate(
        id_register_semester=register_semester.id,
        note=5.248473952550778,
        is_valid=False,
        date_validation='2025-11-15T18:57:07.987104',
        comment='ckiQZF5',
    )

    result_teaching_unit = crud.result_teaching_unit.create(db=db, obj_in=result_teaching_unit_data)

    # Get all records
    records = crud.result_teaching_unit.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == result_teaching_unit.id for r in records)


def test_get_by_id_result_teaching_unit(db: Session):
    """Test get_by_id operation for ResultTeachingUnit."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='LjfOy',
        slug='i2y3j',
        abbreviation='u73Vo',
        plugged='TEhVP',
        background='GcnC8',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='NbtyY',
        code='tHG2L',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='4UfiL',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='Tazgi',
        value='AVAlE',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='pEeI5',
        email='G9VCX@6iqzv.com',
        num_select='blN81',
        last_name='G6dmo',
        first_name='UCPbp',
        date_of_birth='2025-11-15',
        place_of_birth='Q4YEE',
        address='QOtpAeJ5CV4FJIQBfH77NSM2SWviRtxuRMCQnJsEB5sbaTav9nrUzdOyqbABF2PcYWp2t67Mmevdw',
        sex='Féminin',
        martial_status='Veuf/Veuve',
        phone_number='sh786',
        num_of_cin='tOL6X',
        date_of_cin='2025-11-15',
        place_of_cin='JYzom',
        repeat_status='1',
        picture='uPEsf',
        num_of_baccalaureate='TdTa4',
        center_of_baccalaureate='V5j9x',
        year_of_baccalaureate='2025-11-15',
        job='RVsEh',
        father_name='RaWqN',
        father_job='8duDh',
        mother_name='w3XpB',
        mother_job='nhF89',
        parent_address='mT0K6yWX6VnadIlLCoxaQA3u2lCXEx8dr8YE',
        level='L2',
        mean=2.446665595862152,
        enrollment_status='ancien(ne)',
        imported_id='npq8R',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=3.8293515903726,
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
        name='7uo5M',
        abbreviation='F6p2y',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='MHJpv',
        repeat_status='2',
        id_journey=journey.id,
        imported_id='RrFgM',
        is_valid=True,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    # Test data for ResultTeachingUnit
    result_teaching_unit_data = schemas.ResultTeachingUnitCreate(
        id_register_semester=register_semester.id,
        note=1.507397637129384,
        is_valid=False,
        date_validation='2025-11-15T18:57:07.988160',
        comment='bz22LbbqZAXVQkaIKgOGhvTfoTw7y3IwGEbbHT7YcNhuVaI3zp1qaHhC0JTMvhNn5g7Cr4GW9riZfK',
    )

    result_teaching_unit = crud.result_teaching_unit.create(db=db, obj_in=result_teaching_unit_data)

    # Get by ID
    retrieved_result_teaching_unit = crud.result_teaching_unit.get(db=db, id=result_teaching_unit.id)

    # Assertions
    assert retrieved_result_teaching_unit is not None
    assert retrieved_result_teaching_unit.id == result_teaching_unit.id
    assert retrieved_result_teaching_unit.id_register_semester == result_teaching_unit.id_register_semester
    assert retrieved_result_teaching_unit.note == result_teaching_unit.note
    assert retrieved_result_teaching_unit.is_valid == result_teaching_unit.is_valid
    assert retrieved_result_teaching_unit.date_validation == result_teaching_unit.date_validation
    assert retrieved_result_teaching_unit.comment == result_teaching_unit.comment


def test_delete_result_teaching_unit(db: Session):
    """Test delete operation for ResultTeachingUnit."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='119xc',
        slug='UPsbM',
        abbreviation='4HWN8',
        plugged='kkDxS',
        background='Ei6pm',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='bRdUQ',
        code='v6ak7',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='u13T0',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='FvQYS',
        value='B004M',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='IkQMV',
        email='UXkzo@1chvf.com',
        num_select='tYj4w',
        last_name='Ebtc3',
        first_name='VFG8t',
        date_of_birth='2025-11-15',
        place_of_birth='aaVCK',
        address='Q5P1FXbw4jzvPEQrSJDnMOkhR8uIVqxQoFJc1aYNkM0xpgRftK',
        sex='Masculin',
        martial_status='Marié(e)',
        phone_number='ccTh1',
        num_of_cin='eoTHQ',
        date_of_cin='2025-11-15',
        place_of_cin='zQWIT',
        repeat_status='1',
        picture='eRU1I',
        num_of_baccalaureate='14be8',
        center_of_baccalaureate='eVd6G',
        year_of_baccalaureate='2025-11-15',
        job='wZIUI',
        father_name='wtdEv',
        father_job='trLni',
        mother_name='TonSQ',
        mother_job='P5UF2',
        parent_address='RhxHjnYcs4i2R5',
        level='L2',
        mean=4.728598507971769,
        enrollment_status='Sélectionné(e)',
        imported_id='nNLHR',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=4.385534788939988,
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
        name='PtL87',
        abbreviation='vt7F5',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='82zZE',
        repeat_status='0',
        id_journey=journey.id,
        imported_id='9Ue5x',
        is_valid=True,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    # Test data for ResultTeachingUnit
    result_teaching_unit_data = schemas.ResultTeachingUnitCreate(
        id_register_semester=register_semester.id,
        note=3.7114843439534018,
        is_valid=True,
        date_validation='2025-11-15T18:57:07.989927',
        comment='tPh0cUlJe0pfthx3YhYy01wBsRq7Fi3Db5VY82ycAsxwVeRb',
    )

    result_teaching_unit = crud.result_teaching_unit.create(db=db, obj_in=result_teaching_unit_data)

    # Delete record
    deleted_result_teaching_unit = crud.result_teaching_unit.remove(db=db, id=result_teaching_unit.id)

    # Assertions
    assert deleted_result_teaching_unit is not None
    assert deleted_result_teaching_unit.id == result_teaching_unit.id

    # Verify deletion
    assert crud.result_teaching_unit.get(db=db, id=result_teaching_unit.id) is None

# begin #
# ---write your code here--- #
# end #

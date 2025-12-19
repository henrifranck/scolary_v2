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
"""Tests for CRUD operations on Note model."""


def test_create_note(db: Session):
    """Test create operation for Note."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='l3Ie0',
        slug='yWMGR',
        abbreviation='TuOSv',
        plugged='nB48J',
        background='iMKyZ',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='HjvAX',
        code='H4boP',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='iOxW5',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='15gj5',
        value='ieUvC',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='CrgFH',
        email='lRC2c@xqw0n.com',
        num_select='1JpkT',
        last_name='yWGb9',
        first_name='7jqoe',
        date_of_birth='2025-11-15',
        place_of_birth='zMHHm',
        address='hl9UwxsRMy1HqK5',
        sex='Féminin',
        martial_status='Veuf/Veuve',
        phone_number='rNgEz',
        num_of_cin='H4ap5',
        date_of_cin='2025-11-15',
        place_of_cin='9iNr8',
        repeat_status='1',
        picture='Lpp5O',
        num_of_baccalaureate='FRSn2',
        center_of_baccalaureate='43XpF',
        year_of_baccalaureate='2025-11-15',
        job='qQXLX',
        father_name='mUEX1',
        father_job='VOMWy',
        mother_name='NbCG6',
        mother_job='IMejc',
        parent_address='E7XKWQ6i2sN',
        level='L2',
        mean=5.143743178217843,
        enrollment_status='ancien(ne)',
        imported_id='Wzepw',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=2.7990691559301037,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=7,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='k1O9S',
        abbreviation='MpSUh',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='sJtZg',
        repeat_status='2',
        id_journey=journey.id,
        imported_id='KndCu',
        is_valid=True,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='Yfuz2',
        semester='QtHnm',
        id_journey=journey.id,
        color='kYETG',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='KR6TR',
        semester='H99x5',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='DxawJ',
        selection_regle='2V1BqbcSQJGCHbIzDZ0TSSryLo6CIqUr90KlYuecF',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=13,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='AI3bCz5ww2yY4zBtWt52i2vg0f5PeOBSGfJubR',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=4.001663264304363,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

    # Test data for User
    user_data = schemas.UserCreate(
        email='V5oLH@jrvk0.com',
        first_name='ZJq7L',
        last_name='x1ifw',
        password='GKWMM',
        is_superuser=True,
        picture='BKekx',
        is_active=False,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Note
    note_data = schemas.NoteCreate(
        id_register_semester=register_semester.id,
        id_constituent_element_offering=constituent_element_offering.id,
        session='Normal',
        note=2.574180199745103,
        id_user=user.id,
        comment='ubVrmbk',
    )

    note = crud.note.create(db=db, obj_in=note_data)

    # Assertions
    assert note.id is not None
    assert note.id_register_semester == note_data.id_register_semester
    assert note.id_constituent_element_offering == note_data.id_constituent_element_offering
    assert note.session == note_data.session
    assert note.note == note_data.note
    assert note.id_user == note_data.id_user
    assert note.comment == note_data.comment


def test_update_note(db: Session):
    """Test update operation for Note."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='CYJtt',
        slug='6GjKx',
        abbreviation='b0gZS',
        plugged='ZPV03',
        background='w5NQI',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='YC0Ii',
        code='84EBX',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='imvYn',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='bizvf',
        value='rH3j2',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='LjyTp',
        email='cx48o@di8og.com',
        num_select='8Qsp1',
        last_name='fN3z2',
        first_name='40CkG',
        date_of_birth='2025-11-15',
        place_of_birth='dZpIm',
        address='AUD6uxNtBteydIFkJDJnXHqD9CXvBhvXlJoiegQF9zS1fv2K7LY6im',
        sex='Féminin',
        martial_status='Célibataire',
        phone_number='OOnkS',
        num_of_cin='rukNf',
        date_of_cin='2025-11-15',
        place_of_cin='UR0G7',
        repeat_status='1',
        picture='rxK6s',
        num_of_baccalaureate='ygrH3',
        center_of_baccalaureate='DnbnM',
        year_of_baccalaureate='2025-11-15',
        job='T7b7P',
        father_name='EhFmh',
        father_job='D7jNv',
        mother_name='kwN9u',
        mother_job='g6xXj',
        parent_address='X6RniiKOq1tWCH',
        level='L3',
        mean=5.190582290716762,
        enrollment_status='Sélectionné(e)',
        imported_id='fqUkT',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=2.531926276435087,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=9,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='BthjU',
        abbreviation='w72wT',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='7qual',
        repeat_status='1',
        id_journey=journey.id,
        imported_id='mtHNc',
        is_valid=False,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='WwA35',
        semester='C2vC9',
        id_journey=journey.id,
        color='3V7Bf',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='RDkis',
        semester='DBBgD',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='pdkZw',
        selection_regle='fs8kQTHsbmUzW4iq1L8ZmOFhuwIT0phCp5',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=12,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='r8rZauKFzQRXxGrZ6LknHddGgTYga',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=4.833138781616311,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

    # Test data for User
    user_data = schemas.UserCreate(
        email='wODGS@mfhbk.com',
        first_name='mUPew',
        last_name='MsArq',
        password='QgZfU',
        is_superuser=True,
        picture='bEsud',
        is_active=True,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Note
    note_data = schemas.NoteCreate(
        id_register_semester=register_semester.id,
        id_constituent_element_offering=constituent_element_offering.id,
        session='Normal',
        note=2.3416741179258067,
        id_user=user.id,
        comment='xrPjNKX6Uc74WQR2w1fG1qsvLEIik4TsvxNzBLzU77iq9D',
    )

    note = crud.note.create(db=db, obj_in=note_data)

    # Precompute enum values for update
    enum_values_map = {}
    enum_values_map['session'] = ['Normal', 'Rattrapage']

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
    session_value = note.session
    note_value = note.note
    comment_value = note.comment
    update_data = schemas.NoteUpdate(**{
        k: _updated_value(k, v)
        for k, v in note_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_note = crud.note.update(
        db=db, db_obj=note, obj_in=update_data
    )

    # Assertions
    assert updated_note.id == note.id
    assert updated_note.session != session_value
    assert updated_note.note != note_value
    assert updated_note.comment != comment_value


def test_get_note(db: Session):
    """Test get operation for Note."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='5zAuo',
        slug='aWkuH',
        abbreviation='38MA1',
        plugged='0DVwV',
        background='KZZu7',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='H1zbt',
        code='5QSQs',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='igBbk',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='rmEKc',
        value='jKmWD',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='R3SIJ',
        email='YwFAH@2jpl2.com',
        num_select='mJYKH',
        last_name='VHL8r',
        first_name='TYSMZ',
        date_of_birth='2025-11-15',
        place_of_birth='uCpgn',
        address='lBSVKDJG9YOXMdBrG7SVoyIjB7JkD1KB9njdtccjlbFtqTeEGd1TrP8wYsWxykSB',
        sex='Masculin',
        martial_status='Marié(e)',
        phone_number='7dgGh',
        num_of_cin='f3Eo7',
        date_of_cin='2025-11-15',
        place_of_cin='bgygn',
        repeat_status='2',
        picture='sb5Q7',
        num_of_baccalaureate='rWyJu',
        center_of_baccalaureate='GgSev',
        year_of_baccalaureate='2025-11-15',
        job='wP4bd',
        father_name='sF9Ek',
        father_job='fX8sQ',
        mother_name='N4yVm',
        mother_job='zmoZW',
        parent_address='860kGBVRGwBhbgGQ5kTaTWcb3KNYznw6NxOPGMQSFpSL4og666esfKJjjfr8SVFZmgR9yEsWLhNeURESP48Fb87V2G6Jp',
        level='L3',
        mean=4.559843247395416,
        enrollment_status='En attente',
        imported_id='SRObw',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=3.800184168913742,
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
        name='lS7Hj',
        abbreviation='YexTL',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='zjLT0',
        repeat_status='1',
        id_journey=journey.id,
        imported_id='dK5zv',
        is_valid=False,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='vhtro',
        semester='R5Hgg',
        id_journey=journey.id,
        color='G32Vv',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='SWUqE',
        semester='a56xP',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='lghTA',
        selection_regle='HiUZJHXdJ',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=1,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='3QKr2ytSW8iGSbC0AGziRn',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=3.950161499810742,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

    # Test data for User
    user_data = schemas.UserCreate(
        email='DlQDW@bibxg.com',
        first_name='HSack',
        last_name='IUfYN',
        password='qDgC2',
        is_superuser=True,
        picture='JwDrH',
        is_active=True,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Note
    note_data = schemas.NoteCreate(
        id_register_semester=register_semester.id,
        id_constituent_element_offering=constituent_element_offering.id,
        session='Rattrapage',
        note=4.371377401600446,
        id_user=user.id,
        comment='l5ixOUeZFIkRUz',
    )

    note = crud.note.create(db=db, obj_in=note_data)

    # Get all records
    records = crud.note.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == note.id for r in records)


def test_get_by_id_note(db: Session):
    """Test get_by_id operation for Note."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='tYpH0',
        slug='zs2aR',
        abbreviation='f187c',
        plugged='o4B9u',
        background='EiRqA',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='2jz3F',
        code='hDUXC',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='wd9dA',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='WwoSU',
        value='VCQbt',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='Q7nRU',
        email='Al22u@53kvk.com',
        num_select='WOgoK',
        last_name='HB7hm',
        first_name='cPN6n',
        date_of_birth='2025-11-15',
        place_of_birth='qlyaC',
        address='DOXeHyHQAbsE4qBz',
        sex='Masculin',
        martial_status='Divorcé(e)',
        phone_number='CGGNL',
        num_of_cin='GQ0Tq',
        date_of_cin='2025-11-15',
        place_of_cin='3lr18',
        repeat_status='0',
        picture='Mp7h0',
        num_of_baccalaureate='m3KRB',
        center_of_baccalaureate='FIlRQ',
        year_of_baccalaureate='2025-11-15',
        job='tN70P',
        father_name='NABEw',
        father_job='81OgY',
        mother_name='7biVZ',
        mother_job='XdSlO',
        parent_address='SRtZgoq7jUpFgIBHfaNbvvQHZqt2cfSE5vJO7nD4Y3OTZFhyfCe',
        level='L3',
        mean=4.577433696976948,
        enrollment_status='ancien(ne)',
        imported_id='C2D68',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=3.560210559393786,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=17,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='7xjRc',
        abbreviation='Fwv2V',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='i95ee',
        repeat_status='1',
        id_journey=journey.id,
        imported_id='cftTW',
        is_valid=True,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='uVxb0',
        semester='uwejr',
        id_journey=journey.id,
        color='rErVt',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='jIwk5',
        semester='6ykH1',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='uUZIx',
        selection_regle='QglIrSt1gSMX4QK3Ok6qumS1awLbMgYTkf1Mzku1fedjlt',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=19,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='no6dOAWAEjTymF6gtWJjZh3lRb9rwMAcxQw310m6CzuS9TBXp0JjWaK3HKgtDbAVtekoU',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=2.115478988768646,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

    # Test data for User
    user_data = schemas.UserCreate(
        email='iQPX0@7necq.com',
        first_name='QhIWC',
        last_name='i5JPg',
        password='Ix9tw',
        is_superuser=False,
        picture='oJBS3',
        is_active=False,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Note
    note_data = schemas.NoteCreate(
        id_register_semester=register_semester.id,
        id_constituent_element_offering=constituent_element_offering.id,
        session='Rattrapage',
        note=1.9846675459687204,
        id_user=user.id,
        comment='DSIuAYdyl0z',
    )

    note = crud.note.create(db=db, obj_in=note_data)

    # Get by ID
    retrieved_note = crud.note.get(db=db, id=note.id)

    # Assertions
    assert retrieved_note is not None
    assert retrieved_note.id == note.id
    assert retrieved_note.id_register_semester == note.id_register_semester
    assert retrieved_note.id_constituent_element_offering == note.id_constituent_element_offering
    assert retrieved_note.session == note.session
    assert retrieved_note.note == note.note
    assert retrieved_note.id_user == note.id_user
    assert retrieved_note.comment == note.comment


def test_delete_note(db: Session):
    """Test delete operation for Note."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='qQkBq',
        slug='QDcvk',
        abbreviation='eTcHu',
        plugged='DDwlu',
        background='Hno77',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='dv2ZC',
        code='R9S4O',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='hDnD2',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='S9tnv',
        value='mcfzW',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='szRFk',
        email='Lx0uo@e3hlx.com',
        num_select='UaIWH',
        last_name='Zh4Uu',
        first_name='ViiuR',
        date_of_birth='2025-11-15',
        place_of_birth='UzNam',
        address='d5KIIp4moUf3MGgx1gd8UkCQHZhLmWF1igr0cNOv62OkOg3d3scAotccXjUmdyOG1wAVhjO6SfUSPfTo0JPfmU4cb3eTSjxDmt',
        sex='Masculin',
        martial_status='Marié(e)',
        phone_number='JYqzX',
        num_of_cin='4rLXo',
        date_of_cin='2025-11-15',
        place_of_cin='FDrGd',
        repeat_status='1',
        picture='Mdtic',
        num_of_baccalaureate='S5AbV',
        center_of_baccalaureate='SHXTF',
        year_of_baccalaureate='2025-11-15',
        job='XSnX1',
        father_name='1C3z1',
        father_job='XXlAA',
        mother_name='IQxS8',
        mother_job='oju4G',
        parent_address='4c67Uxw4vtWp12BNx8vS6OryT0Gb4Cnl7AFWfBeoq0OWAxl5qVzNkkTO3Hh4VxUb',
        level='L3',
        mean=5.373286748343132,
        enrollment_status='Inscrit(e)',
        imported_id='sYLaV',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=5.205063607827547,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=20,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='Trkvt',
        abbreviation='R2bwp',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='Uk0p6',
        repeat_status='0',
        id_journey=journey.id,
        imported_id='pMA5W',
        is_valid=False,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='9lXb1',
        semester='obC5E',
        id_journey=journey.id,
        color='mceFs',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='Gw1pX',
        semester='26ehd',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='4a1hl',
        selection_regle='vGJ4gIZ',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=15,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='DGnycjvQAWAzergB3yFzujNaJ1ozeNDoXgR9YwEqjTRfNWwGioKCiPOVU6cd8ZW4JjNIyQv1p',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=2.354692175545993,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

    # Test data for User
    user_data = schemas.UserCreate(
        email='MpZ5D@k3ywe.com',
        first_name='ZWUyM',
        last_name='K8aR3',
        password='eoZR7',
        is_superuser=False,
        picture='azHEk',
        is_active=False,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Note
    note_data = schemas.NoteCreate(
        id_register_semester=register_semester.id,
        id_constituent_element_offering=constituent_element_offering.id,
        session='Normal',
        note=1.8354922525779496,
        id_user=user.id,
        comment='yORN0SzEJ7q6fz5V0zmH8MEV1mqOAfCxwmadIcXj0wRahCkAjVKL5vhiG3f0D1CCb5tWtQF7hV0RyrSsGv88cITXlLxFbHB',
    )

    note = crud.note.create(db=db, obj_in=note_data)

    # Delete record
    deleted_note = crud.note.remove(db=db, id=note.id)

    # Assertions
    assert deleted_note is not None
    assert deleted_note.id == note.id

    # Verify deletion
    assert crud.note.get(db=db, id=note.id) is None

# begin #
# ---write your code here--- #
# end #

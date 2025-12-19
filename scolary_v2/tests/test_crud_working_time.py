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
"""Tests for CRUD operations on WorkingTime model."""


def test_create_working_time(db: Session):
    """Test create operation for WorkingTime."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='e3mZR',
        slug='UmCEm',
        abbreviation='MR4pc',
        plugged='vR21X',
        background='mGlzl',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='USIGz',
        abbreviation='szREM',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='MC8aB',
        semester='dywHK',
        id_journey=journey.id,
        color='A0iJm',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='Te1at',
        code='UdK5w',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='Zpv3s',
        semester='PBiGJ',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='elyfI',
        selection_regle='1',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=0,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='p1f2sSR9yi3JCMgmSvCOa4d83HjBmn6pBtk2CzgGwomfJZhqNzDpYPTHc',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=1.6154987984075304,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

    # Test data for Group
    group_data = schemas.GroupCreate(
        id_journey=journey.id,
        semester='dvyJm',
        group_number=12,
        student_count=5,
    )

    group = crud.group.create(db=db, obj_in=group_data)

    # Test data for WorkingTime
    working_time_data = schemas.WorkingTimeCreate(
        id_constituent_element=constituent_element_offering.id,
        working_time_type='td',
        day='5YWaP',
        start='01:30:40',
        end='17:05:17',
        id_group=group.id,
        date='2025-11-15T18:57:07.927769',
        session='Normal',
    )

    working_time = crud.working_time.create(db=db, obj_in=working_time_data)

    # Assertions
    assert working_time.id is not None
    assert working_time.id_constituent_element == working_time_data.id_constituent_element
    assert working_time.working_time_type == working_time_data.working_time_type
    assert working_time.day == working_time_data.day
    assert working_time.start == working_time_data.start
    assert working_time.end == working_time_data.end
    assert working_time.id_group == working_time_data.id_group
    assert working_time.date == working_time_data.date
    assert working_time.session == working_time_data.session


def test_update_working_time(db: Session):
    """Test update operation for WorkingTime."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='UpU0B',
        slug='8IeVO',
        abbreviation='uGnRK',
        plugged='SzUv7',
        background='4kmOY',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='nY77t',
        abbreviation='3Bj0u',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='0jBp4',
        semester='gHdSa',
        id_journey=journey.id,
        color='SKzja',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='ylO43',
        code='THDLl',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='bHucO',
        semester='yPGM1',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='MrDNs',
        selection_regle='VJ0OMkm',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=7,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='ysTuINUFQY2GWCgbeU5iIUsEZFZhCxxtxfvWKa7kECvsVczbYttANOdJPUMZ0cbdEiJfpPIVSDc5K',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=4.581719143520891,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

    # Test data for Group
    group_data = schemas.GroupCreate(
        id_journey=journey.id,
        semester='NSwUd',
        group_number=7,
        student_count=19,
    )

    group = crud.group.create(db=db, obj_in=group_data)

    # Test data for WorkingTime
    working_time_data = schemas.WorkingTimeCreate(
        id_constituent_element=constituent_element_offering.id,
        working_time_type='Exam',
        day='hoygT',
        start='13:16:31',
        end='07:44:52',
        id_group=group.id,
        date='2025-11-15T18:57:07.929774',
        session='Rattrapage',
    )

    working_time = crud.working_time.create(db=db, obj_in=working_time_data)

    # Precompute enum values for update
    enum_values_map = {}
    enum_values_map['working_time_type'] = ['cours', 'tp', 'td', 'Exam']
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
        if k in ['date'] and isinstance(v, str):
            return (datetime.fromisoformat(v) + timedelta(days=1)).isoformat()
        if k in ['date'] and isinstance(v, datetime):
            return v + timedelta(days=1)

        # date +1 day
        if k in [] and isinstance(v, str):
            return (date.fromisoformat(v) + timedelta(days=1)).isoformat()
        if k in [] and isinstance(v, date):
            return v + timedelta(days=1)

        # time +1 hour
        if k in ['start', 'end'] and isinstance(v, str):
            return (datetime.strptime(v, '%H:%M:%S') + timedelta(hours=1)).time().strftime('%H:%M:%S')
        if k in ['start', 'end'] and isinstance(v, time):
            return (datetime.combine(date.today(), v) + timedelta(hours=1)).time()

        # fallback -> prefix 'updated_'
        return f'updated_{v}'

    # Update data
    working_time_type_value = working_time.working_time_type
    day_value = working_time.day
    start_value = working_time.start
    end_value = working_time.end
    date_value = working_time.date
    session_value = working_time.session
    update_data = schemas.WorkingTimeUpdate(**{
        k: _updated_value(k, v)
        for k, v in working_time_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_working_time = crud.working_time.update(
        db=db, db_obj=working_time, obj_in=update_data
    )

    # Assertions
    assert updated_working_time.id == working_time.id
    assert updated_working_time.working_time_type != working_time_type_value
    assert updated_working_time.day != day_value
    assert updated_working_time.start.strftime('%H:%M:%S') != start_value.strftime('%H:%M:%S')
    assert updated_working_time.end.strftime('%H:%M:%S') != end_value.strftime('%H:%M:%S')
    assert updated_working_time.date.date() != date_value.date()
    assert updated_working_time.session != session_value


def test_get_working_time(db: Session):
    """Test get operation for WorkingTime."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='DbkwC',
        slug='Sd042',
        abbreviation='RtKRC',
        plugged='h9BzR',
        background='YG1Ew',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='gnnhx',
        abbreviation='bE9dm',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='tTsTu',
        semester='FMcOI',
        id_journey=journey.id,
        color='JaQhy',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='lUpVr',
        code='miopS',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='0UDAw',
        semester='3caoZ',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='syseh',
        selection_regle='Y7ZbC8svKhSIFRIkClkoaiPbN2jfH6fLXkq3rdN4jqq6rKbyGbEBlpiUmYk',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=14,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='5bjdDV18DqyHr60v5QP5qrd0ieY',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=4.1525084394379945,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

    # Test data for Group
    group_data = schemas.GroupCreate(
        id_journey=journey.id,
        semester='bPrnM',
        group_number=0,
        student_count=6,
    )

    group = crud.group.create(db=db, obj_in=group_data)

    # Test data for WorkingTime
    working_time_data = schemas.WorkingTimeCreate(
        id_constituent_element=constituent_element_offering.id,
        working_time_type='cours',
        day='JeDp3',
        start='03:13:34',
        end='13:00:04',
        id_group=group.id,
        date='2025-11-15T18:57:07.932542',
        session='Normal',
    )

    working_time = crud.working_time.create(db=db, obj_in=working_time_data)

    # Get all records
    records = crud.working_time.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == working_time.id for r in records)


def test_get_by_id_working_time(db: Session):
    """Test get_by_id operation for WorkingTime."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='93m57',
        slug='mgLt1',
        abbreviation='r0Sqo',
        plugged='TlJWG',
        background='t8SUA',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='ArMFv',
        abbreviation='lC0nL',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='FnfvC',
        semester='MHV8a',
        id_journey=journey.id,
        color='5G1Rj',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='0tmJK',
        code='GipxE',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='MZkJH',
        semester='gmURW',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='41Enf',
        selection_regle='E0FPkWkho14Zaxi',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=4,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='dZW6RLIpAD1I6QjOEZMrxNoivpNVBfINQPp8kQ1HH4RNv1HLK1UqyuKcBRipTh6SM5SW3TsQVDQRRom0FL2eAAyIOE0',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=4.615085365172828,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

    # Test data for Group
    group_data = schemas.GroupCreate(
        id_journey=journey.id,
        semester='sgJDU',
        group_number=1,
        student_count=9,
    )

    group = crud.group.create(db=db, obj_in=group_data)

    # Test data for WorkingTime
    working_time_data = schemas.WorkingTimeCreate(
        id_constituent_element=constituent_element_offering.id,
        working_time_type='cours',
        day='hXFjC',
        start='07:37:50',
        end='03:31:41',
        id_group=group.id,
        date='2025-11-15T18:57:07.933143',
        session='Normal',
    )

    working_time = crud.working_time.create(db=db, obj_in=working_time_data)

    # Get by ID
    retrieved_working_time = crud.working_time.get(db=db, id=working_time.id)

    # Assertions
    assert retrieved_working_time is not None
    assert retrieved_working_time.id == working_time.id
    assert retrieved_working_time.id_constituent_element == working_time.id_constituent_element
    assert retrieved_working_time.working_time_type == working_time.working_time_type
    assert retrieved_working_time.day == working_time.day
    assert retrieved_working_time.start == working_time.start
    assert retrieved_working_time.end == working_time.end
    assert retrieved_working_time.id_group == working_time.id_group
    assert retrieved_working_time.date == working_time.date
    assert retrieved_working_time.session == working_time.session


def test_delete_working_time(db: Session):
    """Test delete operation for WorkingTime."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='9jcio',
        slug='Oc6I3',
        abbreviation='4zqGX',
        plugged='8GT2J',
        background='5pRg3',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='0SqYi',
        abbreviation='u6KYK',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='fd77b',
        semester='JGfyW',
        id_journey=journey.id,
        color='3pxGE',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='OjV4e',
        code='fHzzx',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='BPO7S',
        semester='hNnYD',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='4Oo7U',
        selection_regle='SjGXFTBt3VazIhK40FpbfqFVndU1n',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=8,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='13PCeIzNMKmZRQDH8VSK2zQh3XS0ZS67rZ1DPKJbE',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=3.7627830076393005,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

    # Test data for Group
    group_data = schemas.GroupCreate(
        id_journey=journey.id,
        semester='ckJ95',
        group_number=14,
        student_count=1,
    )

    group = crud.group.create(db=db, obj_in=group_data)

    # Test data for WorkingTime
    working_time_data = schemas.WorkingTimeCreate(
        id_constituent_element=constituent_element_offering.id,
        working_time_type='Exam',
        day='4gBxw',
        start='14:26:27',
        end='05:13:34',
        id_group=group.id,
        date='2025-11-15T18:57:07.933759',
        session='Normal',
    )

    working_time = crud.working_time.create(db=db, obj_in=working_time_data)

    # Delete record
    deleted_working_time = crud.working_time.remove(db=db, id=working_time.id)

    # Assertions
    assert deleted_working_time is not None
    assert deleted_working_time.id == working_time.id

    # Verify deletion
    assert crud.working_time.get(db=db, id=working_time.id) is None

# begin #
# ---write your code here--- #
# end #

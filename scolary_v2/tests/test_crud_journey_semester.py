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
"""Tests for CRUD operations on JourneySemester model."""


def test_create_journey_semester(db: Session):
    """Test create operation for JourneySemester."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='ClMT4',
        slug='4OK2N',
        abbreviation='H8K68',
        plugged='dilVI',
        background='MeVRj',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='AXR4B',
        abbreviation='aHWJ9',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for JourneySemester
    journey_semester_data = schemas.JourneySemesterCreate(
        id_journey=journey.id,
        semester='Zj1l8',
    )

    journey_semester = crud.journey_semester.create(db=db, obj_in=journey_semester_data)

    # Assertions
    assert journey_semester.id is not None
    assert journey_semester.id_journey == journey_semester_data.id_journey
    assert journey_semester.semester == journey_semester_data.semester


def test_update_journey_semester(db: Session):
    """Test update operation for JourneySemester."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='Jzr0n',
        slug='bIKfl',
        abbreviation='W8nYT',
        plugged='Di4Hf',
        background='EUNGG',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='AS94D',
        abbreviation='AMfSV',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for JourneySemester
    journey_semester_data = schemas.JourneySemesterCreate(
        id_journey=journey.id,
        semester='nrfiJ',
    )

    journey_semester = crud.journey_semester.create(db=db, obj_in=journey_semester_data)

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
    semester_value = journey_semester.semester
    update_data = schemas.JourneySemesterUpdate(**{
        k: _updated_value(k, v)
        for k, v in journey_semester_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_journey_semester = crud.journey_semester.update(
        db=db, db_obj=journey_semester, obj_in=update_data
    )

    # Assertions
    assert updated_journey_semester.id == journey_semester.id
    assert updated_journey_semester.semester != semester_value


def test_get_journey_semester(db: Session):
    """Test get operation for JourneySemester."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='VTF5j',
        slug='VZmJN',
        abbreviation='Th65S',
        plugged='toQPy',
        background='adchj',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='0HSH1',
        abbreviation='uWpQp',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for JourneySemester
    journey_semester_data = schemas.JourneySemesterCreate(
        id_journey=journey.id,
        semester='cUTm0',
    )

    journey_semester = crud.journey_semester.create(db=db, obj_in=journey_semester_data)

    # Get all records
    records = crud.journey_semester.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == journey_semester.id for r in records)


def test_get_by_id_journey_semester(db: Session):
    """Test get_by_id operation for JourneySemester."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='bTdVB',
        slug='cWeph',
        abbreviation='YU5AX',
        plugged='Fvncm',
        background='QAguO',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='MsPI5',
        abbreviation='7P8qX',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for JourneySemester
    journey_semester_data = schemas.JourneySemesterCreate(
        id_journey=journey.id,
        semester='QRGQT',
    )

    journey_semester = crud.journey_semester.create(db=db, obj_in=journey_semester_data)

    # Get by ID
    retrieved_journey_semester = crud.journey_semester.get(db=db, id=journey_semester.id)

    # Assertions
    assert retrieved_journey_semester is not None
    assert retrieved_journey_semester.id == journey_semester.id
    assert retrieved_journey_semester.id_journey == journey_semester.id_journey
    assert retrieved_journey_semester.semester == journey_semester.semester


def test_delete_journey_semester(db: Session):
    """Test delete operation for JourneySemester."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='mDKvm',
        slug='cBjua',
        abbreviation='LKEPR',
        plugged='mJAnW',
        background='NckRa',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='y7lMI',
        abbreviation='xbxuD',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for JourneySemester
    journey_semester_data = schemas.JourneySemesterCreate(
        id_journey=journey.id,
        semester='hBkaY',
    )

    journey_semester = crud.journey_semester.create(db=db, obj_in=journey_semester_data)

    # Delete record
    deleted_journey_semester = crud.journey_semester.remove(db=db, id=journey_semester.id)

    # Assertions
    assert deleted_journey_semester is not None
    assert deleted_journey_semester.id == journey_semester.id

    # Verify deletion
    assert crud.journey_semester.get(db=db, id=journey_semester.id) is None

# begin #
# ---write your code here--- #
# end #

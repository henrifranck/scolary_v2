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
"""Tests for CRUD operations on TeachingUnit model."""


def test_create_teaching_unit(db: Session):
    """Test create operation for TeachingUnit."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='s9FtW',
        slug='M8K8R',
        abbreviation='SACUl',
        plugged='Vckcw',
        background='6N0cx',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='RNFfP',
        abbreviation='7Yn2d',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='5u4xH',
        semester='dRcRy',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Assertions
    assert teaching_unit.id is not None
    assert teaching_unit.name == teaching_unit_data.name
    assert teaching_unit.semester == teaching_unit_data.semester
    assert teaching_unit.id_journey == teaching_unit_data.id_journey


def test_update_teaching_unit(db: Session):
    """Test update operation for TeachingUnit."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='dYUNY',
        slug='IkpHB',
        abbreviation='hgobW',
        plugged='xntqT',
        background='xWrZk',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='j93xB',
        abbreviation='5Fidv',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='9bdZk',
        semester='6cRhy',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

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
    name_value = teaching_unit.name
    semester_value = teaching_unit.semester
    update_data = schemas.TeachingUnitUpdate(**{
        k: _updated_value(k, v)
        for k, v in teaching_unit_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_teaching_unit = crud.teaching_unit.update(
        db=db, db_obj=teaching_unit, obj_in=update_data
    )

    # Assertions
    assert updated_teaching_unit.id == teaching_unit.id
    assert updated_teaching_unit.name != name_value
    assert updated_teaching_unit.semester != semester_value


def test_get_teaching_unit(db: Session):
    """Test get operation for TeachingUnit."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='ctBqv',
        slug='CV63p',
        abbreviation='8Vlso',
        plugged='Ss603',
        background='C2Dqo',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='VrgpF',
        abbreviation='IVAbs',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='uBiY5',
        semester='LOde2',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Get all records
    records = crud.teaching_unit.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == teaching_unit.id for r in records)


def test_get_by_id_teaching_unit(db: Session):
    """Test get_by_id operation for TeachingUnit."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='BQchA',
        slug='4wQg5',
        abbreviation='ow0qS',
        plugged='2j9RH',
        background='UGp3o',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='8ghVt',
        abbreviation='0ZKPP',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='PLvL9',
        semester='loVGd',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Get by ID
    retrieved_teaching_unit = crud.teaching_unit.get(db=db, id=teaching_unit.id)

    # Assertions
    assert retrieved_teaching_unit is not None
    assert retrieved_teaching_unit.id == teaching_unit.id
    assert retrieved_teaching_unit.name == teaching_unit.name
    assert retrieved_teaching_unit.semester == teaching_unit.semester
    assert retrieved_teaching_unit.id_journey == teaching_unit.id_journey


def test_delete_teaching_unit(db: Session):
    """Test delete operation for TeachingUnit."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='qMW95',
        slug='PCNs9',
        abbreviation='20YS4',
        plugged='iu0rT',
        background='0ytnA',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='DUfol',
        abbreviation='nbgqA',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='6m1LV',
        semester='MCxvk',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Delete record
    deleted_teaching_unit = crud.teaching_unit.remove(db=db, id=teaching_unit.id)

    # Assertions
    assert deleted_teaching_unit is not None
    assert deleted_teaching_unit.id == teaching_unit.id

    # Verify deletion
    assert crud.teaching_unit.get(db=db, id=teaching_unit.id) is None

# begin #
# ---write your code here--- #
# end #

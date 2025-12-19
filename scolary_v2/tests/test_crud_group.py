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
"""Tests for CRUD operations on Group model."""


def test_create_group(db: Session):
    """Test create operation for Group."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='lTPkw',
        slug='6q17Q',
        abbreviation='nAd8T',
        plugged='7B4gS',
        background='l5Wk9',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='Nr5su',
        abbreviation='WV2Nj',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for Group
    group_data = schemas.GroupCreate(
        id_journey=journey.id,
        semester='NqvsK',
        group_number=4,
        student_count=5,
    )

    group = crud.group.create(db=db, obj_in=group_data)

    # Assertions
    assert group.id is not None
    assert group.id_journey == group_data.id_journey
    assert group.semester == group_data.semester
    assert group.group_number == group_data.group_number
    assert group.student_count == group_data.student_count


def test_update_group(db: Session):
    """Test update operation for Group."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='DCpB2',
        slug='ylDFE',
        abbreviation='zelLM',
        plugged='kBYnu',
        background='qaWKT',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='BSRyq',
        abbreviation='2HdlX',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for Group
    group_data = schemas.GroupCreate(
        id_journey=journey.id,
        semester='32E7I',
        group_number=19,
        student_count=17,
    )

    group = crud.group.create(db=db, obj_in=group_data)

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
    semester_value = group.semester
    group_number_value = group.group_number
    student_count_value = group.student_count
    update_data = schemas.GroupUpdate(**{
        k: _updated_value(k, v)
        for k, v in group_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_group = crud.group.update(
        db=db, db_obj=group, obj_in=update_data
    )

    # Assertions
    assert updated_group.id == group.id
    assert updated_group.semester != semester_value
    assert updated_group.group_number != group_number_value
    assert updated_group.student_count != student_count_value


def test_get_group(db: Session):
    """Test get operation for Group."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='ZKI6f',
        slug='9mIaK',
        abbreviation='C3U4B',
        plugged='pPzAf',
        background='HDfgE',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='OvieX',
        abbreviation='MrcwA',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for Group
    group_data = schemas.GroupCreate(
        id_journey=journey.id,
        semester='qAiTj',
        group_number=1,
        student_count=9,
    )

    group = crud.group.create(db=db, obj_in=group_data)

    # Get all records
    records = crud.group.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == group.id for r in records)


def test_get_by_id_group(db: Session):
    """Test get_by_id operation for Group."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='KJkly',
        slug='4PXLS',
        abbreviation='SST01',
        plugged='bTbjR',
        background='WOzo8',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='NzXUl',
        abbreviation='7Vrpw',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for Group
    group_data = schemas.GroupCreate(
        id_journey=journey.id,
        semester='w0MlF',
        group_number=19,
        student_count=6,
    )

    group = crud.group.create(db=db, obj_in=group_data)

    # Get by ID
    retrieved_group = crud.group.get(db=db, id=group.id)

    # Assertions
    assert retrieved_group is not None
    assert retrieved_group.id == group.id
    assert retrieved_group.id_journey == group.id_journey
    assert retrieved_group.semester == group.semester
    assert retrieved_group.group_number == group.group_number
    assert retrieved_group.student_count == group.student_count


def test_delete_group(db: Session):
    """Test delete operation for Group."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='oj5Ua',
        slug='3vwIi',
        abbreviation='vjUNw',
        plugged='VNJb0',
        background='R0f4u',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='WkQbR',
        abbreviation='HBgkj',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for Group
    group_data = schemas.GroupCreate(
        id_journey=journey.id,
        semester='oqCw8',
        group_number=4,
        student_count=8,
    )

    group = crud.group.create(db=db, obj_in=group_data)

    # Delete record
    deleted_group = crud.group.remove(db=db, id=group.id)

    # Assertions
    assert deleted_group is not None
    assert deleted_group.id == group.id

    # Verify deletion
    assert crud.group.get(db=db, id=group.id) is None

# begin #
# ---write your code here--- #
# end #

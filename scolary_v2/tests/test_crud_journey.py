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
"""Tests for CRUD operations on Journey model."""


def test_create_journey(db: Session):
    """Test create operation for Journey."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='LDBSN',
        slug='ePLW2',
        abbreviation='1NSrT',
        plugged='9WI7U',
        background='aK1tV',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='GN1tX',
        abbreviation='WbZCF',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Assertions
    assert journey.id is not None
    assert journey.name == journey_data.name
    assert journey.abbreviation == journey_data.abbreviation
    assert journey.id_mention == journey_data.id_mention


def test_update_journey(db: Session):
    """Test update operation for Journey."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='5TCHI',
        slug='A5HHp',
        abbreviation='xM8YX',
        plugged='Y97zZ',
        background='QiIKX',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='GRDn9',
        abbreviation='H7buw',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

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
    name_value = journey.name
    abbreviation_value = journey.abbreviation
    update_data = schemas.JourneyUpdate(**{
        k: _updated_value(k, v)
        for k, v in journey_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_journey = crud.journey.update(
        db=db, db_obj=journey, obj_in=update_data
    )

    # Assertions
    assert updated_journey.id == journey.id
    assert updated_journey.name != name_value
    assert updated_journey.abbreviation != abbreviation_value


def test_get_journey(db: Session):
    """Test get operation for Journey."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='GTvz6',
        slug='2KlgW',
        abbreviation='ZmpGt',
        plugged='FupsB',
        background='eWu4C',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='b5Wty',
        abbreviation='4EU8l',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Get all records
    records = crud.journey.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == journey.id for r in records)


def test_get_by_id_journey(db: Session):
    """Test get_by_id operation for Journey."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='09x0g',
        slug='S6xyc',
        abbreviation='X23GB',
        plugged='PoZHG',
        background='HQsiv',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='h5DmS',
        abbreviation='8Lp8V',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Get by ID
    retrieved_journey = crud.journey.get(db=db, id=journey.id)

    # Assertions
    assert retrieved_journey is not None
    assert retrieved_journey.id == journey.id
    assert retrieved_journey.name == journey.name
    assert retrieved_journey.abbreviation == journey.abbreviation
    assert retrieved_journey.id_mention == journey.id_mention


def test_delete_journey(db: Session):
    """Test delete operation for Journey."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='8Vgsi',
        slug='i4wji',
        abbreviation='ecH7d',
        plugged='yMFmg',
        background='pirff',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='Spi9e',
        abbreviation='uzlwp',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Delete record
    deleted_journey = crud.journey.remove(db=db, id=journey.id)

    # Assertions
    assert deleted_journey is not None
    assert deleted_journey.id == journey.id

    # Verify deletion
    assert crud.journey.get(db=db, id=journey.id) is None

# begin #
# ---write your code here--- #
# end #

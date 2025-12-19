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
"""Tests for CRUD operations on ConstituentElement model."""


def test_create_constituent_element(db: Session):
    """Test create operation for ConstituentElement."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='W34jl',
        slug='2LWYF',
        abbreviation='q3VfI',
        plugged='czykM',
        background='pNZ9j',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='w3VW1',
        abbreviation='cq15m',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='m28ko',
        semester='Hqulu',
        id_journey=journey.id,
        color='vHDJE',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Assertions
    assert constituent_element.id is not None
    assert constituent_element.name == constituent_element_data.name
    assert constituent_element.semester == constituent_element_data.semester
    assert constituent_element.id_journey == constituent_element_data.id_journey
    assert constituent_element.color == constituent_element_data.color


def test_update_constituent_element(db: Session):
    """Test update operation for ConstituentElement."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='PDMMt',
        slug='moLni',
        abbreviation='t2Ytm',
        plugged='nxSib',
        background='YtQk6',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='2RAQl',
        abbreviation='Zg9fe',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='1GS9E',
        semester='gZx8h',
        id_journey=journey.id,
        color='Myuli',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

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
    name_value = constituent_element.name
    semester_value = constituent_element.semester
    color_value = constituent_element.color
    update_data = schemas.ConstituentElementUpdate(**{
        k: _updated_value(k, v)
        for k, v in constituent_element_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_constituent_element = crud.constituent_element.update(
        db=db, db_obj=constituent_element, obj_in=update_data
    )

    # Assertions
    assert updated_constituent_element.id == constituent_element.id
    assert updated_constituent_element.name != name_value
    assert updated_constituent_element.semester != semester_value
    assert updated_constituent_element.color != color_value


def test_get_constituent_element(db: Session):
    """Test get operation for ConstituentElement."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='WK6Gu',
        slug='5kcsQ',
        abbreviation='YrW0R',
        plugged='aJYe5',
        background='VWCMX',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='FuunL',
        abbreviation='ZidIW',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='uxRBK',
        semester='Blczl',
        id_journey=journey.id,
        color='SeItZ',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Get all records
    records = crud.constituent_element.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == constituent_element.id for r in records)


def test_get_by_id_constituent_element(db: Session):
    """Test get_by_id operation for ConstituentElement."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='x1t5R',
        slug='FQ6JC',
        abbreviation='R9XVD',
        plugged='CnucF',
        background='4W57P',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='dQLu4',
        abbreviation='kVVrB',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='tGwmA',
        semester='PupbA',
        id_journey=journey.id,
        color='r90T0',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Get by ID
    retrieved_constituent_element = crud.constituent_element.get(db=db, id=constituent_element.id)

    # Assertions
    assert retrieved_constituent_element is not None
    assert retrieved_constituent_element.id == constituent_element.id
    assert retrieved_constituent_element.name == constituent_element.name
    assert retrieved_constituent_element.semester == constituent_element.semester
    assert retrieved_constituent_element.id_journey == constituent_element.id_journey
    assert retrieved_constituent_element.color == constituent_element.color


def test_delete_constituent_element(db: Session):
    """Test delete operation for ConstituentElement."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='v8xmf',
        slug='Fra77',
        abbreviation='UyK9t',
        plugged='olY6L',
        background='zdLLb',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='z84zA',
        abbreviation='1qBnI',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='ma2hr',
        semester='gZciq',
        id_journey=journey.id,
        color='wwDf5',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Delete record
    deleted_constituent_element = crud.constituent_element.remove(db=db, id=constituent_element.id)

    # Assertions
    assert deleted_constituent_element is not None
    assert deleted_constituent_element.id == constituent_element.id

    # Verify deletion
    assert crud.constituent_element.get(db=db, id=constituent_element.id) is None

# begin #
# ---write your code here--- #
# end #

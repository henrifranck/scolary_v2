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
"""Tests for CRUD operations on Mention model."""


def test_create_mention(db: Session):
    """Test create operation for Mention."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='tUYuP',
        slug='eSWns',
        abbreviation='8VmHq',
        plugged='y6LbN',
        background='4BbWs',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Assertions
    assert mention.id is not None
    assert mention.name == mention_data.name
    assert mention.slug == mention_data.slug
    assert mention.abbreviation == mention_data.abbreviation
    assert mention.plugged == mention_data.plugged
    assert mention.background == mention_data.background


def test_update_mention(db: Session):
    """Test update operation for Mention."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='A1f2D',
        slug='dlkJu',
        abbreviation='CPTy8',
        plugged='HW9Bg',
        background='GVLaq',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

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
    name_value = mention.name
    slug_value = mention.slug
    abbreviation_value = mention.abbreviation
    plugged_value = mention.plugged
    background_value = mention.background
    update_data = schemas.MentionUpdate(**{
        k: _updated_value(k, v)
        for k, v in mention_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_mention = crud.mention.update(
        db=db, db_obj=mention, obj_in=update_data
    )

    # Assertions
    assert updated_mention.id == mention.id
    assert updated_mention.name != name_value
    assert updated_mention.slug != slug_value
    assert updated_mention.abbreviation != abbreviation_value
    assert updated_mention.plugged != plugged_value
    assert updated_mention.background != background_value


def test_get_mention(db: Session):
    """Test get operation for Mention."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='oON1z',
        slug='CyNc4',
        abbreviation='DFqRE',
        plugged='vyFKB',
        background='a4W1V',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Get all records
    records = crud.mention.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == mention.id for r in records)


def test_get_by_id_mention(db: Session):
    """Test get_by_id operation for Mention."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='Lds2o',
        slug='vZjah',
        abbreviation='IH5NY',
        plugged='mLk06',
        background='UvNQs',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Get by ID
    retrieved_mention = crud.mention.get(db=db, id=mention.id)

    # Assertions
    assert retrieved_mention is not None
    assert retrieved_mention.id == mention.id
    assert retrieved_mention.name == mention.name
    assert retrieved_mention.slug == mention.slug
    assert retrieved_mention.abbreviation == mention.abbreviation
    assert retrieved_mention.plugged == mention.plugged
    assert retrieved_mention.background == mention.background


def test_delete_mention(db: Session):
    """Test delete operation for Mention."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='UCD9f',
        slug='o8qUY',
        abbreviation='jG1WG',
        plugged='Sijzx',
        background='w0fG8',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Delete record
    deleted_mention = crud.mention.remove(db=db, id=mention.id)

    # Assertions
    assert deleted_mention is not None
    assert deleted_mention.id == mention.id

    # Verify deletion
    assert crud.mention.get(db=db, id=mention.id) is None

# begin #
# ---write your code here--- #
# end #

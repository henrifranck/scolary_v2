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
"""Tests for CRUD operations on UserMention model."""


def test_create_user_mention(db: Session):
    """Test create operation for UserMention."""
    # Test data for User
    user_data = schemas.UserCreate(
        email='N8q2j@xb4e1.com',
        first_name='Z7J8R',
        last_name='ceFQM',
        password='FP2wj',
        is_superuser=False,
        picture='SstZt',
        is_active=False,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='XvQoI',
        slug='xwjQu',
        abbreviation='fgB6C',
        plugged='XZ5oX',
        background='Yy9Ev',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for UserMention
    user_mention_data = schemas.UserMentionCreate(
        id_user=user.id,
        id_mention=mention.id,
    )

    user_mention = crud.user_mention.create(db=db, obj_in=user_mention_data)

    # Assertions
    assert user_mention.id is not None
    assert user_mention.id_user == user_mention_data.id_user
    assert user_mention.id_mention == user_mention_data.id_mention


def test_update_user_mention(db: Session):
    """Test update operation for UserMention."""
    # Test data for User
    user_data = schemas.UserCreate(
        email='Sf59v@0focm.com',
        first_name='WbTfy',
        last_name='rDNCF',
        password='Zf2zc',
        is_superuser=False,
        picture='KYfGJ',
        is_active=True,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='poNoA',
        slug='vXlTR',
        abbreviation='bGw8p',
        plugged='80UNU',
        background='vr0Aw',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for UserMention
    user_mention_data = schemas.UserMentionCreate(
        id_user=user.id,
        id_mention=mention.id,
    )

    user_mention = crud.user_mention.create(db=db, obj_in=user_mention_data)

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
    update_data = schemas.UserMentionUpdate(**{
        k: _updated_value(k, v)
        for k, v in user_mention_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_user_mention = crud.user_mention.update(
        db=db, db_obj=user_mention, obj_in=update_data
    )

    # Assertions
    assert updated_user_mention.id == user_mention.id


def test_get_user_mention(db: Session):
    """Test get operation for UserMention."""
    # Test data for User
    user_data = schemas.UserCreate(
        email='vOtil@u7git.com',
        first_name='jGDGs',
        last_name='pW4Oq',
        password='zy2QZ',
        is_superuser=False,
        picture='Pzip1',
        is_active=True,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='HDufr',
        slug='uY5Ty',
        abbreviation='4q40h',
        plugged='JJe9u',
        background='x93bs',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for UserMention
    user_mention_data = schemas.UserMentionCreate(
        id_user=user.id,
        id_mention=mention.id,
    )

    user_mention = crud.user_mention.create(db=db, obj_in=user_mention_data)

    # Get all records
    records = crud.user_mention.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == user_mention.id for r in records)


def test_get_by_id_user_mention(db: Session):
    """Test get_by_id operation for UserMention."""
    # Test data for User
    user_data = schemas.UserCreate(
        email='xkD5n@lbxab.com',
        first_name='64Ur5',
        last_name='GTQEm',
        password='orE6w',
        is_superuser=False,
        picture='gCuTG',
        is_active=False,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='Twsa2',
        slug='7a8Cj',
        abbreviation='Jxxhi',
        plugged='e7shg',
        background='gfvTj',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for UserMention
    user_mention_data = schemas.UserMentionCreate(
        id_user=user.id,
        id_mention=mention.id,
    )

    user_mention = crud.user_mention.create(db=db, obj_in=user_mention_data)

    # Get by ID
    retrieved_user_mention = crud.user_mention.get(db=db, id=user_mention.id)

    # Assertions
    assert retrieved_user_mention is not None
    assert retrieved_user_mention.id == user_mention.id
    assert retrieved_user_mention.id_user == user_mention.id_user
    assert retrieved_user_mention.id_mention == user_mention.id_mention


def test_delete_user_mention(db: Session):
    """Test delete operation for UserMention."""
    # Test data for User
    user_data = schemas.UserCreate(
        email='WFQm6@vue5p.com',
        first_name='geAuV',
        last_name='a52fD',
        password='FQEu4',
        is_superuser=True,
        picture='yZ5XY',
        is_active=True,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='IU7Nm',
        slug='mnxDy',
        abbreviation='XCGQD',
        plugged='8LxLp',
        background='pM3Hj',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for UserMention
    user_mention_data = schemas.UserMentionCreate(
        id_user=user.id,
        id_mention=mention.id,
    )

    user_mention = crud.user_mention.create(db=db, obj_in=user_mention_data)

    # Delete record
    deleted_user_mention = crud.user_mention.remove(db=db, id=user_mention.id)

    # Assertions
    assert deleted_user_mention is not None
    assert deleted_user_mention.id == user_mention.id

    # Verify deletion
    assert crud.user_mention.get(db=db, id=user_mention.id) is None

# begin #
# ---write your code here--- #
# end #

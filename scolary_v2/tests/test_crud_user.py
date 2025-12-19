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
"""Tests for CRUD operations on User model."""


def test_create_user(db: Session):
    """Test create operation for User."""
    # Test data for User
    user_data = schemas.UserCreate(
        email='CMZ3C@lumw4.com',
        first_name='0G6zR',
        last_name='z3ZrB',
        password='9GEfR',
        is_superuser=True,
        picture='MWIdD',
        is_active=True,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Assertions
    assert user.id is not None
    assert user.email == user_data.email
    assert user.first_name == user_data.first_name
    assert user.last_name == user_data.last_name
    assert user.is_superuser == user_data.is_superuser
    assert user.picture == user_data.picture
    assert user.is_active == user_data.is_active


def test_update_user(db: Session):
    """Test update operation for User."""
    # Test data for User
    user_data = schemas.UserCreate(
        email='SJuyv@d7agh.com',
        first_name='OAIcP',
        last_name='JWlWi',
        password='th92p',
        is_superuser=False,
        picture='ZxTWn',
        is_active=True,
    )

    user = crud.user.create(db=db, obj_in=user_data)

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
    email_value = user.email
    first_name_value = user.first_name
    last_name_value = user.last_name
    is_superuser_value = user.is_superuser
    picture_value = user.picture
    is_active_value = user.is_active
    update_data = schemas.UserUpdate(**{
        k: _updated_value(k, v)
        for k, v in user_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_user = crud.user.update(
        db=db, db_obj=user, obj_in=update_data
    )

    # Assertions
    assert updated_user.id == user.id
    assert updated_user.email != email_value
    assert updated_user.first_name != first_name_value
    assert updated_user.last_name != last_name_value
    assert updated_user.is_superuser != is_superuser_value
    assert updated_user.picture != picture_value
    assert updated_user.is_active != is_active_value


def test_get_user(db: Session):
    """Test get operation for User."""
    # Test data for User
    user_data = schemas.UserCreate(
        email='xodYd@7rl19.com',
        first_name='xxr0G',
        last_name='7pWKR',
        password='6TrfL',
        is_superuser=False,
        picture='K3J7r',
        is_active=False,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Get all records
    records = crud.user.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == user.id for r in records)


def test_get_by_id_user(db: Session):
    """Test get_by_id operation for User."""
    # Test data for User
    user_data = schemas.UserCreate(
        email='tCqQA@ykxcg.com',
        first_name='4sTEh',
        last_name='SJzTN',
        password='E6D7g',
        is_superuser=True,
        picture='ucxz7',
        is_active=True,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Get by ID
    retrieved_user = crud.user.get(db=db, id=user.id)

    # Assertions
    assert retrieved_user is not None
    assert retrieved_user.id == user.id
    assert retrieved_user.email == user.email
    assert retrieved_user.first_name == user.first_name
    assert retrieved_user.last_name == user.last_name
    assert retrieved_user.is_superuser == user.is_superuser
    assert retrieved_user.picture == user.picture
    assert retrieved_user.is_active == user.is_active


def test_delete_user(db: Session):
    """Test delete operation for User."""
    # Test data for User
    user_data = schemas.UserCreate(
        email='k4Sw0@xtnxr.com',
        first_name='mTy0I',
        last_name='C8kdS',
        password='UYRal',
        is_superuser=False,
        picture='XvMvJ',
        is_active=True,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Delete record
    deleted_user = crud.user.remove(db=db, id=user.id)

    # Assertions
    assert deleted_user is not None
    assert deleted_user.id == user.id

    # Verify deletion
    assert crud.user.get(db=db, id=user.id) is None

# begin #
# ---write your code here--- #
# end #

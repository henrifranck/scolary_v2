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
"""Tests for CRUD operations on UserRole model."""


def test_create_user_role(db: Session):
    """Test create operation for UserRole."""
    # Test data for User
    user_data = schemas.UserCreate(
        email='HQCCl@i53od.com',
        first_name='GUa1Q',
        last_name='AaDy8',
        password='otJNK',
        is_superuser=False,
        picture='Ooakh',
        is_active=False,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Role
    role_data = schemas.RoleCreate(
        name='8tCTq',
    )

    role = crud.role.create(db=db, obj_in=role_data)

    # Test data for UserRole
    user_role_data = schemas.UserRoleCreate(
        id_user=user.id,
        id_role=role.id,
    )

    user_role = crud.user_role.create(db=db, obj_in=user_role_data)

    # Assertions
    assert user_role.id is not None
    assert user_role.id_user == user_role_data.id_user
    assert user_role.id_role == user_role_data.id_role


def test_update_user_role(db: Session):
    """Test update operation for UserRole."""
    # Test data for User
    user_data = schemas.UserCreate(
        email='Ayj3A@8ggoq.com',
        first_name='KNKZn',
        last_name='iOF5J',
        password='EtUg7',
        is_superuser=False,
        picture='N4MSA',
        is_active=False,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Role
    role_data = schemas.RoleCreate(
        name='bYAzc',
    )

    role = crud.role.create(db=db, obj_in=role_data)

    # Test data for UserRole
    user_role_data = schemas.UserRoleCreate(
        id_user=user.id,
        id_role=role.id,
    )

    user_role = crud.user_role.create(db=db, obj_in=user_role_data)

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
    update_data = schemas.UserRoleUpdate(**{
        k: _updated_value(k, v)
        for k, v in user_role_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_user_role = crud.user_role.update(
        db=db, db_obj=user_role, obj_in=update_data
    )

    # Assertions
    assert updated_user_role.id == user_role.id


def test_get_user_role(db: Session):
    """Test get operation for UserRole."""
    # Test data for User
    user_data = schemas.UserCreate(
        email='6wfdG@6tmar.com',
        first_name='hxLCj',
        last_name='2kmKr',
        password='ANJf8',
        is_superuser=True,
        picture='QNzeH',
        is_active=True,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Role
    role_data = schemas.RoleCreate(
        name='6S66I',
    )

    role = crud.role.create(db=db, obj_in=role_data)

    # Test data for UserRole
    user_role_data = schemas.UserRoleCreate(
        id_user=user.id,
        id_role=role.id,
    )

    user_role = crud.user_role.create(db=db, obj_in=user_role_data)

    # Get all records
    records = crud.user_role.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == user_role.id for r in records)


def test_get_by_id_user_role(db: Session):
    """Test get_by_id operation for UserRole."""
    # Test data for User
    user_data = schemas.UserCreate(
        email='0ZwVo@qxrg9.com',
        first_name='9PTzQ',
        last_name='SoApx',
        password='kkAJR',
        is_superuser=True,
        picture='SZAXq',
        is_active=True,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Role
    role_data = schemas.RoleCreate(
        name='E1sRR',
    )

    role = crud.role.create(db=db, obj_in=role_data)

    # Test data for UserRole
    user_role_data = schemas.UserRoleCreate(
        id_user=user.id,
        id_role=role.id,
    )

    user_role = crud.user_role.create(db=db, obj_in=user_role_data)

    # Get by ID
    retrieved_user_role = crud.user_role.get(db=db, id=user_role.id)

    # Assertions
    assert retrieved_user_role is not None
    assert retrieved_user_role.id == user_role.id
    assert retrieved_user_role.id_user == user_role.id_user
    assert retrieved_user_role.id_role == user_role.id_role


def test_delete_user_role(db: Session):
    """Test delete operation for UserRole."""
    # Test data for User
    user_data = schemas.UserCreate(
        email='oePQK@yv8xi.com',
        first_name='LXBXD',
        last_name='u6vIE',
        password='6ODUt',
        is_superuser=True,
        picture='ZjlcY',
        is_active=False,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    # Test data for Role
    role_data = schemas.RoleCreate(
        name='if2kg',
    )

    role = crud.role.create(db=db, obj_in=role_data)

    # Test data for UserRole
    user_role_data = schemas.UserRoleCreate(
        id_user=user.id,
        id_role=role.id,
    )

    user_role = crud.user_role.create(db=db, obj_in=user_role_data)

    # Delete record
    deleted_user_role = crud.user_role.remove(db=db, id=user_role.id)

    # Assertions
    assert deleted_user_role is not None
    assert deleted_user_role.id == user_role.id

    # Verify deletion
    assert crud.user_role.get(db=db, id=user_role.id) is None

# begin #
# ---write your code here--- #
# end #

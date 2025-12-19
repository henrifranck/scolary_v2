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
"""Tests for CRUD operations on Permission model."""


def test_create_permission(db: Session):
    """Test create operation for Permission."""
    # Test data for Permission
    permission_data = schemas.PermissionCreate(
        name='zK0GS',
        method='qj9MV',
        model_name='iK92r',
    )

    permission = crud.permission.create(db=db, obj_in=permission_data)

    # Assertions
    assert permission.id is not None
    assert permission.name == permission_data.name
    assert permission.method == permission_data.method
    assert permission.model_name == permission_data.model_name


def test_update_permission(db: Session):
    """Test update operation for Permission."""
    # Test data for Permission
    permission_data = schemas.PermissionCreate(
        name='FK6Dt',
        method='i9WUD',
        model_name='KG7fI',
    )

    permission = crud.permission.create(db=db, obj_in=permission_data)

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
    name_value = permission.name
    method_value = permission.method
    model_name_value = permission.model_name
    update_data = schemas.PermissionUpdate(**{
        k: _updated_value(k, v)
        for k, v in permission_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_permission = crud.permission.update(
        db=db, db_obj=permission, obj_in=update_data
    )

    # Assertions
    assert updated_permission.id == permission.id
    assert updated_permission.name != name_value
    assert updated_permission.method != method_value
    assert updated_permission.model_name != model_name_value


def test_get_permission(db: Session):
    """Test get operation for Permission."""
    # Test data for Permission
    permission_data = schemas.PermissionCreate(
        name='YDDG2',
        method='TlFkz',
        model_name='6OSWP',
    )

    permission = crud.permission.create(db=db, obj_in=permission_data)

    # Get all records
    records = crud.permission.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == permission.id for r in records)


def test_get_by_id_permission(db: Session):
    """Test get_by_id operation for Permission."""
    # Test data for Permission
    permission_data = schemas.PermissionCreate(
        name='lT3a0',
        method='WseiF',
        model_name='mZXiJ',
    )

    permission = crud.permission.create(db=db, obj_in=permission_data)

    # Get by ID
    retrieved_permission = crud.permission.get(db=db, id=permission.id)

    # Assertions
    assert retrieved_permission is not None
    assert retrieved_permission.id == permission.id
    assert retrieved_permission.name == permission.name
    assert retrieved_permission.method == permission.method
    assert retrieved_permission.model_name == permission.model_name


def test_delete_permission(db: Session):
    """Test delete operation for Permission."""
    # Test data for Permission
    permission_data = schemas.PermissionCreate(
        name='Qb6RZ',
        method='mcei3',
        model_name='E8OGb',
    )

    permission = crud.permission.create(db=db, obj_in=permission_data)

    # Delete record
    deleted_permission = crud.permission.remove(db=db, id=permission.id)

    # Assertions
    assert deleted_permission is not None
    assert deleted_permission.id == permission.id

    # Verify deletion
    assert crud.permission.get(db=db, id=permission.id) is None

# begin #
# ---write your code here--- #
# end #

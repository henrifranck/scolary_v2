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
"""Tests for CRUD operations on RolePermission model."""


def test_create_role_permission(db: Session):
    """Test create operation for RolePermission."""
    # Test data for Role
    role_data = schemas.RoleCreate(
        name='vM18z',
    )

    role = crud.role.create(db=db, obj_in=role_data)

    # Test data for Permission
    permission_data = schemas.PermissionCreate(
        name='KYJ9G',
        method='QjPXT',
        model_name='qzBXg',
    )

    permission = crud.permission.create(db=db, obj_in=permission_data)

    # Test data for RolePermission
    role_permission_data = schemas.RolePermissionCreate(
        id_role=role.id,
        id_permission=permission.id,
    )

    role_permission = crud.role_permission.create(db=db, obj_in=role_permission_data)

    # Assertions
    assert role_permission.id is not None
    assert role_permission.id_role == role_permission_data.id_role
    assert role_permission.id_permission == role_permission_data.id_permission


def test_update_role_permission(db: Session):
    """Test update operation for RolePermission."""
    # Test data for Role
    role_data = schemas.RoleCreate(
        name='7ZJic',
    )

    role = crud.role.create(db=db, obj_in=role_data)

    # Test data for Permission
    permission_data = schemas.PermissionCreate(
        name='iG3mD',
        method='elPUp',
        model_name='B0J5D',
    )

    permission = crud.permission.create(db=db, obj_in=permission_data)

    # Test data for RolePermission
    role_permission_data = schemas.RolePermissionCreate(
        id_role=role.id,
        id_permission=permission.id,
    )

    role_permission = crud.role_permission.create(db=db, obj_in=role_permission_data)

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
    update_data = schemas.RolePermissionUpdate(**{
        k: _updated_value(k, v)
        for k, v in role_permission_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_role_permission = crud.role_permission.update(
        db=db, db_obj=role_permission, obj_in=update_data
    )

    # Assertions
    assert updated_role_permission.id == role_permission.id


def test_get_role_permission(db: Session):
    """Test get operation for RolePermission."""
    # Test data for Role
    role_data = schemas.RoleCreate(
        name='VLvHF',
    )

    role = crud.role.create(db=db, obj_in=role_data)

    # Test data for Permission
    permission_data = schemas.PermissionCreate(
        name='hhWTw',
        method='pVWwc',
        model_name='A6TC3',
    )

    permission = crud.permission.create(db=db, obj_in=permission_data)

    # Test data for RolePermission
    role_permission_data = schemas.RolePermissionCreate(
        id_role=role.id,
        id_permission=permission.id,
    )

    role_permission = crud.role_permission.create(db=db, obj_in=role_permission_data)

    # Get all records
    records = crud.role_permission.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == role_permission.id for r in records)


def test_get_by_id_role_permission(db: Session):
    """Test get_by_id operation for RolePermission."""
    # Test data for Role
    role_data = schemas.RoleCreate(
        name='JS2nE',
    )

    role = crud.role.create(db=db, obj_in=role_data)

    # Test data for Permission
    permission_data = schemas.PermissionCreate(
        name='ZlbHp',
        method='JOA1T',
        model_name='c8FaX',
    )

    permission = crud.permission.create(db=db, obj_in=permission_data)

    # Test data for RolePermission
    role_permission_data = schemas.RolePermissionCreate(
        id_role=role.id,
        id_permission=permission.id,
    )

    role_permission = crud.role_permission.create(db=db, obj_in=role_permission_data)

    # Get by ID
    retrieved_role_permission = crud.role_permission.get(db=db, id=role_permission.id)

    # Assertions
    assert retrieved_role_permission is not None
    assert retrieved_role_permission.id == role_permission.id
    assert retrieved_role_permission.id_role == role_permission.id_role
    assert retrieved_role_permission.id_permission == role_permission.id_permission


def test_delete_role_permission(db: Session):
    """Test delete operation for RolePermission."""
    # Test data for Role
    role_data = schemas.RoleCreate(
        name='7uFKR',
    )

    role = crud.role.create(db=db, obj_in=role_data)

    # Test data for Permission
    permission_data = schemas.PermissionCreate(
        name='6o6pO',
        method='JEkFt',
        model_name='AlzXh',
    )

    permission = crud.permission.create(db=db, obj_in=permission_data)

    # Test data for RolePermission
    role_permission_data = schemas.RolePermissionCreate(
        id_role=role.id,
        id_permission=permission.id,
    )

    role_permission = crud.role_permission.create(db=db, obj_in=role_permission_data)

    # Delete record
    deleted_role_permission = crud.role_permission.remove(db=db, id=role_permission.id)

    # Assertions
    assert deleted_role_permission is not None
    assert deleted_role_permission.id == role_permission.id

    # Verify deletion
    assert crud.role_permission.get(db=db, id=role_permission.id) is None

# begin #
# ---write your code here--- #
# end #

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
"""Tests for CRUD operations on Role model."""


def test_create_role(db: Session):
    """Test create operation for Role."""
    # Test data for Role
    role_data = schemas.RoleCreate(
        name='hhaEL',
    )

    role = crud.role.create(db=db, obj_in=role_data)

    # Assertions
    assert role.id is not None
    assert role.name == role_data.name


def test_update_role(db: Session):
    """Test update operation for Role."""
    # Test data for Role
    role_data = schemas.RoleCreate(
        name='jTOtM',
    )

    role = crud.role.create(db=db, obj_in=role_data)

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
    name_value = role.name
    update_data = schemas.RoleUpdate(**{
        k: _updated_value(k, v)
        for k, v in role_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_role = crud.role.update(
        db=db, db_obj=role, obj_in=update_data
    )

    # Assertions
    assert updated_role.id == role.id
    assert updated_role.name != name_value


def test_get_role(db: Session):
    """Test get operation for Role."""
    # Test data for Role
    role_data = schemas.RoleCreate(
        name='n3rwy',
    )

    role = crud.role.create(db=db, obj_in=role_data)

    # Get all records
    records = crud.role.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == role.id for r in records)


def test_get_by_id_role(db: Session):
    """Test get_by_id operation for Role."""
    # Test data for Role
    role_data = schemas.RoleCreate(
        name='J8BX9',
    )

    role = crud.role.create(db=db, obj_in=role_data)

    # Get by ID
    retrieved_role = crud.role.get(db=db, id=role.id)

    # Assertions
    assert retrieved_role is not None
    assert retrieved_role.id == role.id
    assert retrieved_role.name == role.name


def test_delete_role(db: Session):
    """Test delete operation for Role."""
    # Test data for Role
    role_data = schemas.RoleCreate(
        name='ghMZz',
    )

    role = crud.role.create(db=db, obj_in=role_data)

    # Delete record
    deleted_role = crud.role.remove(db=db, id=role.id)

    # Assertions
    assert deleted_role is not None
    assert deleted_role.id == role.id

    # Verify deletion
    assert crud.role.get(db=db, id=role.id) is None

# begin #
# ---write your code here--- #
# end #

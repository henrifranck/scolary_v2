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
"""Tests for CRUD operations on Classroom model."""


def test_create_classroom(db: Session):
    """Test create operation for Classroom."""
    # Test data for Classroom
    classroom_data = schemas.ClassroomCreate(
        name='Gf3Is',
        capacity=16,
    )

    classroom = crud.classroom.create(db=db, obj_in=classroom_data)

    # Assertions
    assert classroom.id is not None
    assert classroom.name == classroom_data.name
    assert classroom.capacity == classroom_data.capacity


def test_update_classroom(db: Session):
    """Test update operation for Classroom."""
    # Test data for Classroom
    classroom_data = schemas.ClassroomCreate(
        name='3uHq5',
        capacity=14,
    )

    classroom = crud.classroom.create(db=db, obj_in=classroom_data)

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
    name_value = classroom.name
    capacity_value = classroom.capacity
    update_data = schemas.ClassroomUpdate(**{
        k: _updated_value(k, v)
        for k, v in classroom_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_classroom = crud.classroom.update(
        db=db, db_obj=classroom, obj_in=update_data
    )

    # Assertions
    assert updated_classroom.id == classroom.id
    assert updated_classroom.name != name_value
    assert updated_classroom.capacity != capacity_value


def test_get_classroom(db: Session):
    """Test get operation for Classroom."""
    # Test data for Classroom
    classroom_data = schemas.ClassroomCreate(
        name='iXccU',
        capacity=20,
    )

    classroom = crud.classroom.create(db=db, obj_in=classroom_data)

    # Get all records
    records = crud.classroom.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == classroom.id for r in records)


def test_get_by_id_classroom(db: Session):
    """Test get_by_id operation for Classroom."""
    # Test data for Classroom
    classroom_data = schemas.ClassroomCreate(
        name='xgKFZ',
        capacity=10,
    )

    classroom = crud.classroom.create(db=db, obj_in=classroom_data)

    # Get by ID
    retrieved_classroom = crud.classroom.get(db=db, id=classroom.id)

    # Assertions
    assert retrieved_classroom is not None
    assert retrieved_classroom.id == classroom.id
    assert retrieved_classroom.name == classroom.name
    assert retrieved_classroom.capacity == classroom.capacity


def test_delete_classroom(db: Session):
    """Test delete operation for Classroom."""
    # Test data for Classroom
    classroom_data = schemas.ClassroomCreate(
        name='43W1G',
        capacity=4,
    )

    classroom = crud.classroom.create(db=db, obj_in=classroom_data)

    # Delete record
    deleted_classroom = crud.classroom.remove(db=db, id=classroom.id)

    # Assertions
    assert deleted_classroom is not None
    assert deleted_classroom.id == classroom.id

    # Verify deletion
    assert crud.classroom.get(db=db, id=classroom.id) is None

# begin #
# ---write your code here--- #
# end #

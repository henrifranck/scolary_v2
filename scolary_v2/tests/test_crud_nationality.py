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
"""Tests for CRUD operations on Nationality model."""


def test_create_nationality(db: Session):
    """Test create operation for Nationality."""
    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='olBn8',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Assertions
    assert nationality.id is not None
    assert nationality.name == nationality_data.name


def test_update_nationality(db: Session):
    """Test update operation for Nationality."""
    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='RZovU',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

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
    name_value = nationality.name
    update_data = schemas.NationalityUpdate(**{
        k: _updated_value(k, v)
        for k, v in nationality_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_nationality = crud.nationality.update(
        db=db, db_obj=nationality, obj_in=update_data
    )

    # Assertions
    assert updated_nationality.id == nationality.id
    assert updated_nationality.name != name_value


def test_get_nationality(db: Session):
    """Test get operation for Nationality."""
    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='8tPIM',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Get all records
    records = crud.nationality.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == nationality.id for r in records)


def test_get_by_id_nationality(db: Session):
    """Test get_by_id operation for Nationality."""
    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='ozjJk',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Get by ID
    retrieved_nationality = crud.nationality.get(db=db, id=nationality.id)

    # Assertions
    assert retrieved_nationality is not None
    assert retrieved_nationality.id == nationality.id
    assert retrieved_nationality.name == nationality.name


def test_delete_nationality(db: Session):
    """Test delete operation for Nationality."""
    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='Y0GU2',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Delete record
    deleted_nationality = crud.nationality.remove(db=db, id=nationality.id)

    # Assertions
    assert deleted_nationality is not None
    assert deleted_nationality.id == nationality.id

    # Verify deletion
    assert crud.nationality.get(db=db, id=nationality.id) is None

# begin #
# ---write your code here--- #
# end #

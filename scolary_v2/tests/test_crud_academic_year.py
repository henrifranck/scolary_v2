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
"""Tests for CRUD operations on AcademicYear model."""


def test_create_academic_year(db: Session):
    """Test create operation for AcademicYear."""
    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='oFYT9',
        code='M1oKY',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Assertions
    assert academic_year.id is not None
    assert academic_year.name == academic_year_data.name
    assert academic_year.code == academic_year_data.code


def test_update_academic_year(db: Session):
    """Test update operation for AcademicYear."""
    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='42cPZ',
        code='diX4C',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

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
    name_value = academic_year.name
    code_value = academic_year.code
    update_data = schemas.AcademicYearUpdate(**{
        k: _updated_value(k, v)
        for k, v in academic_year_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_academic_year = crud.academic_year.update(
        db=db, db_obj=academic_year, obj_in=update_data
    )

    # Assertions
    assert updated_academic_year.id == academic_year.id
    assert updated_academic_year.name != name_value
    assert updated_academic_year.code != code_value


def test_get_academic_year(db: Session):
    """Test get operation for AcademicYear."""
    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='iUxIE',
        code='EeaYL',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Get all records
    records = crud.academic_year.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == academic_year.id for r in records)


def test_get_by_id_academic_year(db: Session):
    """Test get_by_id operation for AcademicYear."""
    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='ylcob',
        code='WUnQb',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Get by ID
    retrieved_academic_year = crud.academic_year.get(db=db, id=academic_year.id)

    # Assertions
    assert retrieved_academic_year is not None
    assert retrieved_academic_year.id == academic_year.id
    assert retrieved_academic_year.name == academic_year.name
    assert retrieved_academic_year.code == academic_year.code


def test_delete_academic_year(db: Session):
    """Test delete operation for AcademicYear."""
    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='rcFWw',
        code='LM1U9',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Delete record
    deleted_academic_year = crud.academic_year.remove(db=db, id=academic_year.id)

    # Assertions
    assert deleted_academic_year is not None
    assert deleted_academic_year.id == academic_year.id

    # Verify deletion
    assert crud.academic_year.get(db=db, id=academic_year.id) is None

# begin #
# ---write your code here--- #
# end #

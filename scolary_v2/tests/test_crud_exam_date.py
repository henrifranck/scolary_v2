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
"""Tests for CRUD operations on ExamDate model."""


def test_create_exam_date(db: Session):
    """Test create operation for ExamDate."""
    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='g6vh7',
        code='yVyxV',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for ExamDate
    exam_date_data = schemas.ExamDateCreate(
        id_academic_year=academic_year.id,
        date_from='2025-11-15',
        date_to='2025-11-15',
        session='wxhcU',
    )

    exam_date = crud.exam_date.create(db=db, obj_in=exam_date_data)

    # Assertions
    assert exam_date.id is not None
    assert exam_date.id_academic_year == exam_date_data.id_academic_year
    assert exam_date.date_from == exam_date_data.date_from
    assert exam_date.date_to == exam_date_data.date_to
    assert exam_date.session == exam_date_data.session


def test_update_exam_date(db: Session):
    """Test update operation for ExamDate."""
    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='8HBur',
        code='GEOwi',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for ExamDate
    exam_date_data = schemas.ExamDateCreate(
        id_academic_year=academic_year.id,
        date_from='2025-11-15',
        date_to='2025-11-15',
        session='1X7Mx',
    )

    exam_date = crud.exam_date.create(db=db, obj_in=exam_date_data)

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
        if k in ['date_from', 'date_to'] and isinstance(v, str):
            return (date.fromisoformat(v) + timedelta(days=1)).isoformat()
        if k in ['date_from', 'date_to'] and isinstance(v, date):
            return v + timedelta(days=1)

        # time +1 hour
        if k in [] and isinstance(v, str):
            return (datetime.strptime(v, '%H:%M:%S') + timedelta(hours=1)).time().strftime('%H:%M:%S')
        if k in [] and isinstance(v, time):
            return (datetime.combine(date.today(), v) + timedelta(hours=1)).time()

        # fallback -> prefix 'updated_'
        return f'updated_{v}'

    # Update data
    date_from_value = exam_date.date_from
    date_to_value = exam_date.date_to
    session_value = exam_date.session
    update_data = schemas.ExamDateUpdate(**{
        k: _updated_value(k, v)
        for k, v in exam_date_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_exam_date = crud.exam_date.update(
        db=db, db_obj=exam_date, obj_in=update_data
    )

    # Assertions
    assert updated_exam_date.id == exam_date.id
    assert updated_exam_date.date_from != date_from_value
    assert updated_exam_date.date_to != date_to_value
    assert updated_exam_date.session != session_value


def test_get_exam_date(db: Session):
    """Test get operation for ExamDate."""
    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='uBKGX',
        code='VOd6s',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for ExamDate
    exam_date_data = schemas.ExamDateCreate(
        id_academic_year=academic_year.id,
        date_from='2025-11-15',
        date_to='2025-11-15',
        session='5UX2O',
    )

    exam_date = crud.exam_date.create(db=db, obj_in=exam_date_data)

    # Get all records
    records = crud.exam_date.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == exam_date.id for r in records)


def test_get_by_id_exam_date(db: Session):
    """Test get_by_id operation for ExamDate."""
    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='xvvjB',
        code='hzF9a',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for ExamDate
    exam_date_data = schemas.ExamDateCreate(
        id_academic_year=academic_year.id,
        date_from='2025-11-15',
        date_to='2025-11-15',
        session='C4Gi9',
    )

    exam_date = crud.exam_date.create(db=db, obj_in=exam_date_data)

    # Get by ID
    retrieved_exam_date = crud.exam_date.get(db=db, id=exam_date.id)

    # Assertions
    assert retrieved_exam_date is not None
    assert retrieved_exam_date.id == exam_date.id
    assert retrieved_exam_date.id_academic_year == exam_date.id_academic_year
    assert retrieved_exam_date.date_from == exam_date.date_from
    assert retrieved_exam_date.date_to == exam_date.date_to
    assert retrieved_exam_date.session == exam_date.session


def test_delete_exam_date(db: Session):
    """Test delete operation for ExamDate."""
    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='gwZo5',
        code='iCG3e',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for ExamDate
    exam_date_data = schemas.ExamDateCreate(
        id_academic_year=academic_year.id,
        date_from='2025-11-15',
        date_to='2025-11-15',
        session='aYLEl',
    )

    exam_date = crud.exam_date.create(db=db, obj_in=exam_date_data)

    # Delete record
    deleted_exam_date = crud.exam_date.remove(db=db, id=exam_date.id)

    # Assertions
    assert deleted_exam_date is not None
    assert deleted_exam_date.id == exam_date.id

    # Verify deletion
    assert crud.exam_date.get(db=db, id=exam_date.id) is None

# begin #
# ---write your code here--- #
# end #

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
"""Tests for CRUD operations on BaccalaureateSerie model."""


def test_create_baccalaureate_serie(db: Session):
    """Test create operation for BaccalaureateSerie."""
    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='3zdL8',
        value='tJZAm',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Assertions
    assert baccalaureate_serie.id is not None
    assert baccalaureate_serie.name == baccalaureate_serie_data.name
    assert baccalaureate_serie.value == baccalaureate_serie_data.value


def test_update_baccalaureate_serie(db: Session):
    """Test update operation for BaccalaureateSerie."""
    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='Bvan3',
        value='OyK0r',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

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
    name_value = baccalaureate_serie.name
    value_value = baccalaureate_serie.value
    update_data = schemas.BaccalaureateSerieUpdate(**{
        k: _updated_value(k, v)
        for k, v in baccalaureate_serie_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_baccalaureate_serie = crud.baccalaureate_serie.update(
        db=db, db_obj=baccalaureate_serie, obj_in=update_data
    )

    # Assertions
    assert updated_baccalaureate_serie.id == baccalaureate_serie.id
    assert updated_baccalaureate_serie.name != name_value
    assert updated_baccalaureate_serie.value != value_value


def test_get_baccalaureate_serie(db: Session):
    """Test get operation for BaccalaureateSerie."""
    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='Z2vud',
        value='hLSgq',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Get all records
    records = crud.baccalaureate_serie.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == baccalaureate_serie.id for r in records)


def test_get_by_id_baccalaureate_serie(db: Session):
    """Test get_by_id operation for BaccalaureateSerie."""
    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='4EXsc',
        value='A4qVy',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Get by ID
    retrieved_baccalaureate_serie = crud.baccalaureate_serie.get(db=db, id=baccalaureate_serie.id)

    # Assertions
    assert retrieved_baccalaureate_serie is not None
    assert retrieved_baccalaureate_serie.id == baccalaureate_serie.id
    assert retrieved_baccalaureate_serie.name == baccalaureate_serie.name
    assert retrieved_baccalaureate_serie.value == baccalaureate_serie.value


def test_delete_baccalaureate_serie(db: Session):
    """Test delete operation for BaccalaureateSerie."""
    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='db3DN',
        value='n18Sw',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Delete record
    deleted_baccalaureate_serie = crud.baccalaureate_serie.remove(db=db, id=baccalaureate_serie.id)

    # Assertions
    assert deleted_baccalaureate_serie is not None
    assert deleted_baccalaureate_serie.id == baccalaureate_serie.id

    # Verify deletion
    assert crud.baccalaureate_serie.get(db=db, id=baccalaureate_serie.id) is None

# begin #
# ---write your code here--- #
# end #

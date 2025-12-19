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
"""Tests for CRUD operations on Feature model."""


def test_create_feature(db: Session):
    """Test create operation for Feature."""
    # Test data for Feature
    feature_data = schemas.FeatureCreate(
        name='IqJ0h',
        description='gRYLf4bCm2Uz02zyKwdWFOw1wHgiQJHRxQ446vrC9G',
    )

    feature = crud.feature.create(db=db, obj_in=feature_data)

    # Assertions
    assert feature.id is not None
    assert feature.name == feature_data.name
    assert feature.description == feature_data.description


def test_update_feature(db: Session):
    """Test update operation for Feature."""
    # Test data for Feature
    feature_data = schemas.FeatureCreate(
        name='3OAZ5',
        description='2vM4yjjNv0Hi5pfgPV0vncTJkUsWxAr',
    )

    feature = crud.feature.create(db=db, obj_in=feature_data)

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
    name_value = feature.name
    description_value = feature.description
    update_data = schemas.FeatureUpdate(**{
        k: _updated_value(k, v)
        for k, v in feature_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_feature = crud.feature.update(
        db=db, db_obj=feature, obj_in=update_data
    )

    # Assertions
    assert updated_feature.id == feature.id
    assert updated_feature.name != name_value
    assert updated_feature.description != description_value


def test_get_feature(db: Session):
    """Test get operation for Feature."""
    # Test data for Feature
    feature_data = schemas.FeatureCreate(
        name='7sawl',
        description='dAoe',
    )

    feature = crud.feature.create(db=db, obj_in=feature_data)

    # Get all records
    records = crud.feature.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == feature.id for r in records)


def test_get_by_id_feature(db: Session):
    """Test get_by_id operation for Feature."""
    # Test data for Feature
    feature_data = schemas.FeatureCreate(
        name='P1VYS',
        description='1Mf5yp8xHPzlG3CuuPRnYZx1vFSj04B5dCdbFAAsPVwaGPslTcy383aLMh9lqgnUtbRMah',
    )

    feature = crud.feature.create(db=db, obj_in=feature_data)

    # Get by ID
    retrieved_feature = crud.feature.get(db=db, id=feature.id)

    # Assertions
    assert retrieved_feature is not None
    assert retrieved_feature.id == feature.id
    assert retrieved_feature.name == feature.name
    assert retrieved_feature.description == feature.description


def test_delete_feature(db: Session):
    """Test delete operation for Feature."""
    # Test data for Feature
    feature_data = schemas.FeatureCreate(
        name='I4inH',
        description='v38w2zB0mNKMrMtMQsfcKKRj6WX7DcaMVIsrLapACynRIgwCVLzlDpJiTIn',
    )

    feature = crud.feature.create(db=db, obj_in=feature_data)

    # Delete record
    deleted_feature = crud.feature.remove(db=db, id=feature.id)

    # Assertions
    assert deleted_feature is not None
    assert deleted_feature.id == feature.id

    # Verify deletion
    assert crud.feature.get(db=db, id=feature.id) is None

# begin #
# ---write your code here--- #
# end #

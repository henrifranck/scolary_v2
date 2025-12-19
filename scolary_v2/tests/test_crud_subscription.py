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
"""Tests for CRUD operations on Subscription model."""


def test_create_subscription(db: Session):
    """Test create operation for Subscription."""
    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='PT4Bt',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

    # Assertions
    assert subscription.id is not None
    assert subscription.name == subscription_data.name


def test_update_subscription(db: Session):
    """Test update operation for Subscription."""
    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='If1Wf',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

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
    name_value = subscription.name
    update_data = schemas.SubscriptionUpdate(**{
        k: _updated_value(k, v)
        for k, v in subscription_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_subscription = crud.subscription.update(
        db=db, db_obj=subscription, obj_in=update_data
    )

    # Assertions
    assert updated_subscription.id == subscription.id
    assert updated_subscription.name != name_value


def test_get_subscription(db: Session):
    """Test get operation for Subscription."""
    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='xVemm',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

    # Get all records
    records = crud.subscription.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == subscription.id for r in records)


def test_get_by_id_subscription(db: Session):
    """Test get_by_id operation for Subscription."""
    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='dJpiH',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

    # Get by ID
    retrieved_subscription = crud.subscription.get(db=db, id=subscription.id)

    # Assertions
    assert retrieved_subscription is not None
    assert retrieved_subscription.id == subscription.id
    assert retrieved_subscription.name == subscription.name


def test_delete_subscription(db: Session):
    """Test delete operation for Subscription."""
    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='I4n92',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

    # Delete record
    deleted_subscription = crud.subscription.remove(db=db, id=subscription.id)

    # Assertions
    assert deleted_subscription is not None
    assert deleted_subscription.id == subscription.id

    # Verify deletion
    assert crud.subscription.get(db=db, id=subscription.id) is None

# begin #
# ---write your code here--- #
# end #

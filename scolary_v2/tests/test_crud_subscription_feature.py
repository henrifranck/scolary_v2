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
"""Tests for CRUD operations on SubscriptionFeature model."""


def test_create_subscription_feature(db: Session):
    """Test create operation for SubscriptionFeature."""
    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='Ot7JI',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

    # Test data for Feature
    feature_data = schemas.FeatureCreate(
        name='bHses',
        description='vBg0c9yNK4oGQ4NTnJ2qij36Yvn0GcOkaULpkPeGa9FQ',
    )

    feature = crud.feature.create(db=db, obj_in=feature_data)

    # Test data for SubscriptionFeature
    subscription_feature_data = schemas.SubscriptionFeatureCreate(
        id_subscription=subscription.id,
        id_feature=feature.id,
    )

    subscription_feature = crud.subscription_feature.create(db=db, obj_in=subscription_feature_data)

    # Assertions
    assert subscription_feature.id is not None
    assert subscription_feature.id_subscription == subscription_feature_data.id_subscription
    assert subscription_feature.id_feature == subscription_feature_data.id_feature


def test_update_subscription_feature(db: Session):
    """Test update operation for SubscriptionFeature."""
    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='gAc5v',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

    # Test data for Feature
    feature_data = schemas.FeatureCreate(
        name='NjKKc',
        description='0shyx1TRKLNeORZaCyno0ycbWxVyAaB67ECcMIBYTOHBNWAfLDWId1byRE1YrK',
    )

    feature = crud.feature.create(db=db, obj_in=feature_data)

    # Test data for SubscriptionFeature
    subscription_feature_data = schemas.SubscriptionFeatureCreate(
        id_subscription=subscription.id,
        id_feature=feature.id,
    )

    subscription_feature = crud.subscription_feature.create(db=db, obj_in=subscription_feature_data)

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
    update_data = schemas.SubscriptionFeatureUpdate(**{
        k: _updated_value(k, v)
        for k, v in subscription_feature_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_subscription_feature = crud.subscription_feature.update(
        db=db, db_obj=subscription_feature, obj_in=update_data
    )

    # Assertions
    assert updated_subscription_feature.id == subscription_feature.id


def test_get_subscription_feature(db: Session):
    """Test get operation for SubscriptionFeature."""
    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='AZVub',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

    # Test data for Feature
    feature_data = schemas.FeatureCreate(
        name='tW7cV',
        description='ID7rVoSPNQKMrh5RwtgI3UeTcwvAJJ5',
    )

    feature = crud.feature.create(db=db, obj_in=feature_data)

    # Test data for SubscriptionFeature
    subscription_feature_data = schemas.SubscriptionFeatureCreate(
        id_subscription=subscription.id,
        id_feature=feature.id,
    )

    subscription_feature = crud.subscription_feature.create(db=db, obj_in=subscription_feature_data)

    # Get all records
    records = crud.subscription_feature.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == subscription_feature.id for r in records)


def test_get_by_id_subscription_feature(db: Session):
    """Test get_by_id operation for SubscriptionFeature."""
    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='RpSXw',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

    # Test data for Feature
    feature_data = schemas.FeatureCreate(
        name='fX0LI',
        description='oBELLMlMPpawSm',
    )

    feature = crud.feature.create(db=db, obj_in=feature_data)

    # Test data for SubscriptionFeature
    subscription_feature_data = schemas.SubscriptionFeatureCreate(
        id_subscription=subscription.id,
        id_feature=feature.id,
    )

    subscription_feature = crud.subscription_feature.create(db=db, obj_in=subscription_feature_data)

    # Get by ID
    retrieved_subscription_feature = crud.subscription_feature.get(db=db, id=subscription_feature.id)

    # Assertions
    assert retrieved_subscription_feature is not None
    assert retrieved_subscription_feature.id == subscription_feature.id
    assert retrieved_subscription_feature.id_subscription == subscription_feature.id_subscription
    assert retrieved_subscription_feature.id_feature == subscription_feature.id_feature


def test_delete_subscription_feature(db: Session):
    """Test delete operation for SubscriptionFeature."""
    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='BrHgs',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

    # Test data for Feature
    feature_data = schemas.FeatureCreate(
        name='z5SKd',
        description='KZ3SJI4STD55GjLDzWcYWP1wpBDwn3vy20FysuxrEzQCw9navA3kSr2GKaACJ',
    )

    feature = crud.feature.create(db=db, obj_in=feature_data)

    # Test data for SubscriptionFeature
    subscription_feature_data = schemas.SubscriptionFeatureCreate(
        id_subscription=subscription.id,
        id_feature=feature.id,
    )

    subscription_feature = crud.subscription_feature.create(db=db, obj_in=subscription_feature_data)

    # Delete record
    deleted_subscription_feature = crud.subscription_feature.remove(db=db, id=subscription_feature.id)

    # Assertions
    assert deleted_subscription_feature is not None
    assert deleted_subscription_feature.id == subscription_feature.id

    # Verify deletion
    assert crud.subscription_feature.get(db=db, id=subscription_feature.id) is None

# begin #
# ---write your code here--- #
# end #

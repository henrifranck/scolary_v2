# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_subscription_feature_api(client, db):
    """Create SubscriptionFeature via API."""
    # Auth setup
    user_data = {
        'email': 'Fi5TN@lfb02.com',
        'last_name': '9xlxC',
        'password': 'x9JLU',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='Ef5bi',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

    # Test data for Feature
    feature_data = schemas.FeatureCreate(
        name='sH1dx',
        description='NEZo',
    )

    feature = crud.feature.create(db=db, obj_in=feature_data)

    subscription_feature_data = {
        'id_subscription': subscription.id,
        'id_feature': feature.id,
    }

    resp = client.post('/api/v1/subscription_features/', json=subscription_feature_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['id_subscription'] == subscription_feature_data['id_subscription']
    assert created['id_feature'] == subscription_feature_data['id_feature']


def test_update_subscription_feature_api(client, db):
    """Update SubscriptionFeature via API."""
    # Auth setup
    user_data = {
        'email': '4O56B@pfpi8.com',
        'last_name': 'q69n0',
        'password': 'bykdR',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='T0XFZ',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

    # Test data for Feature
    feature_data = schemas.FeatureCreate(
        name='Du64T',
        description='bOksWmDPJQhkDrVEVuqiHWlOB4387OBK',
    )

    feature = crud.feature.create(db=db, obj_in=feature_data)

    subscription_feature_data = {
        'id_subscription': subscription.id,
        'id_feature': feature.id,
    }

    # Precompute enum values for update
    enum_values_map = {}

    # Helper to compute a new value different from the current one (for API payload)
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
            current = v
            values = enum_values_map[k]
            try:
                idx = values.index(current)
                if len(values) > 1:
                    return values[(idx + 1) % len(values)]
                else:
                    return current
            except ValueError:
                # si la valeur actuelle n'est pas dans la liste, prendre la première
                return values[0] if values else v

        # datetime +1 jour
        if k in []:
            if isinstance(v, str):
                return (datetime.fromisoformat(v) + timedelta(days=1)).isoformat()
            return v

        # date +1 jour
        if k in []:
            if isinstance(v, str):
                return (date.fromisoformat(v) + timedelta(days=1)).isoformat()
            return v

        # time +1 heure
        if k in []:
            if isinstance(v, str):
                return (datetime.strptime(v, '%H:%M:%S') + timedelta(hours=1)).time().strftime('%H:%M:%S')
            return v

        # fallback -> prefix 'updated_'
        return f'updated_{v}'

    resp_c = client.post('/api/v1/subscription_features/', json=subscription_feature_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = ['id_subscription', 'id_feature']

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in subscription_feature_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/subscription_features/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']


def test_get_subscription_feature_api(client, db):
    """Get SubscriptionFeature via API."""
    # Auth setup
    user_data = {
        'email': 'VxF3s@dhcse.com',
        'last_name': 'WVHsL',
        'password': 'dp0Oy',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='OaNrn',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

    # Test data for Feature
    feature_data = schemas.FeatureCreate(
        name='fMJQb',
        description='STSyQlTQ7nRy6',
    )

    feature = crud.feature.create(db=db, obj_in=feature_data)

    subscription_feature_data = {
        'id_subscription': subscription.id,
        'id_feature': feature.id,
    }

    client.post('/api/v1/subscription_features/', json=subscription_feature_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/subscription_features/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_subscription_feature_api(client, db):
    """Get_by_id SubscriptionFeature via API."""
    # Auth setup
    user_data = {
        'email': 'i7ePI@8fjgz.com',
        'last_name': 'iGgVv',
        'password': 'so4fs',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='p3MjJ',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

    # Test data for Feature
    feature_data = schemas.FeatureCreate(
        name='6ZKry',
        description='trYU6Iezxi81BC6qg2ynCyrmsMqsDeeVtSc0v0fXckC3mpUUDVBQadYfl6sX',
    )

    feature = crud.feature.create(db=db, obj_in=feature_data)

    subscription_feature_data = {
        'id_subscription': subscription.id,
        'id_feature': feature.id,
    }

    resp_c = client.post('/api/v1/subscription_features/', json=subscription_feature_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/subscription_features/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_subscription_feature_api(client, db):
    """Delete SubscriptionFeature via API."""
    # Auth setup
    user_data = {
        'email': 'q4SFv@ceusq.com',
        'last_name': '6QbaX',
        'password': 'qhUYA',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='L5ABQ',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

    # Test data for Feature
    feature_data = schemas.FeatureCreate(
        name='rpLxq',
        description='dFKY9cD4khRyZcDXccgUXuounNwtdpbfLDLPuUSfZ1o4FhXp5X76GdDr1NFpuNLcEhCa1ty1rcUBcbS',
    )

    feature = crud.feature.create(db=db, obj_in=feature_data)

    subscription_feature_data = {
        'id_subscription': subscription.id,
        'id_feature': feature.id,
    }

    resp_c = client.post('/api/v1/subscription_features/', json=subscription_feature_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/subscription_features/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'SubscriptionFeature deleted successfully'
    resp_chk = client.get(f'/api/v1/subscription_features/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_subscription_api(client, db):
    """Create Subscription via API."""
    # Auth setup
    user_data = {
        'email': 'psmWA@rvzne.com',
        'last_name': 'BBbHP',
        'password': 'xanHT',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    subscription_data = {
        'name': 'NmvCj',
    }

    resp = client.post('/api/v1/subscriptions/', json=subscription_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['name'] == subscription_data['name']


def test_update_subscription_api(client, db):
    """Update Subscription via API."""
    # Auth setup
    user_data = {
        'email': 'x4AGG@ngf0c.com',
        'last_name': 'HjsaP',
        'password': 'gxJOm',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    subscription_data = {
        'name': 's4E7r',
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

    resp_c = client.post('/api/v1/subscriptions/', json=subscription_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = []

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in subscription_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/subscriptions/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['name'] == update_data['name']


def test_get_subscription_api(client, db):
    """Get Subscription via API."""
    # Auth setup
    user_data = {
        'email': 'ruD4n@oz1pl.com',
        'last_name': 'aml2Y',
        'password': 'hObvJ',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    subscription_data = {
        'name': 'flK0f',
    }

    client.post('/api/v1/subscriptions/', json=subscription_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/subscriptions/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_subscription_api(client, db):
    """Get_by_id Subscription via API."""
    # Auth setup
    user_data = {
        'email': '5Nluq@t1cvk.com',
        'last_name': '1pSAr',
        'password': 'p3egV',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    subscription_data = {
        'name': '1coLx',
    }

    resp_c = client.post('/api/v1/subscriptions/', json=subscription_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/subscriptions/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_subscription_api(client, db):
    """Delete Subscription via API."""
    # Auth setup
    user_data = {
        'email': 'JPAiu@llswq.com',
        'last_name': 'wvzgN',
        'password': 'ag49y',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    subscription_data = {
        'name': 'KN5If',
    }

    resp_c = client.post('/api/v1/subscriptions/', json=subscription_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/subscriptions/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'Subscription deleted successfully'
    resp_chk = client.get(f'/api/v1/subscriptions/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

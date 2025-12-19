# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_feature_api(client, db):
    """Create Feature via API."""
    # Auth setup
    user_data = {
        'email': 'wKk5v@g6jyw.com',
        'last_name': 'BNj5d',
        'password': 'aQBtJ',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    feature_data = {
        'name': 'ADjYe',
        'description': 'j9WrWPXJor14hcM6h03khvX2ktpy0wPnhnxvXCzm55DsKF0k96BvlRbsvA',
    }

    resp = client.post('/api/v1/features/', json=feature_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['name'] == feature_data['name']
    assert created['description'] == feature_data['description']


def test_update_feature_api(client, db):
    """Update Feature via API."""
    # Auth setup
    user_data = {
        'email': '11RvI@4wftt.com',
        'last_name': 'jaBWw',
        'password': '7q98V',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    feature_data = {
        'name': 'h5j9R',
        'description': 'b97XuILPUtymC8M',
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

    resp_c = client.post('/api/v1/features/', json=feature_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = []

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in feature_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/features/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['name'] == update_data['name']
    assert updated['description'] == update_data['description']


def test_get_feature_api(client, db):
    """Get Feature via API."""
    # Auth setup
    user_data = {
        'email': 'YWhRO@flx5b.com',
        'last_name': 'V2czw',
        'password': 'BLiRk',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    feature_data = {
        'name': 'sO8dZ',
        'description': 'VXhQhZB78jmXMweN3qZow4EPfpSkTZenqwr',
    }

    client.post('/api/v1/features/', json=feature_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/features/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_feature_api(client, db):
    """Get_by_id Feature via API."""
    # Auth setup
    user_data = {
        'email': 'LlRKW@7yglg.com',
        'last_name': 'hjGQ4',
        'password': 'RXEHG',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    feature_data = {
        'name': 'VqJIh',
        'description': '5Jhn5LCbN0j5owe6rxxO2b',
    }

    resp_c = client.post('/api/v1/features/', json=feature_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/features/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_feature_api(client, db):
    """Delete Feature via API."""
    # Auth setup
    user_data = {
        'email': 'BP4LB@sokep.com',
        'last_name': '6eBVG',
        'password': 'E7FO2',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    feature_data = {
        'name': 'nwQKo',
        'description': 'xu1q5f4Cx30RrSJMUIm9Y8jinTbodojUoXqRH0FwzQF8I6wtECp8fXqCfLSZD7o4g3aDuIRZCf92l9HA',
    }

    resp_c = client.post('/api/v1/features/', json=feature_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/features/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'Feature deleted successfully'
    resp_chk = client.get(f'/api/v1/features/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

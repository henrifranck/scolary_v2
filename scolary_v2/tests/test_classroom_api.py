# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_classroom_api(client, db):
    """Create Classroom via API."""
    # Auth setup
    user_data = {
        'email': 'ho8QB@yxhud.com',
        'last_name': 'EjW3d',
        'password': 'FxDmc',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    classroom_data = {
        'name': 'GbSVQ',
        'capacity': 5,
    }

    resp = client.post('/api/v1/classrooms/', json=classroom_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['name'] == classroom_data['name']
    assert created['capacity'] == classroom_data['capacity']


def test_update_classroom_api(client, db):
    """Update Classroom via API."""
    # Auth setup
    user_data = {
        'email': 'pho7D@9fsxj.com',
        'last_name': 'tRGjv',
        'password': 'xzPiC',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    classroom_data = {
        'name': 'VbNlO',
        'capacity': 14,
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

    resp_c = client.post('/api/v1/classrooms/', json=classroom_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = []

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in classroom_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/classrooms/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['name'] == update_data['name']
    assert updated['capacity'] == update_data['capacity']


def test_get_classroom_api(client, db):
    """Get Classroom via API."""
    # Auth setup
    user_data = {
        'email': 'fJ8vK@mqnqm.com',
        'last_name': 'Ak0Ri',
        'password': 'WDzEi',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    classroom_data = {
        'name': 'C2DM6',
        'capacity': 17,
    }

    client.post('/api/v1/classrooms/', json=classroom_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/classrooms/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_classroom_api(client, db):
    """Get_by_id Classroom via API."""
    # Auth setup
    user_data = {
        'email': 'L4D3i@h05dv.com',
        'last_name': 'WUK3y',
        'password': 'KWkIw',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    classroom_data = {
        'name': 'qrsvh',
        'capacity': 9,
    }

    resp_c = client.post('/api/v1/classrooms/', json=classroom_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/classrooms/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_classroom_api(client, db):
    """Delete Classroom via API."""
    # Auth setup
    user_data = {
        'email': 'TWf9i@5bv8u.com',
        'last_name': 'l3OFR',
        'password': 'rtLqW',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    classroom_data = {
        'name': 'jCHk9',
        'capacity': 12,
    }

    resp_c = client.post('/api/v1/classrooms/', json=classroom_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/classrooms/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'Classroom deleted successfully'
    resp_chk = client.get(f'/api/v1/classrooms/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_academic_year_api(client, db):
    """Create AcademicYear via API."""
    # Auth setup
    user_data = {
        'email': 'OdkuP@ltgv0.com',
        'last_name': 'fabie',
        'password': 'k52n5',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    academic_year_data = {
        'name': 'LQ66Z',
        'code': '22YUw',
    }

    resp = client.post('/api/v1/academic_years/', json=academic_year_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['name'] == academic_year_data['name']
    assert created['code'] == academic_year_data['code']


def test_update_academic_year_api(client, db):
    """Update AcademicYear via API."""
    # Auth setup
    user_data = {
        'email': 'R2Uyt@mf4gm.com',
        'last_name': 'CaUqV',
        'password': 's2Gt7',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    academic_year_data = {
        'name': 'ZNa31',
        'code': '00Xtf',
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

    resp_c = client.post('/api/v1/academic_years/', json=academic_year_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = []

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in academic_year_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/academic_years/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['name'] == update_data['name']
    assert updated['code'] == update_data['code']


def test_get_academic_year_api(client, db):
    """Get AcademicYear via API."""
    # Auth setup
    user_data = {
        'email': '1RMxF@deqji.com',
        'last_name': 'k4Nk8',
        'password': '3qwLR',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    academic_year_data = {
        'name': 'OFxpc',
        'code': 'JWCGm',
    }

    client.post('/api/v1/academic_years/', json=academic_year_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/academic_years/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_academic_year_api(client, db):
    """Get_by_id AcademicYear via API."""
    # Auth setup
    user_data = {
        'email': 'nBFMN@ubbtc.com',
        'last_name': '0Kl8V',
        'password': 'moaLw',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    academic_year_data = {
        'name': 'C4Zvn',
        'code': 'PQ4gA',
    }

    resp_c = client.post('/api/v1/academic_years/', json=academic_year_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/academic_years/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_academic_year_api(client, db):
    """Delete AcademicYear via API."""
    # Auth setup
    user_data = {
        'email': 'xO5t1@hojnq.com',
        'last_name': 'KngHf',
        'password': '9VT7a',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    academic_year_data = {
        'name': 'cJn1B',
        'code': '0iWeC',
    }

    resp_c = client.post('/api/v1/academic_years/', json=academic_year_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/academic_years/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'AcademicYear deleted successfully'
    resp_chk = client.get(f'/api/v1/academic_years/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

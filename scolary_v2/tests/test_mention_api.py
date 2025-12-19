# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_mention_api(client, db):
    """Create Mention via API."""
    # Auth setup
    user_data = {
        'email': 'xejwP@jvatt.com',
        'last_name': 'eoLwi',
        'password': 'Ut5YD',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    mention_data = {
        'name': 'teraN',
        'slug': 'ZYGfO',
        'abbreviation': 'jY623',
        'plugged': 'X7aWt',
        'background': 'E4jaJ',
    }

    resp = client.post('/api/v1/mentions/', json=mention_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['name'] == mention_data['name']
    assert created['slug'] == mention_data['slug']
    assert created['abbreviation'] == mention_data['abbreviation']
    assert created['plugged'] == mention_data['plugged']
    assert created['background'] == mention_data['background']


def test_update_mention_api(client, db):
    """Update Mention via API."""
    # Auth setup
    user_data = {
        'email': 'LLgex@whpvl.com',
        'last_name': 'EVbzy',
        'password': 'aaqZV',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    mention_data = {
        'name': '0yHRA',
        'slug': 'HVv2J',
        'abbreviation': 'rpMqf',
        'plugged': 'KpEth',
        'background': 'hcUOH',
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

    resp_c = client.post('/api/v1/mentions/', json=mention_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = []

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in mention_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/mentions/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['name'] == update_data['name']
    assert updated['slug'] == update_data['slug']
    assert updated['abbreviation'] == update_data['abbreviation']
    assert updated['plugged'] == update_data['plugged']
    assert updated['background'] == update_data['background']


def test_get_mention_api(client, db):
    """Get Mention via API."""
    # Auth setup
    user_data = {
        'email': 'sSGBs@nxuta.com',
        'last_name': 'iryn8',
        'password': 'a9NzF',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    mention_data = {
        'name': 'SPlRS',
        'slug': 'Dph3e',
        'abbreviation': '3s0oz',
        'plugged': 'uEcG1',
        'background': 'RTPxs',
    }

    client.post('/api/v1/mentions/', json=mention_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/mentions/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_mention_api(client, db):
    """Get_by_id Mention via API."""
    # Auth setup
    user_data = {
        'email': 'Tp9SU@ptmvf.com',
        'last_name': '9RFi4',
        'password': 'FUktn',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    mention_data = {
        'name': 'XTd52',
        'slug': 'hlYsr',
        'abbreviation': 'JiN0E',
        'plugged': 'sjGMf',
        'background': 'xHYrU',
    }

    resp_c = client.post('/api/v1/mentions/', json=mention_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/mentions/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_mention_api(client, db):
    """Delete Mention via API."""
    # Auth setup
    user_data = {
        'email': '4HPa7@ljpjp.com',
        'last_name': 'Flt74',
        'password': '2WtNJ',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    mention_data = {
        'name': '45sAH',
        'slug': 'eMZcM',
        'abbreviation': 'tGMPB',
        'plugged': 'hokt3',
        'background': 'WdgR7',
    }

    resp_c = client.post('/api/v1/mentions/', json=mention_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/mentions/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'Mention deleted successfully'
    resp_chk = client.get(f'/api/v1/mentions/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

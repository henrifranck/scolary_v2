# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_university_api(client, db):
    """Create University via API."""
    # Auth setup
    user_data = {
        'email': 'Lp9k3@bwt3r.com',
        'last_name': 'fAxx4',
        'password': 'YC8RH',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    university_data = {
        'province': 'GEnZr',
        'department_name': 'XC1If',
        'department_other_information': 'bgfON',
        'department_address': 'yWKZ2H',
        'email': 'TVVu1@gyf0p.com',
        'logo_university': 'kSNvX',
        'logo_departement': 'v5RSR',
        'phone_number': '399xp',
        'admin_signature': 'm3n2s',
    }

    resp = client.post('/api/v1/universitys/', json=university_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['province'] == university_data['province']
    assert created['department_name'] == university_data['department_name']
    assert created['department_other_information'] == university_data['department_other_information']
    assert created['department_address'] == university_data['department_address']
    assert created['email'] == university_data['email']
    assert created['logo_university'] == university_data['logo_university']
    assert created['logo_departement'] == university_data['logo_departement']
    assert created['phone_number'] == university_data['phone_number']
    assert created['admin_signature'] == university_data['admin_signature']


def test_update_university_api(client, db):
    """Update University via API."""
    # Auth setup
    user_data = {
        'email': 'Fz7Rw@ajshz.com',
        'last_name': 'bc19O',
        'password': 'T7M5x',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    university_data = {
        'province': '2CDag',
        'department_name': '0cWct',
        'department_other_information': 'H2qmI',
        'department_address': 'kZdx9w5J4CJPpNKac1Fx1miw6sRUj0Ohz8VbZU5lJDFFdCAm7ERF6td4ynJS6lmG41AYGxKkJEaLK4Q3uTtYQGGYiq1j2',
        'email': 'qTYkL@rhdwi.com',
        'logo_university': 'cMltZ',
        'logo_departement': 'hrCHA',
        'phone_number': 'X0682',
        'admin_signature': 'ZpubZ',
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

    resp_c = client.post('/api/v1/universitys/', json=university_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = []

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in university_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/universitys/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['province'] == update_data['province']
    assert updated['department_name'] == update_data['department_name']
    assert updated['department_other_information'] == update_data['department_other_information']
    assert updated['department_address'] == update_data['department_address']
    assert updated['email'] == update_data['email']
    assert updated['logo_university'] == update_data['logo_university']
    assert updated['logo_departement'] == update_data['logo_departement']
    assert updated['phone_number'] == update_data['phone_number']
    assert updated['admin_signature'] == update_data['admin_signature']


def test_get_university_api(client, db):
    """Get University via API."""
    # Auth setup
    user_data = {
        'email': 'rtfiw@gzowm.com',
        'last_name': 'pHi4v',
        'password': 'jUM2j',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    university_data = {
        'province': 'h4pdZ',
        'department_name': 'amGqW',
        'department_other_information': 'Znsm4',
        'department_address': 'YfUJlf2VvUYg5yOI2FCa2PVizgq9RS6uH4pEzRLc11PIiybm19CnJO2iEu4aeWx6D0q',
        'email': '44FVm@yiynp.com',
        'logo_university': 'oDli0',
        'logo_departement': 'EySkQ',
        'phone_number': 'HWWOB',
        'admin_signature': 'HtI4d',
    }

    client.post('/api/v1/universitys/', json=university_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/universitys/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_university_api(client, db):
    """Get_by_id University via API."""
    # Auth setup
    user_data = {
        'email': 'JBnrU@upcg8.com',
        'last_name': 'RqZM2',
        'password': 'U8msC',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    university_data = {
        'province': 'TlZlK',
        'department_name': 'IJ4hi',
        'department_other_information': '17Eic',
        'department_address': 'dkYQ5l6klilRrjPkBbgrNR3Xmf3qh1OAfsB',
        'email': '0fwMi@uc1zo.com',
        'logo_university': 'Ij4E6',
        'logo_departement': 'a5sbl',
        'phone_number': 'WKGle',
        'admin_signature': 'b18C4',
    }

    resp_c = client.post('/api/v1/universitys/', json=university_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/universitys/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_university_api(client, db):
    """Delete University via API."""
    # Auth setup
    user_data = {
        'email': 'SRUWj@grghj.com',
        'last_name': '3lCep',
        'password': 'CytNN',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    university_data = {
        'province': '243lO',
        'department_name': '3ohdg',
        'department_other_information': 'tDJ0f',
        'department_address': 'k6PhbvjvDuxSqQfpbmf9HPNTCFpJPU7Td7vNgBSMF0E83pviY2qK2sjNjxYavEz4I92DfZgReqU1K1zKjsGhLUd4upuF8',
        'email': 'vPgQu@q8m7c.com',
        'logo_university': 'E08lw',
        'logo_departement': 'yLCov',
        'phone_number': 'EzaXi',
        'admin_signature': 'C7IZO',
    }

    resp_c = client.post('/api/v1/universitys/', json=university_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/universitys/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'University deleted successfully'
    resp_chk = client.get(f'/api/v1/universitys/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

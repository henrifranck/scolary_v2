# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_journey_api(client, db):
    """Create Journey via API."""
    # Auth setup
    user_data = {
        'email': 'WMXaT@6xaca.com',
        'last_name': 'tt4kd',
        'password': 'NGoiH',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='g2qyt',
        slug='K5sdY',
        abbreviation='4WafS',
        plugged='7XtDj',
        background='KJOoY',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    journey_data = {
        'name': 'xaVGj',
        'abbreviation': 'nC0Ak',
        'id_mention': mention.id,
    }

    resp = client.post('/api/v1/journeys/', json=journey_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['name'] == journey_data['name']
    assert created['abbreviation'] == journey_data['abbreviation']
    assert created['id_mention'] == journey_data['id_mention']


def test_update_journey_api(client, db):
    """Update Journey via API."""
    # Auth setup
    user_data = {
        'email': '2MJNF@cgjp9.com',
        'last_name': 'GDfP6',
        'password': '6TgAk',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='C93qf',
        slug='3CWWZ',
        abbreviation='nCsak',
        plugged='uvoKg',
        background='wd9LK',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    journey_data = {
        'name': 'FSAdg',
        'abbreviation': 'Eevtn',
        'id_mention': mention.id,
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

    resp_c = client.post('/api/v1/journeys/', json=journey_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = ['id_mention']

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in journey_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/journeys/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['name'] == update_data['name']
    assert updated['abbreviation'] == update_data['abbreviation']


def test_get_journey_api(client, db):
    """Get Journey via API."""
    # Auth setup
    user_data = {
        'email': '4zYS1@vouxr.com',
        'last_name': 'Sto01',
        'password': 'FC0St',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='NKLMa',
        slug='afGZl',
        abbreviation='B7NDX',
        plugged='xAQRN',
        background='UI8bo',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    journey_data = {
        'name': '8G3Wt',
        'abbreviation': 'Lor9B',
        'id_mention': mention.id,
    }

    client.post('/api/v1/journeys/', json=journey_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/journeys/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_journey_api(client, db):
    """Get_by_id Journey via API."""
    # Auth setup
    user_data = {
        'email': 'atsmp@nsora.com',
        'last_name': 'rk9Am',
        'password': 'mCSy9',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='HVHBT',
        slug='jJzH0',
        abbreviation='wWGps',
        plugged='ol44x',
        background='2UxYI',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    journey_data = {
        'name': 'fNjkP',
        'abbreviation': 'hwidf',
        'id_mention': mention.id,
    }

    resp_c = client.post('/api/v1/journeys/', json=journey_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/journeys/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_journey_api(client, db):
    """Delete Journey via API."""
    # Auth setup
    user_data = {
        'email': 'X8O9l@ppslk.com',
        'last_name': 'GtCRx',
        'password': '2ywHm',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='1hRNQ',
        slug='O9Nbf',
        abbreviation='n0bM5',
        plugged='UxFdG',
        background='RqUGW',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    journey_data = {
        'name': 'HHFyC',
        'abbreviation': 'DYbVc',
        'id_mention': mention.id,
    }

    resp_c = client.post('/api/v1/journeys/', json=journey_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/journeys/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'Journey deleted successfully'
    resp_chk = client.get(f'/api/v1/journeys/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

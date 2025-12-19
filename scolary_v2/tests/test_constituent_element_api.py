# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_constituent_element_api(client, db):
    """Create ConstituentElement via API."""
    # Auth setup
    user_data = {
        'email': 'nee49@lagwl.com',
        'last_name': 'HpDVI',
        'password': 'aPWiq',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='1YQKY',
        slug='p5IWv',
        abbreviation='5M5oI',
        plugged='zudqe',
        background='GQwt9',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='2mxOy',
        abbreviation='TDCJA',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    constituent_element_data = {
        'name': 'MvBnh',
        'semester': '5tZ9Q',
        'id_journey': journey.id,
        'color': 'hp0h3',
    }

    resp = client.post('/api/v1/constituent_elements/', json=constituent_element_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['name'] == constituent_element_data['name']
    assert created['semester'] == constituent_element_data['semester']
    assert created['id_journey'] == constituent_element_data['id_journey']
    assert created['color'] == constituent_element_data['color']


def test_update_constituent_element_api(client, db):
    """Update ConstituentElement via API."""
    # Auth setup
    user_data = {
        'email': '4keEs@0v9j4.com',
        'last_name': 'P9Z6Z',
        'password': 'W7zWP',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='zyGLE',
        slug='0k2VY',
        abbreviation='aI75x',
        plugged='qVom8',
        background='n5Drb',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='tYcIv',
        abbreviation='eIc8q',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    constituent_element_data = {
        'name': 'MiBuT',
        'semester': 'pFtjy',
        'id_journey': journey.id,
        'color': 'dhcVr',
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

    resp_c = client.post('/api/v1/constituent_elements/', json=constituent_element_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = ['id_journey']

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in constituent_element_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/constituent_elements/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['name'] == update_data['name']
    assert updated['semester'] == update_data['semester']
    assert updated['color'] == update_data['color']


def test_get_constituent_element_api(client, db):
    """Get ConstituentElement via API."""
    # Auth setup
    user_data = {
        'email': 'Bv55Y@gz7jl.com',
        'last_name': 'LjHcf',
        'password': 'MqGOY',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='4Gtq2',
        slug='gZc8U',
        abbreviation='71B1k',
        plugged='SXl5E',
        background='Uo20C',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='ALXwz',
        abbreviation='dp7uv',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    constituent_element_data = {
        'name': 'TM3lu',
        'semester': 'W8Jcd',
        'id_journey': journey.id,
        'color': 'FGQDW',
    }

    client.post('/api/v1/constituent_elements/', json=constituent_element_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/constituent_elements/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_constituent_element_api(client, db):
    """Get_by_id ConstituentElement via API."""
    # Auth setup
    user_data = {
        'email': 'bkEcr@h10jy.com',
        'last_name': '1sdTC',
        'password': 'urJBI',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='JeJXm',
        slug='OZbnU',
        abbreviation='jqLvj',
        plugged='mvy4w',
        background='fuYTe',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='K4cxX',
        abbreviation='8SBKl',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    constituent_element_data = {
        'name': 'S66ka',
        'semester': '2K6Nl',
        'id_journey': journey.id,
        'color': 'fV9DO',
    }

    resp_c = client.post('/api/v1/constituent_elements/', json=constituent_element_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/constituent_elements/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_constituent_element_api(client, db):
    """Delete ConstituentElement via API."""
    # Auth setup
    user_data = {
        'email': 'GzVne@67lld.com',
        'last_name': 'N1oHs',
        'password': 'B5uGo',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='XjkUO',
        slug='E6aq1',
        abbreviation='jBOVG',
        plugged='5owaQ',
        background='qD19z',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='IK4Df',
        abbreviation='AkjOj',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    constituent_element_data = {
        'name': 'XpDxo',
        'semester': 'dgzon',
        'id_journey': journey.id,
        'color': 'Hsdpf',
    }

    resp_c = client.post('/api/v1/constituent_elements/', json=constituent_element_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/constituent_elements/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'ConstituentElement deleted successfully'
    resp_chk = client.get(f'/api/v1/constituent_elements/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

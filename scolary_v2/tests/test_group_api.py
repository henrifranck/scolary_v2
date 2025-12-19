# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_group_api(client, db):
    """Create Group via API."""
    # Auth setup
    user_data = {
        'email': 'euDGF@tmy7v.com',
        'last_name': 'PHniY',
        'password': 'bhGSa',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='utBo4',
        slug='r4CQ4',
        abbreviation='BPc87',
        plugged='XgllZ',
        background='h2V1f',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='zIBzq',
        abbreviation='NkJIX',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    group_data = {
        'id_journey': journey.id,
        'semester': 'd7rio',
        'group_number': 6,
        'student_count': 6,
    }

    resp = client.post('/api/v1/groups/', json=group_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['id_journey'] == group_data['id_journey']
    assert created['semester'] == group_data['semester']
    assert created['group_number'] == group_data['group_number']
    assert created['student_count'] == group_data['student_count']


def test_update_group_api(client, db):
    """Update Group via API."""
    # Auth setup
    user_data = {
        'email': 'EwIhE@qesny.com',
        'last_name': 'Jv3hi',
        'password': 'nDYph',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='aTVHY',
        slug='ii0LX',
        abbreviation='6gIUL',
        plugged='EgypW',
        background='xacMr',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='ObaoQ',
        abbreviation='0BwbT',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    group_data = {
        'id_journey': journey.id,
        'semester': 'f7e4s',
        'group_number': 9,
        'student_count': 13,
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

    resp_c = client.post('/api/v1/groups/', json=group_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = ['id_journey']

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in group_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/groups/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['semester'] == update_data['semester']
    assert updated['group_number'] == update_data['group_number']
    assert updated['student_count'] == update_data['student_count']


def test_get_group_api(client, db):
    """Get Group via API."""
    # Auth setup
    user_data = {
        'email': 'zfgHQ@xtkhy.com',
        'last_name': 'LmuiE',
        'password': 'QiJsS',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='tl1Uv',
        slug='5ES2p',
        abbreviation='WekPb',
        plugged='OJejz',
        background='jEPvF',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='mViJi',
        abbreviation='wKBUR',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    group_data = {
        'id_journey': journey.id,
        'semester': 'C3E8I',
        'group_number': 1,
        'student_count': 2,
    }

    client.post('/api/v1/groups/', json=group_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/groups/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_group_api(client, db):
    """Get_by_id Group via API."""
    # Auth setup
    user_data = {
        'email': 'pggsd@pk0l5.com',
        'last_name': 'cFdqd',
        'password': 'FO6Ne',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='FCH6u',
        slug='Sj5zt',
        abbreviation='bCdjx',
        plugged='B1yd9',
        background='YT2ic',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='zOcoL',
        abbreviation='0huXU',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    group_data = {
        'id_journey': journey.id,
        'semester': 'Uvf7H',
        'group_number': 7,
        'student_count': 11,
    }

    resp_c = client.post('/api/v1/groups/', json=group_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/groups/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_group_api(client, db):
    """Delete Group via API."""
    # Auth setup
    user_data = {
        'email': 'pkXno@ijtve.com',
        'last_name': 'wmzQ9',
        'password': 'l8hQw',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='9KpND',
        slug='HF8JH',
        abbreviation='TetIz',
        plugged='eZsjf',
        background='7akad',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='2ShOe',
        abbreviation='iua0G',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    group_data = {
        'id_journey': journey.id,
        'semester': 'cjcgs',
        'group_number': 8,
        'student_count': 12,
    }

    resp_c = client.post('/api/v1/groups/', json=group_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/groups/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'Group deleted successfully'
    resp_chk = client.get(f'/api/v1/groups/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

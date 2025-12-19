# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_journey_semester_api(client, db):
    """Create JourneySemester via API."""
    # Auth setup
    user_data = {
        'email': '5XGYY@ci5ff.com',
        'last_name': 'IOzzj',
        'password': 'l6kY2',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='0nHxO',
        slug='Xuftm',
        abbreviation='iM7r4',
        plugged='dFzOa',
        background='Tmt9l',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='pbxou',
        abbreviation='lNNbk',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    journey_semester_data = {
        'id_journey': journey.id,
        'semester': '17TQn',
    }

    resp = client.post('/api/v1/journey_semesters/', json=journey_semester_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['id_journey'] == journey_semester_data['id_journey']
    assert created['semester'] == journey_semester_data['semester']


def test_update_journey_semester_api(client, db):
    """Update JourneySemester via API."""
    # Auth setup
    user_data = {
        'email': 'CkEPA@4gxez.com',
        'last_name': '6vUV0',
        'password': '8a1pC',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='anPKt',
        slug='6uYcU',
        abbreviation='nzdrd',
        plugged='uJCjk',
        background='ScQ0O',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='V4921',
        abbreviation='LYegp',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    journey_semester_data = {
        'id_journey': journey.id,
        'semester': 'vVfkA',
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

    resp_c = client.post('/api/v1/journey_semesters/', json=journey_semester_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = ['id_journey']

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in journey_semester_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/journey_semesters/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['semester'] == update_data['semester']


def test_get_journey_semester_api(client, db):
    """Get JourneySemester via API."""
    # Auth setup
    user_data = {
        'email': '4Jd9a@e4pjc.com',
        'last_name': 'VOZGH',
        'password': 'paeo4',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='w01Bc',
        slug='7xCB1',
        abbreviation='yreJZ',
        plugged='0in3Y',
        background='dPzp3',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='cpd4h',
        abbreviation='g5UsT',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    journey_semester_data = {
        'id_journey': journey.id,
        'semester': 'BFqNo',
    }

    client.post('/api/v1/journey_semesters/', json=journey_semester_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/journey_semesters/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_journey_semester_api(client, db):
    """Get_by_id JourneySemester via API."""
    # Auth setup
    user_data = {
        'email': 'RQDCC@tmr6f.com',
        'last_name': 'Nfvfd',
        'password': 'BlG5y',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='VRY0M',
        slug='bXJCk',
        abbreviation='DEjXv',
        plugged='5RQka',
        background='KyTTp',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='vwPxm',
        abbreviation='KyhOh',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    journey_semester_data = {
        'id_journey': journey.id,
        'semester': 'RmD05',
    }

    resp_c = client.post('/api/v1/journey_semesters/', json=journey_semester_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/journey_semesters/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_journey_semester_api(client, db):
    """Delete JourneySemester via API."""
    # Auth setup
    user_data = {
        'email': 'B1ccT@84lto.com',
        'last_name': 'pUHGR',
        'password': 'Sf4M9',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='mBTL1',
        slug='AehcE',
        abbreviation='MeXFK',
        plugged='TtJg7',
        background='c9zn5',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='GeNay',
        abbreviation='224XK',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    journey_semester_data = {
        'id_journey': journey.id,
        'semester': 'hajWI',
    }

    resp_c = client.post('/api/v1/journey_semesters/', json=journey_semester_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/journey_semesters/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'JourneySemester deleted successfully'
    resp_chk = client.get(f'/api/v1/journey_semesters/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

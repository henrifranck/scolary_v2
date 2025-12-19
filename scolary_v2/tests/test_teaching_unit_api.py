# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_teaching_unit_api(client, db):
    """Create TeachingUnit via API."""
    # Auth setup
    user_data = {
        'email': 'AMZmR@lxiu2.com',
        'last_name': 'BEeun',
        'password': 'uaJhO',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='CBH0l',
        slug='SJpya',
        abbreviation='mH2Rv',
        plugged='zd5rH',
        background='x8Nuh',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='HM0Ln',
        abbreviation='vu7GS',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    teaching_unit_data = {
        'name': 'SkDcQ',
        'semester': 'LOppS',
        'id_journey': journey.id,
    }

    resp = client.post('/api/v1/teaching_units/', json=teaching_unit_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['name'] == teaching_unit_data['name']
    assert created['semester'] == teaching_unit_data['semester']
    assert created['id_journey'] == teaching_unit_data['id_journey']


def test_update_teaching_unit_api(client, db):
    """Update TeachingUnit via API."""
    # Auth setup
    user_data = {
        'email': 'YzYLB@ervbi.com',
        'last_name': 'Awmgt',
        'password': 'QQ2jJ',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='Ie5yZ',
        slug='Ytaca',
        abbreviation='rTEt1',
        plugged='hK7xS',
        background='gDZe8',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='n7Lv1',
        abbreviation='c2wus',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    teaching_unit_data = {
        'name': 'ovtCm',
        'semester': '2WaKZ',
        'id_journey': journey.id,
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

    resp_c = client.post('/api/v1/teaching_units/', json=teaching_unit_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = ['id_journey']

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in teaching_unit_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/teaching_units/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['name'] == update_data['name']
    assert updated['semester'] == update_data['semester']


def test_get_teaching_unit_api(client, db):
    """Get TeachingUnit via API."""
    # Auth setup
    user_data = {
        'email': 'k5feY@ubybg.com',
        'last_name': 'Irwrv',
        'password': 'n63s9',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='QRd0Q',
        slug='uieZ8',
        abbreviation='KZNUe',
        plugged='p2eCZ',
        background='XbxCJ',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='gEyBa',
        abbreviation='A4UNW',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    teaching_unit_data = {
        'name': 'VaniP',
        'semester': 'F2tCx',
        'id_journey': journey.id,
    }

    client.post('/api/v1/teaching_units/', json=teaching_unit_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/teaching_units/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_teaching_unit_api(client, db):
    """Get_by_id TeachingUnit via API."""
    # Auth setup
    user_data = {
        'email': 'ExKiI@8ytoi.com',
        'last_name': 'oZkFe',
        'password': 'S7KWu',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='Y1Paa',
        slug='zLR0n',
        abbreviation='LBxF0',
        plugged='dcKwu',
        background='Zf87j',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='DC91x',
        abbreviation='bIRW4',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    teaching_unit_data = {
        'name': '0BvqR',
        'semester': 'tjNPn',
        'id_journey': journey.id,
    }

    resp_c = client.post('/api/v1/teaching_units/', json=teaching_unit_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/teaching_units/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_teaching_unit_api(client, db):
    """Delete TeachingUnit via API."""
    # Auth setup
    user_data = {
        'email': 'huilH@rsduc.com',
        'last_name': 'rBDEl',
        'password': '2Zp2i',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='nyoGE',
        slug='IGu5S',
        abbreviation='QbAuT',
        plugged='Ni8AD',
        background='cqom7',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='PyGcD',
        abbreviation='GVyrw',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    teaching_unit_data = {
        'name': 'CPUd0',
        'semester': 'ZEfjr',
        'id_journey': journey.id,
    }

    resp_c = client.post('/api/v1/teaching_units/', json=teaching_unit_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/teaching_units/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'TeachingUnit deleted successfully'
    resp_chk = client.get(f'/api/v1/teaching_units/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

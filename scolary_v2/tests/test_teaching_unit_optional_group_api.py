# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_teaching_unit_optional_group_api(client, db):
    """Create TeachingUnitOptionalGroup via API."""
    # Auth setup
    user_data = {
        'email': 'UKOeS@1nlof.com',
        'last_name': '95QTQ',
        'password': '3qsiV',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='Mw7bO',
        slug='KsYah',
        abbreviation='XXO7o',
        plugged='Ewtqg',
        background='XzaG4',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='erPWc',
        abbreviation='DzfMx',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    teaching_unit_optional_group_data = {
        'id_journey': journey.id,
        'semester': 'fEaXc',
        'selection_regle': 'e6R2kEPMO1odshFeZny8QC9XlcWnCTGLaoEldYE7BEXpq5SrpjLYN8iFVzG',
    }

    resp = client.post('/api/v1/teaching_unit_optional_groups/', json=teaching_unit_optional_group_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['id_journey'] == teaching_unit_optional_group_data['id_journey']
    assert created['semester'] == teaching_unit_optional_group_data['semester']
    assert created['selection_regle'] == teaching_unit_optional_group_data['selection_regle']


def test_update_teaching_unit_optional_group_api(client, db):
    """Update TeachingUnitOptionalGroup via API."""
    # Auth setup
    user_data = {
        'email': 'XoEdX@oxtq3.com',
        'last_name': '0kyrQ',
        'password': 'rCnmN',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='EL7GY',
        slug='qaCMw',
        abbreviation='Su6H4',
        plugged='ut93B',
        background='cuTgT',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='3j99T',
        abbreviation='q4zdG',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    teaching_unit_optional_group_data = {
        'id_journey': journey.id,
        'semester': 'd9ImJ',
        'selection_regle': 'YcCx0wH4Nb5PyuAiIAUkws8HE94SHO0',
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

    resp_c = client.post('/api/v1/teaching_unit_optional_groups/', json=teaching_unit_optional_group_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = ['id_journey']

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in teaching_unit_optional_group_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/teaching_unit_optional_groups/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['semester'] == update_data['semester']
    assert updated['selection_regle'] == update_data['selection_regle']


def test_get_teaching_unit_optional_group_api(client, db):
    """Get TeachingUnitOptionalGroup via API."""
    # Auth setup
    user_data = {
        'email': 'bsB3V@h06au.com',
        'last_name': 'XDMf4',
        'password': '96a06',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='jlDKN',
        slug='AA2KM',
        abbreviation='S80A2',
        plugged='m4I2y',
        background='eVkyt',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='EplXz',
        abbreviation='nYKcW',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    teaching_unit_optional_group_data = {
        'id_journey': journey.id,
        'semester': 'Tl7lK',
        'selection_regle': '',
    }

    client.post('/api/v1/teaching_unit_optional_groups/', json=teaching_unit_optional_group_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/teaching_unit_optional_groups/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_teaching_unit_optional_group_api(client, db):
    """Get_by_id TeachingUnitOptionalGroup via API."""
    # Auth setup
    user_data = {
        'email': 'RujtU@70ujn.com',
        'last_name': 'lbVT2',
        'password': 'pxw7N',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='PJbB0',
        slug='Vfc83',
        abbreviation='s58DH',
        plugged='1NRXr',
        background='Pfz52',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='MCQty',
        abbreviation='IOb0E',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    teaching_unit_optional_group_data = {
        'id_journey': journey.id,
        'semester': 'Hhnxu',
        'selection_regle': 'lBrAYASeiMyKxfohTpz6GTA0l3dh7EEcS',
    }

    resp_c = client.post('/api/v1/teaching_unit_optional_groups/', json=teaching_unit_optional_group_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/teaching_unit_optional_groups/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_teaching_unit_optional_group_api(client, db):
    """Delete TeachingUnitOptionalGroup via API."""
    # Auth setup
    user_data = {
        'email': 'j1SjR@1xf3l.com',
        'last_name': 'EhQa2',
        'password': 'zC2la',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='iHYNF',
        slug='v8mBb',
        abbreviation='cv78f',
        plugged='EHSZ9',
        background='cwfBP',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='lFrgn',
        abbreviation='bqaQj',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    teaching_unit_optional_group_data = {
        'id_journey': journey.id,
        'semester': '2rKuq',
        'selection_regle': 'usf2urLW3h6pTi2rzNJct5i7zQzzVce1EZbOtVgxY1A51wMzkK3MFKR3KhHvSvQrWKusTuFvxYrHYXN3xA70UpdNR',
    }

    resp_c = client.post('/api/v1/teaching_unit_optional_groups/', json=teaching_unit_optional_group_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/teaching_unit_optional_groups/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'TeachingUnitOptionalGroup deleted successfully'
    resp_chk = client.get(f'/api/v1/teaching_unit_optional_groups/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

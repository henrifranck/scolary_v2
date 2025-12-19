# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_teaching_unit_offering_api(client, db):
    """Create TeachingUnitOffering via API."""
    # Auth setup
    user_data = {
        'email': 'ozULC@ua9ui.com',
        'last_name': 'KYcJn',
        'password': '7NhY1',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='Uit1G',
        slug='7mUGm',
        abbreviation='qIRsM',
        plugged='nTxXt',
        background='DyadJ',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='1vRsz',
        abbreviation='L4QkD',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='wHh0o',
        semester='fUjzO',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='NaytZ',
        code='nMwzQ',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='t6TGV',
        selection_regle='pNQn4V4y9UAILOEYGR9DBHxSTfJ7qglusjLnYAMZeYCt7WVB5pNdsrF1fQWenllUZouV4s8OsDvXNPUNg8q5I',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    teaching_unit_offering_data = {
        'id_teaching_unit': teaching_unit.id,
        'credit': 18,
        'id_academic_year': academic_year.id,
        'id_teaching_unit_goup': teaching_unit_optional_group.id,
    }

    resp = client.post('/api/v1/teaching_unit_offerings/', json=teaching_unit_offering_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['id_teaching_unit'] == teaching_unit_offering_data['id_teaching_unit']
    assert created['credit'] == teaching_unit_offering_data['credit']
    assert created['id_academic_year'] == teaching_unit_offering_data['id_academic_year']
    assert created['id_teaching_unit_goup'] == teaching_unit_offering_data['id_teaching_unit_goup']


def test_update_teaching_unit_offering_api(client, db):
    """Update TeachingUnitOffering via API."""
    # Auth setup
    user_data = {
        'email': 'JaONH@pugdl.com',
        'last_name': 'p65RB',
        'password': 'VEkAa',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='nkmum',
        slug='9vUzu',
        abbreviation='xZfEu',
        plugged='pmhYn',
        background='QMa6A',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='LZ2fu',
        abbreviation='7fdAt',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='ZxzQa',
        semester='15XGt',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='8aPii',
        code='JZxK1',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='wTLl7',
        selection_regle='v60YxtjScz8I7Bh6G4hcED6uOiSKbzWbysvXZPczciXYi',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    teaching_unit_offering_data = {
        'id_teaching_unit': teaching_unit.id,
        'credit': 17,
        'id_academic_year': academic_year.id,
        'id_teaching_unit_goup': teaching_unit_optional_group.id,
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

    resp_c = client.post('/api/v1/teaching_unit_offerings/', json=teaching_unit_offering_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = ['id_teaching_unit', 'id_academic_year', 'id_teaching_unit_goup']

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in teaching_unit_offering_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/teaching_unit_offerings/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['credit'] == update_data['credit']


def test_get_teaching_unit_offering_api(client, db):
    """Get TeachingUnitOffering via API."""
    # Auth setup
    user_data = {
        'email': 'Hcxzo@crvro.com',
        'last_name': 'pTKmb',
        'password': 'vyT8Z',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='ZHcxk',
        slug='mumVJ',
        abbreviation='dXIkO',
        plugged='44Dcc',
        background='ImJSG',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='2QUEE',
        abbreviation='Niaao',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='NWYBU',
        semester='p9cix',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='FNUzN',
        code='p7itG',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='1yp78',
        selection_regle='diwxuFgwZrX5blxBODTSrRYtqY7vhXAZSUC6tBruNroq7BHKGEGKWfOdiEUDOTsYZcJC5N1V0',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    teaching_unit_offering_data = {
        'id_teaching_unit': teaching_unit.id,
        'credit': 16,
        'id_academic_year': academic_year.id,
        'id_teaching_unit_goup': teaching_unit_optional_group.id,
    }

    client.post('/api/v1/teaching_unit_offerings/', json=teaching_unit_offering_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/teaching_unit_offerings/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_teaching_unit_offering_api(client, db):
    """Get_by_id TeachingUnitOffering via API."""
    # Auth setup
    user_data = {
        'email': 'YZgNd@ptw3b.com',
        'last_name': '4Hbvr',
        'password': '48BNF',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='HUbie',
        slug='W8OUU',
        abbreviation='5HDiy',
        plugged='DplYv',
        background='7mDNu',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='4eHKB',
        abbreviation='I6VS1',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='ghPh0',
        semester='T8yE3',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='vtBUJ',
        code='sRXWG',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='kMD2l',
        selection_regle='05H1ppFBGoCYKxPioOzX7etSb',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    teaching_unit_offering_data = {
        'id_teaching_unit': teaching_unit.id,
        'credit': 18,
        'id_academic_year': academic_year.id,
        'id_teaching_unit_goup': teaching_unit_optional_group.id,
    }

    resp_c = client.post('/api/v1/teaching_unit_offerings/', json=teaching_unit_offering_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/teaching_unit_offerings/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_teaching_unit_offering_api(client, db):
    """Delete TeachingUnitOffering via API."""
    # Auth setup
    user_data = {
        'email': 'JIc76@mjchk.com',
        'last_name': 'vtIW0',
        'password': 'cKt04',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='ESotK',
        slug='14DMO',
        abbreviation='0AS4o',
        plugged='KBApw',
        background='CQDK3',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='gU9xV',
        abbreviation='ORRxN',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='Ondws',
        semester='TM3x6',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='sJbdS',
        code='ZBPF1',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='XOoB3',
        selection_regle='Jqgbss0J29lW9Q4FsueVJTVdp',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    teaching_unit_offering_data = {
        'id_teaching_unit': teaching_unit.id,
        'credit': 2,
        'id_academic_year': academic_year.id,
        'id_teaching_unit_goup': teaching_unit_optional_group.id,
    }

    resp_c = client.post('/api/v1/teaching_unit_offerings/', json=teaching_unit_offering_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/teaching_unit_offerings/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'TeachingUnitOffering deleted successfully'
    resp_chk = client.get(f'/api/v1/teaching_unit_offerings/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

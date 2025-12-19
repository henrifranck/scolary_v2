# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_constituent_element_optional_group_api(client, db):
    """Create ConstituentElementOptionalGroup via API."""
    # Auth setup
    user_data = {
        'email': 'k4zyd@63xy3.com',
        'last_name': 'hFGNH',
        'password': 'LU0Vn',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='jij3t',
        slug='KO32n',
        abbreviation='b2TkR',
        plugged='MrgZN',
        background='wATE5',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='BUdC0',
        abbreviation='toXGf',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='hEXYs',
        semester='U5RmC',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='VDxC5',
        code='0SEJH',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='ldhQh',
        selection_regle='iIZ5YgEsatLlHuO8Y4aJ0rp6gGNaBUU6ti3BaQTp3ZqCZv6uun6EqMPCxEt',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=4,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    constituent_element_optional_group_data = {
        'id_teaching_unit_offering': teaching_unit_offering.id,
        'selection_regle': 'YpGXWXfxAwrDGpTV8mMZUfyBsPVrC8qqwq2o5709kP0pIgtsbv3Wm6fazWUyx7nlZT4vWG2LgVnVhKL',
    }

    resp = client.post('/api/v1/constituent_element_optional_groups/', json=constituent_element_optional_group_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['id_teaching_unit_offering'] == constituent_element_optional_group_data['id_teaching_unit_offering']
    assert created['selection_regle'] == constituent_element_optional_group_data['selection_regle']


def test_update_constituent_element_optional_group_api(client, db):
    """Update ConstituentElementOptionalGroup via API."""
    # Auth setup
    user_data = {
        'email': 'rol9P@eruen.com',
        'last_name': 'qoKWL',
        'password': '5fmH6',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='tCwRb',
        slug='MxAYt',
        abbreviation='GxxYs',
        plugged='Zitk8',
        background='5FTw9',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='nLpjS',
        abbreviation='kkRAr',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='5CIX4',
        semester='N4Z4D',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='Bp8L2',
        code='OPc7v',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='yCdca',
        selection_regle='sw3RdYlpaCaU3QmjBl',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=10,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    constituent_element_optional_group_data = {
        'id_teaching_unit_offering': teaching_unit_offering.id,
        'selection_regle': 'KkHPrrA3YmZQDJDnm5YRLgCet',
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

    resp_c = client.post('/api/v1/constituent_element_optional_groups/', json=constituent_element_optional_group_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = ['id_teaching_unit_offering']

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in constituent_element_optional_group_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/constituent_element_optional_groups/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['selection_regle'] == update_data['selection_regle']


def test_get_constituent_element_optional_group_api(client, db):
    """Get ConstituentElementOptionalGroup via API."""
    # Auth setup
    user_data = {
        'email': 'Xruce@uuvby.com',
        'last_name': 'PwsYm',
        'password': 'pE9ry',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='tGAQL',
        slug='aLzWq',
        abbreviation='DAUQE',
        plugged='Lg1I4',
        background='aSnsn',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='E0U9l',
        abbreviation='UFU5q',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='WB1HI',
        semester='TILaJ',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='1V9Rn',
        code='MgYkO',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='0K7bx',
        selection_regle='9AYL1afkEhXHBQoqmfb1rJQ4NJe',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=6,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    constituent_element_optional_group_data = {
        'id_teaching_unit_offering': teaching_unit_offering.id,
        'selection_regle': 'nRDbceWfbQBtTEuKSjGyCw4W8ROVrQHCokRlFXGXhrf9',
    }

    client.post('/api/v1/constituent_element_optional_groups/', json=constituent_element_optional_group_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/constituent_element_optional_groups/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_constituent_element_optional_group_api(client, db):
    """Get_by_id ConstituentElementOptionalGroup via API."""
    # Auth setup
    user_data = {
        'email': 'VdYeU@mkgtd.com',
        'last_name': 'VFkOT',
        'password': 'LPhxr',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='owCvl',
        slug='h9my9',
        abbreviation='eObud',
        plugged='JAAk8',
        background='RGGJl',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='i4Fx6',
        abbreviation='UeX8V',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='1MMeM',
        semester='KYl5Z',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='U70nn',
        code='jXoUI',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='dkGlD',
        selection_regle='i2KTE4DELMvJzIS1GhLKHBngEvSuc30SgRR2e6xCiOeOUkQFM8CmtAX3Q81vugcuknkNA',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=7,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    constituent_element_optional_group_data = {
        'id_teaching_unit_offering': teaching_unit_offering.id,
        'selection_regle': 'ch8WqwPAP2nhQKJx5CwGpGGsm99IY6opo60knK5cMXsi2YvyboqWxdiWGkLs4LX0vfX8XJrnC1',
    }

    resp_c = client.post('/api/v1/constituent_element_optional_groups/', json=constituent_element_optional_group_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/constituent_element_optional_groups/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_constituent_element_optional_group_api(client, db):
    """Delete ConstituentElementOptionalGroup via API."""
    # Auth setup
    user_data = {
        'email': 'kESkP@oggwd.com',
        'last_name': 'ykyBE',
        'password': '7RJMQ',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='EC9A6',
        slug='6bYTp',
        abbreviation='Jg0bQ',
        plugged='YwqvJ',
        background='VDzSL',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='PYtmz',
        abbreviation='qebTy',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='iVQ3Z',
        semester='BYhGC',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='tH7zZ',
        code='Rm0FQ',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='hAuYl',
        selection_regle='y42t57ZYwiOb1orSS4C2UWn6mjDjqDEuZVG6QHb1a',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=0,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    constituent_element_optional_group_data = {
        'id_teaching_unit_offering': teaching_unit_offering.id,
        'selection_regle': 'OLkSZ3OrpOpVjkigO3J',
    }

    resp_c = client.post('/api/v1/constituent_element_optional_groups/', json=constituent_element_optional_group_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/constituent_element_optional_groups/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'ConstituentElementOptionalGroup deleted successfully'
    resp_chk = client.get(f'/api/v1/constituent_element_optional_groups/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

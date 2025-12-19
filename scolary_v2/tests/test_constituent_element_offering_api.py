# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_constituent_element_offering_api(client, db):
    """Create ConstituentElementOffering via API."""
    # Auth setup
    user_data = {
        'email': 'jugVn@ztx98.com',
        'last_name': '7ia3y',
        'password': 'njMlT',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='UOAVB',
        slug='UHri8',
        abbreviation='jWCLS',
        plugged='Cvi0C',
        background='Um6Se',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='CbqHT',
        abbreviation='1ldwB',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='N2D3G',
        semester='nyCsV',
        id_journey=journey.id,
        color='Kyd61',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='Ux2Hm',
        code='GPMVA',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='aGQGe',
        semester='dNF3S',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='kttAY',
        selection_regle='ljZP4Tb2M2UU6XuPVruZ1Lm3mm0DCYGwRTCC5Mrb',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=11,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='18BJkJa3J2Kmqf7TVUkr6fKkRJdVJVOFbc8fHQ4hFXQ5dCe9lXQCAfOd',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=20,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    constituent_element_offering_data = {
        'id_constituent_element': constituent_element.id,
        'weight': 4.52734713184398,
        'id_academic_year': academic_year.id,
        'id_constituent_element_optional_group': constituent_element_optional_group.id,
        'id_teching_unit_offering': teaching_unit_offering.id,
    }

    resp = client.post('/api/v1/constituent_element_offerings/', json=constituent_element_offering_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['id_constituent_element'] == constituent_element_offering_data['id_constituent_element']
    assert created['weight'] == constituent_element_offering_data['weight']
    assert created['id_academic_year'] == constituent_element_offering_data['id_academic_year']
    assert created['id_constituent_element_optional_group'] == constituent_element_offering_data['id_constituent_element_optional_group']
    assert created['id_teching_unit_offering'] == constituent_element_offering_data['id_teching_unit_offering']


def test_update_constituent_element_offering_api(client, db):
    """Update ConstituentElementOffering via API."""
    # Auth setup
    user_data = {
        'email': '9xeIy@x35qs.com',
        'last_name': '15g0c',
        'password': 'WjyCw',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='z9Utc',
        slug='7rKNG',
        abbreviation='4vmci',
        plugged='uPbqn',
        background='9Gytl',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='lxf2t',
        abbreviation='NYg1X',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='OrzZx',
        semester='WQ0Wa',
        id_journey=journey.id,
        color='C8JQt',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='kWXPY',
        code='tlUzh',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='9vBpd',
        semester='OYRKw',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='5Eys8',
        selection_regle='DGjTcbhtH935aqNSENkIdoyB9NIzJ6858qr8Xa1P77DjILHMQgB0HAeaOJkjXA',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=16,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='c6vUlofY0bkyBReDkwEKBa5MWrLwbK8Yw16vKXu3CyakUSbdYTdOB0skg',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=20,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    constituent_element_offering_data = {
        'id_constituent_element': constituent_element.id,
        'weight': 2.6362484897808205,
        'id_academic_year': academic_year.id,
        'id_constituent_element_optional_group': constituent_element_optional_group.id,
        'id_teching_unit_offering': teaching_unit_offering.id,
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

    resp_c = client.post('/api/v1/constituent_element_offerings/', json=constituent_element_offering_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = ['id_constituent_element', 'id_academic_year', 'id_constituent_element_optional_group', 'id_teching_unit_offering']

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in constituent_element_offering_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/constituent_element_offerings/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['weight'] == update_data['weight']


def test_get_constituent_element_offering_api(client, db):
    """Get ConstituentElementOffering via API."""
    # Auth setup
    user_data = {
        'email': 'uKIeR@s6rro.com',
        'last_name': 'sNHKE',
        'password': 'dm1QL',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='sxGaM',
        slug='XcsJz',
        abbreviation='kboz8',
        plugged='8adPJ',
        background='h4r2y',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='VM1yt',
        abbreviation='6N06m',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='yprqr',
        semester='25Yg8',
        id_journey=journey.id,
        color='T1KFS',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='ILbjW',
        code='Et5h0',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='b4TWu',
        semester='HpBEa',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='uMRc1',
        selection_regle='lag',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=16,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='7TJy0x6DsOIrIfm4zkxGuCRRfaLgLTCcSLnSIfgXU52Y7uTBWcQb3b28k',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=15,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    constituent_element_offering_data = {
        'id_constituent_element': constituent_element.id,
        'weight': 3.9514418412032914,
        'id_academic_year': academic_year.id,
        'id_constituent_element_optional_group': constituent_element_optional_group.id,
        'id_teching_unit_offering': teaching_unit_offering.id,
    }

    client.post('/api/v1/constituent_element_offerings/', json=constituent_element_offering_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/constituent_element_offerings/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_constituent_element_offering_api(client, db):
    """Get_by_id ConstituentElementOffering via API."""
    # Auth setup
    user_data = {
        'email': 'A0kkG@oynbc.com',
        'last_name': 'gxXKc',
        'password': 'WCPJC',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='aOzYs',
        slug='iVxeX',
        abbreviation='BEsW3',
        plugged='cxTy0',
        background='wCRYY',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='4R2VE',
        abbreviation='ll7sV',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='ksHaX',
        semester='LxgOh',
        id_journey=journey.id,
        color='PLMRf',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='w26lj',
        code='MbDv1',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='xPZmP',
        semester='qmbym',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='PJOzH',
        selection_regle='jTHYmTYN5puUzmjY4r2f55Y4MYSjjGmNxKhAz5L5v',
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

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='zBXtneqmHjZtURFy8J0vtFS8sYsNHHj6EFkWsW8tH4l54opGchgcYA2FLRlDx5wMyRfW3SXz27Uc6Hx17SMRXAI5GjlcnBqTl',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=19,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    constituent_element_offering_data = {
        'id_constituent_element': constituent_element.id,
        'weight': 1.88233166255963,
        'id_academic_year': academic_year.id,
        'id_constituent_element_optional_group': constituent_element_optional_group.id,
        'id_teching_unit_offering': teaching_unit_offering.id,
    }

    resp_c = client.post('/api/v1/constituent_element_offerings/', json=constituent_element_offering_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/constituent_element_offerings/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_constituent_element_offering_api(client, db):
    """Delete ConstituentElementOffering via API."""
    # Auth setup
    user_data = {
        'email': '4Ojnd@y3zpy.com',
        'last_name': 's4zfM',
        'password': 'DddAK',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='U0N5G',
        slug='DqWr2',
        abbreviation='HUniI',
        plugged='vmImL',
        background='UGSQr',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='OXGmA',
        abbreviation='1ikoW',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='PeJMq',
        semester='GAKlq',
        id_journey=journey.id,
        color='7x3d1',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='bBASV',
        code='2lE6m',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='FObfz',
        semester='HBykx',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='iVjj6',
        selection_regle='NnYP72pqYLnqvd6XenEVQiX51VKdHOmTGVLkQhzvAClJvOuwBcfnkRAUZI3heMrOz84cSwGhw0HFtxbgfI1AaHH2EbRW',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=1,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='k0dNaOC4E8ibyXUOFQC1Jl8HxmHYuybxGdvyEWEDxODghopGgvzTosTeoeyip8qVYJ7TYAmNgsjwzq5NdAiIov3goLBBJ5VHS7',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=0,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    constituent_element_offering_data = {
        'id_constituent_element': constituent_element.id,
        'weight': 2.8312016624519645,
        'id_academic_year': academic_year.id,
        'id_constituent_element_optional_group': constituent_element_optional_group.id,
        'id_teching_unit_offering': teaching_unit_offering.id,
    }

    resp_c = client.post('/api/v1/constituent_element_offerings/', json=constituent_element_offering_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/constituent_element_offerings/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'ConstituentElementOffering deleted successfully'
    resp_chk = client.get(f'/api/v1/constituent_element_offerings/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

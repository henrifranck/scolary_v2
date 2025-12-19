# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_working_time_api(client, db):
    """Create WorkingTime via API."""
    # Auth setup
    user_data = {
        'email': 'f2QqI@v5odb.com',
        'last_name': 'lAUbv',
        'password': 'n21oY',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='ebVgc',
        slug='u1ptu',
        abbreviation='yEvyX',
        plugged='uc84k',
        background='Lio55',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='SJKus',
        abbreviation='VCGHS',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='CKE1g',
        semester='gTUTX',
        id_journey=journey.id,
        color='GFgYV',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='99d4o',
        code='QihxB',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='2RDMI',
        semester='cKCXA',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='ohjib',
        selection_regle='E51SvtkqkkwXOffjEZHffrDFZ',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=15,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='xU3',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=3.250936124378666,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

    # Test data for Group
    group_data = schemas.GroupCreate(
        id_journey=journey.id,
        semester='srH9f',
        group_number=9,
        student_count=8,
    )

    group = crud.group.create(db=db, obj_in=group_data)

    working_time_data = {
        'id_constituent_element': constituent_element_offering.id,
        'working_time_type': 'cours',
        'day': 'vPN4f',
        'start': '20:15:25',
        'end': '15:35:33',
        'id_group': group.id,
        'date': '2025-11-15T18:57:08.740430',
        'session': 'Normal',
    }

    resp = client.post('/api/v1/working_times/', json=working_time_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['id_constituent_element'] == working_time_data['id_constituent_element']
    assert created['working_time_type'] == working_time_data['working_time_type']
    assert created['day'] == working_time_data['day']
    assert created['start'] == working_time_data['start']
    assert created['end'] == working_time_data['end']
    assert created['id_group'] == working_time_data['id_group']
    assert created['session'] == working_time_data['session']


def test_update_working_time_api(client, db):
    """Update WorkingTime via API."""
    # Auth setup
    user_data = {
        'email': 'JTd0V@f0l6r.com',
        'last_name': 'SV8Ux',
        'password': 'p9yx9',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='dQw0o',
        slug='xcbPs',
        abbreviation='N2Ei5',
        plugged='OpsA8',
        background='Bizlj',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='qnDhU',
        abbreviation='oJ3Tw',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='Xic1F',
        semester='loYK2',
        id_journey=journey.id,
        color='E3VhM',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='9uzN0',
        code='OYgX3',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='z0ZNL',
        semester='VuVlv',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='F8GoC',
        selection_regle='BE38KtbfbDu7825uPshNlec89an4',
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

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='FsH5KTPsZv07NY9mt1hvGT',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=3.226200832487172,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

    # Test data for Group
    group_data = schemas.GroupCreate(
        id_journey=journey.id,
        semester='StmI5',
        group_number=18,
        student_count=8,
    )

    group = crud.group.create(db=db, obj_in=group_data)

    working_time_data = {
        'id_constituent_element': constituent_element_offering.id,
        'working_time_type': 'td',
        'day': 'XMMq3',
        'start': '05:10:48',
        'end': '20:34:22',
        'id_group': group.id,
        'date': '2025-11-15T18:57:08.741522',
        'session': 'Rattrapage',
    }

    # Precompute enum values for update
    enum_values_map = {}
    enum_values_map['working_time_type'] = ['cours', 'tp', 'td', 'Exam']
    enum_values_map['session'] = ['Normal', 'Rattrapage']

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
        if k in ['date']:
            if isinstance(v, str):
                return (datetime.fromisoformat(v) + timedelta(days=1)).isoformat()
            return v

        # date +1 jour
        if k in []:
            if isinstance(v, str):
                return (date.fromisoformat(v) + timedelta(days=1)).isoformat()
            return v

        # time +1 heure
        if k in ['start', 'end']:
            if isinstance(v, str):
                return (datetime.strptime(v, '%H:%M:%S') + timedelta(hours=1)).time().strftime('%H:%M:%S')
            return v

        # fallback -> prefix 'updated_'
        return f'updated_{v}'

    resp_c = client.post('/api/v1/working_times/', json=working_time_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = ['id_constituent_element', 'id_group']

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in working_time_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/working_times/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['working_time_type'] == update_data['working_time_type']
    assert updated['day'] == update_data['day']
    assert updated['start'] == update_data['start']
    assert updated['end'] == update_data['end']
    assert updated['date'] == update_data['date']
    assert updated['session'] == update_data['session']


def test_get_working_time_api(client, db):
    """Get WorkingTime via API."""
    # Auth setup
    user_data = {
        'email': 'zT7Dl@pfmf5.com',
        'last_name': 'EWKtN',
        'password': 'e2WGF',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='9AzY7',
        slug='nAiTG',
        abbreviation='thT18',
        plugged='7IDFV',
        background='Bp8Nw',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='fM1oI',
        abbreviation='vB09u',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='MR88u',
        semester='eDPf7',
        id_journey=journey.id,
        color='K9ayY',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='xJhZs',
        code='Gd8XU',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='qJ5ks',
        semester='lECzt',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='sSU3s',
        selection_regle='6aDlei4Lo1e80XI9Ys0TuFRpzn5IZ1pNFt4KFA9jYMpun6oigWs9tszbkaWLenVJ4nuuiXy0yvxCTk5TMSpsavSOjHxKopAu',
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
        selection_regle='lhTiIyM0EL2HuxBMCbLtRk4nYoMkajCl6osyxCKOXKHnbonrj1RrwlHinyCpTA5eTDpPAiHi7DYVu5UwcpDEpdsgk0vv9DS',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=3.9985707396182315,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

    # Test data for Group
    group_data = schemas.GroupCreate(
        id_journey=journey.id,
        semester='cY3pP',
        group_number=3,
        student_count=2,
    )

    group = crud.group.create(db=db, obj_in=group_data)

    working_time_data = {
        'id_constituent_element': constituent_element_offering.id,
        'working_time_type': 'Exam',
        'day': 'Ptw4n',
        'start': '05:03:18',
        'end': '09:47:26',
        'id_group': group.id,
        'date': '2025-11-15T18:57:08.776707',
        'session': 'Normal',
    }

    client.post('/api/v1/working_times/', json=working_time_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/working_times/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_working_time_api(client, db):
    """Get_by_id WorkingTime via API."""
    # Auth setup
    user_data = {
        'email': 'gKpv3@b09me.com',
        'last_name': '1kTe7',
        'password': 'UxFUz',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='cjqVN',
        slug='QW0mU',
        abbreviation='StnCa',
        plugged='1TTDo',
        background='W5Z3z',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='YCkAt',
        abbreviation='bD2bN',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='rlKBD',
        semester='65uFm',
        id_journey=journey.id,
        color='woXOp',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='8cOj8',
        code='1peVI',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='m5i3I',
        semester='CS8Ee',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='gJuPh',
        selection_regle='uaneXyxhE9ss3ECB2pvEIP2IDP',
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
        selection_regle='kfxPLcC3QsL6Z1er61YnJVczYv6HALG7',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=4.301781239370778,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

    # Test data for Group
    group_data = schemas.GroupCreate(
        id_journey=journey.id,
        semester='WacoC',
        group_number=20,
        student_count=14,
    )

    group = crud.group.create(db=db, obj_in=group_data)

    working_time_data = {
        'id_constituent_element': constituent_element_offering.id,
        'working_time_type': 'td',
        'day': 'wUOCV',
        'start': '23:42:37',
        'end': '08:19:36',
        'id_group': group.id,
        'date': '2025-11-15T18:57:08.777812',
        'session': 'Normal',
    }

    resp_c = client.post('/api/v1/working_times/', json=working_time_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/working_times/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_working_time_api(client, db):
    """Delete WorkingTime via API."""
    # Auth setup
    user_data = {
        'email': 'Rya9k@smaaf.com',
        'last_name': 'PV8Ky',
        'password': '9jybF',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='pXOWy',
        slug='4fdMv',
        abbreviation='xX2Sl',
        plugged='kWAR1',
        background='uxuOt',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='EK86Y',
        abbreviation='kDMgg',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='XXSFp',
        semester='8ADS5',
        id_journey=journey.id,
        color='KBod6',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='irj6g',
        code='mVSvD',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='7sWNV',
        semester='dcynR',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='Xuh7m',
        selection_regle='JpzSODmbCfA7Ese3QAUbPICpJNAy5fIMAHLB3C2j13y44HBoOTzZ',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=19,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='xAabvhe3Io4r8Fq0Pm4Rv',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=4.608829881952165,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

    # Test data for Group
    group_data = schemas.GroupCreate(
        id_journey=journey.id,
        semester='qZ3Gw',
        group_number=1,
        student_count=11,
    )

    group = crud.group.create(db=db, obj_in=group_data)

    working_time_data = {
        'id_constituent_element': constituent_element_offering.id,
        'working_time_type': 'tp',
        'day': 'Tn4wX',
        'start': '23:03:19',
        'end': '08:09:29',
        'id_group': group.id,
        'date': '2025-11-15T18:57:08.778549',
        'session': 'Normal',
    }

    resp_c = client.post('/api/v1/working_times/', json=working_time_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/working_times/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'WorkingTime deleted successfully'
    resp_chk = client.get(f'/api/v1/working_times/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

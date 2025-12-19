# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_exam_group_api(client, db):
    """Create ExamGroup via API."""
    # Auth setup
    user_data = {
        'email': '5Ns7c@ykkcu.com',
        'last_name': '3qENf',
        'password': 'rPn2m',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Classroom
    classroom_data = schemas.ClassroomCreate(
        name='InUyR',
        capacity=2,
    )

    classroom = crud.classroom.create(db=db, obj_in=classroom_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='tdGFK',
        slug='W42Hw',
        abbreviation='KtsEV',
        plugged='wNcDX',
        background='Iz95y',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='NKueR',
        abbreviation='YmtqN',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='7B0Rq',
        code='0HTLd',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    exam_group_data = {
        'id_classroom': classroom.id,
        'id_journey': journey.id,
        'semester': 'IniAk',
        'num_from': 14,
        'num_to': 20,
        'session': 'Normal',
        'id_accademic_year': academic_year.id,
    }

    resp = client.post('/api/v1/exam_groups/', json=exam_group_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['id_classroom'] == exam_group_data['id_classroom']
    assert created['id_journey'] == exam_group_data['id_journey']
    assert created['semester'] == exam_group_data['semester']
    assert created['num_from'] == exam_group_data['num_from']
    assert created['num_to'] == exam_group_data['num_to']
    assert created['session'] == exam_group_data['session']
    assert created['id_accademic_year'] == exam_group_data['id_accademic_year']


def test_update_exam_group_api(client, db):
    """Update ExamGroup via API."""
    # Auth setup
    user_data = {
        'email': 'AQfFN@fdrp6.com',
        'last_name': '7Jy9G',
        'password': 'EYVsy',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Classroom
    classroom_data = schemas.ClassroomCreate(
        name='3Gpb7',
        capacity=6,
    )

    classroom = crud.classroom.create(db=db, obj_in=classroom_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='2AdRs',
        slug='7FRWn',
        abbreviation='OStSQ',
        plugged='8t1AR',
        background='M14Ej',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='SkL5u',
        abbreviation='uZJj4',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='FuZLf',
        code='ozMjM',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    exam_group_data = {
        'id_classroom': classroom.id,
        'id_journey': journey.id,
        'semester': '7Z3Xl',
        'num_from': 12,
        'num_to': 17,
        'session': 'Normal',
        'id_accademic_year': academic_year.id,
    }

    # Precompute enum values for update
    enum_values_map = {}
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

    resp_c = client.post('/api/v1/exam_groups/', json=exam_group_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = ['id_classroom', 'id_journey', 'id_accademic_year']

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in exam_group_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/exam_groups/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['semester'] == update_data['semester']
    assert updated['num_from'] == update_data['num_from']
    assert updated['num_to'] == update_data['num_to']
    assert updated['session'] == update_data['session']


def test_get_exam_group_api(client, db):
    """Get ExamGroup via API."""
    # Auth setup
    user_data = {
        'email': 'KPs42@arzcf.com',
        'last_name': 'GU6pU',
        'password': 'yLE5K',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Classroom
    classroom_data = schemas.ClassroomCreate(
        name='2Sh3n',
        capacity=20,
    )

    classroom = crud.classroom.create(db=db, obj_in=classroom_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='Tb5du',
        slug='derNn',
        abbreviation='rHrXB',
        plugged='LVOe3',
        background='j59TC',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='L6S7c',
        abbreviation='pq00H',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='Zh7aR',
        code='CDfAw',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    exam_group_data = {
        'id_classroom': classroom.id,
        'id_journey': journey.id,
        'semester': 'UaJM4',
        'num_from': 15,
        'num_to': 6,
        'session': 'Rattrapage',
        'id_accademic_year': academic_year.id,
    }

    client.post('/api/v1/exam_groups/', json=exam_group_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/exam_groups/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_exam_group_api(client, db):
    """Get_by_id ExamGroup via API."""
    # Auth setup
    user_data = {
        'email': 'VoJ8r@ebfax.com',
        'last_name': 'mtF9e',
        'password': 'E2Rrm',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Classroom
    classroom_data = schemas.ClassroomCreate(
        name='93t5o',
        capacity=20,
    )

    classroom = crud.classroom.create(db=db, obj_in=classroom_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='QUTIr',
        slug='3ux6n',
        abbreviation='DSSNc',
        plugged='pm6YA',
        background='TQwxp',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='wrmab',
        abbreviation='XHRLM',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='t68Y6',
        code='kTMKZ',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    exam_group_data = {
        'id_classroom': classroom.id,
        'id_journey': journey.id,
        'semester': 'KItyv',
        'num_from': 5,
        'num_to': 20,
        'session': 'Rattrapage',
        'id_accademic_year': academic_year.id,
    }

    resp_c = client.post('/api/v1/exam_groups/', json=exam_group_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/exam_groups/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_exam_group_api(client, db):
    """Delete ExamGroup via API."""
    # Auth setup
    user_data = {
        'email': 'qq2NF@7zter.com',
        'last_name': 'VzTWf',
        'password': '1FBXz',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Classroom
    classroom_data = schemas.ClassroomCreate(
        name='U95mD',
        capacity=18,
    )

    classroom = crud.classroom.create(db=db, obj_in=classroom_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='vjmji',
        slug='tJjjj',
        abbreviation='Ao88z',
        plugged='pvoXQ',
        background='LSuvE',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='s1VQo',
        abbreviation='9FIzf',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='wgdTN',
        code='pnmer',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    exam_group_data = {
        'id_classroom': classroom.id,
        'id_journey': journey.id,
        'semester': 'xZiZq',
        'num_from': 9,
        'num_to': 10,
        'session': 'Rattrapage',
        'id_accademic_year': academic_year.id,
    }

    resp_c = client.post('/api/v1/exam_groups/', json=exam_group_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/exam_groups/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'ExamGroup deleted successfully'
    resp_chk = client.get(f'/api/v1/exam_groups/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

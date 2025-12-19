# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_enrollment_fee_api(client, db):
    """Create EnrollmentFee via API."""
    # Auth setup
    user_data = {
        'email': 'bkm7m@kebov.com',
        'last_name': 'hNlco',
        'password': 'USkKS',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='uCd6m',
        slug='niLFM',
        abbreviation='9FPfG',
        plugged='aIdCo',
        background='FX7zi',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='SOewy',
        code='lwY1J',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    enrollment_fee_data = {
        'level': '1',
        'price': 5.418007848574078,
        'id_mention': mention.id,
        'id_academic_year': academic_year.id,
    }

    resp = client.post('/api/v1/enrollment_fees/', json=enrollment_fee_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['level'] == enrollment_fee_data['level']
    assert created['price'] == enrollment_fee_data['price']
    assert created['id_mention'] == enrollment_fee_data['id_mention']
    assert created['id_academic_year'] == enrollment_fee_data['id_academic_year']


def test_update_enrollment_fee_api(client, db):
    """Update EnrollmentFee via API."""
    # Auth setup
    user_data = {
        'email': 'kkIQc@jwgk9.com',
        'last_name': 'stT30',
        'password': 'EAvlZ',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='C1ZD6',
        slug='36KrR',
        abbreviation='1LVtc',
        plugged='slqWT',
        background='qcmlE',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='EVA5V',
        code='yOdc0',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    enrollment_fee_data = {
        'level': '2',
        'price': 5.421612178359355,
        'id_mention': mention.id,
        'id_academic_year': academic_year.id,
    }

    # Precompute enum values for update
    enum_values_map = {}
    enum_values_map['level'] = ['0', '1', '2']

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

    resp_c = client.post('/api/v1/enrollment_fees/', json=enrollment_fee_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = ['id_mention', 'id_academic_year']

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in enrollment_fee_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/enrollment_fees/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['level'] == update_data['level']
    assert updated['price'] == update_data['price']


def test_get_enrollment_fee_api(client, db):
    """Get EnrollmentFee via API."""
    # Auth setup
    user_data = {
        'email': 'h3Ae6@dz5bp.com',
        'last_name': 'k4d2O',
        'password': '80KSD',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='s1jwz',
        slug='s1vtf',
        abbreviation='rt9KJ',
        plugged='4F0RN',
        background='cxllj',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='SSFWP',
        code='NMZdr',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    enrollment_fee_data = {
        'level': '2',
        'price': 4.694490590655504,
        'id_mention': mention.id,
        'id_academic_year': academic_year.id,
    }

    client.post('/api/v1/enrollment_fees/', json=enrollment_fee_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/enrollment_fees/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_enrollment_fee_api(client, db):
    """Get_by_id EnrollmentFee via API."""
    # Auth setup
    user_data = {
        'email': 'FMcC7@olcvq.com',
        'last_name': 'j6fXB',
        'password': 'OHpFF',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='lupV4',
        slug='KH7bM',
        abbreviation='SOn9D',
        plugged='dcx5l',
        background='iRU2O',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='uXXcY',
        code='QXtuS',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    enrollment_fee_data = {
        'level': '1',
        'price': 2.789258742850001,
        'id_mention': mention.id,
        'id_academic_year': academic_year.id,
    }

    resp_c = client.post('/api/v1/enrollment_fees/', json=enrollment_fee_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/enrollment_fees/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_enrollment_fee_api(client, db):
    """Delete EnrollmentFee via API."""
    # Auth setup
    user_data = {
        'email': 'hjuyN@ajo9t.com',
        'last_name': 'mcsG4',
        'password': '9MBQG',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='JYrZm',
        slug='2ZusA',
        abbreviation='ptLKQ',
        plugged='ZmP1Y',
        background='d1TkR',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='9Ugqf',
        code='g7ewa',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    enrollment_fee_data = {
        'level': '0',
        'price': 3.5222438127049043,
        'id_mention': mention.id,
        'id_academic_year': academic_year.id,
    }

    resp_c = client.post('/api/v1/enrollment_fees/', json=enrollment_fee_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/enrollment_fees/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'EnrollmentFee deleted successfully'
    resp_chk = client.get(f'/api/v1/enrollment_fees/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

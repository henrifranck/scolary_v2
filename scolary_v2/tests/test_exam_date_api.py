# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_exam_date_api(client, db):
    """Create ExamDate via API."""
    # Auth setup
    user_data = {
        'email': 'QwUhb@buhu1.com',
        'last_name': 'Quxl5',
        'password': 'XxRo6',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='qG8RW',
        code='2JR60',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    exam_date_data = {
        'id_academic_year': academic_year.id,
        'date_from': '2025-11-15',
        'date_to': '2025-11-15',
        'session': 'UCJzf',
    }

    resp = client.post('/api/v1/exam_dates/', json=exam_date_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['id_academic_year'] == exam_date_data['id_academic_year']
    assert created['date_from'] == exam_date_data['date_from']
    assert created['date_to'] == exam_date_data['date_to']
    assert created['session'] == exam_date_data['session']


def test_update_exam_date_api(client, db):
    """Update ExamDate via API."""
    # Auth setup
    user_data = {
        'email': '6cpk3@b8roj.com',
        'last_name': 'Bzkgm',
        'password': 'hSWGd',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='7q6Ik',
        code='GJL28',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    exam_date_data = {
        'id_academic_year': academic_year.id,
        'date_from': '2025-11-15',
        'date_to': '2025-11-15',
        'session': 'M8E9f',
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
        if k in ['date_from', 'date_to']:
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

    resp_c = client.post('/api/v1/exam_dates/', json=exam_date_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = ['id_academic_year']

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in exam_date_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/exam_dates/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['date_from'] == update_data['date_from']
    assert updated['date_to'] == update_data['date_to']
    assert updated['session'] == update_data['session']


def test_get_exam_date_api(client, db):
    """Get ExamDate via API."""
    # Auth setup
    user_data = {
        'email': 'Q186L@9528n.com',
        'last_name': 'tyPJZ',
        'password': 'DBuUV',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='FL712',
        code='H0ny6',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    exam_date_data = {
        'id_academic_year': academic_year.id,
        'date_from': '2025-11-15',
        'date_to': '2025-11-15',
        'session': 'KHnow',
    }

    client.post('/api/v1/exam_dates/', json=exam_date_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/exam_dates/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_exam_date_api(client, db):
    """Get_by_id ExamDate via API."""
    # Auth setup
    user_data = {
        'email': 'C3Pro@qxblu.com',
        'last_name': 'ULB2t',
        'password': 'wfdCs',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='qB07m',
        code='qDXWG',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    exam_date_data = {
        'id_academic_year': academic_year.id,
        'date_from': '2025-11-15',
        'date_to': '2025-11-15',
        'session': 'Eztt4',
    }

    resp_c = client.post('/api/v1/exam_dates/', json=exam_date_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/exam_dates/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_exam_date_api(client, db):
    """Delete ExamDate via API."""
    # Auth setup
    user_data = {
        'email': 'xBekQ@uapcb.com',
        'last_name': 'ZJhJO',
        'password': 'X79gc',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='PR7LF',
        code='CRkj2',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    exam_date_data = {
        'id_academic_year': academic_year.id,
        'date_from': '2025-11-15',
        'date_to': '2025-11-15',
        'session': 'udl2y',
    }

    resp_c = client.post('/api/v1/exam_dates/', json=exam_date_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/exam_dates/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'ExamDate deleted successfully'
    resp_chk = client.get(f'/api/v1/exam_dates/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

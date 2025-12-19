# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_student_api(client, db):
    """Create Student via API."""
    # Auth setup
    user_data = {
        'email': 'I9B9E@mgkic.com',
        'last_name': 'zj75J',
        'password': 'Vr3FW',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='jRUBr',
        slug='sTv1S',
        abbreviation='8l9LA',
        plugged='4jEFT',
        background='nFj9u',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='pQp8D',
        code='LQIQU',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='qGEO9',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='vpDGn',
        value='VKjis',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    student_data = {
        'num_carte': '8RhB8',
        'email': 'UCQNS@vrf55.com',
        'num_select': 'xU9xd',
        'last_name': 'D1lrK',
        'first_name': 'JRxxM',
        'date_of_birth': '2025-11-15',
        'place_of_birth': '29JJH',
        'address': 'qNoyO5QDbc1oY0ru5mBpVYVjCuHQL4y0Z5KyZQkvVmohPp9jBjLYApVgJnVi2wz',
        'sex': 'Féminin',
        'martial_status': 'Marié(e)',
        'phone_number': 'pl77p',
        'num_of_cin': 'OdR5o',
        'date_of_cin': '2025-11-15',
        'place_of_cin': 'RYf4r',
        'repeat_status': '0',
        'picture': 'FH8Ka',
        'num_of_baccalaureate': 'Xl4LC',
        'center_of_baccalaureate': 'BAheO',
        'year_of_baccalaureate': '2025-11-15',
        'job': 'evDfQ',
        'father_name': 'uXt4l',
        'father_job': 'vDpDb',
        'mother_name': 'T63mE',
        'mother_job': 'qWcHK',
        'parent_address': 'oegUumwFigVINU7ax',
        'level': 'M2',
        'mean': 2.342116136754339,
        'enrollment_status': 'En attente',
        'imported_id': '3XWtt',
        'id_mention': mention.id,
        'id_enter_year': academic_year.id,
        'id_nationality': nationality.id,
        'id_baccalaureate_series': baccalaureate_serie.id,
    }

    resp = client.post('/api/v1/students/', json=student_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['num_carte'] == student_data['num_carte']
    assert created['email'] == student_data['email']
    assert created['num_select'] == student_data['num_select']
    assert created['last_name'] == student_data['last_name']
    assert created['first_name'] == student_data['first_name']
    assert created['date_of_birth'] == student_data['date_of_birth']
    assert created['place_of_birth'] == student_data['place_of_birth']
    assert created['address'] == student_data['address']
    assert created['sex'] == student_data['sex']
    assert created['martial_status'] == student_data['martial_status']
    assert created['phone_number'] == student_data['phone_number']
    assert created['num_of_cin'] == student_data['num_of_cin']
    assert created['date_of_cin'] == student_data['date_of_cin']
    assert created['place_of_cin'] == student_data['place_of_cin']
    assert created['repeat_status'] == student_data['repeat_status']
    assert created['picture'] == student_data['picture']
    assert created['num_of_baccalaureate'] == student_data['num_of_baccalaureate']
    assert created['center_of_baccalaureate'] == student_data['center_of_baccalaureate']
    assert created['year_of_baccalaureate'] == student_data['year_of_baccalaureate']
    assert created['job'] == student_data['job']
    assert created['father_name'] == student_data['father_name']
    assert created['father_job'] == student_data['father_job']
    assert created['mother_name'] == student_data['mother_name']
    assert created['mother_job'] == student_data['mother_job']
    assert created['parent_address'] == student_data['parent_address']
    assert created['level'] == student_data['level']
    assert created['mean'] == student_data['mean']
    assert created['enrollment_status'] == student_data['enrollment_status']
    assert created['imported_id'] == student_data['imported_id']
    assert created['id_mention'] == student_data['id_mention']
    assert created['id_enter_year'] == student_data['id_enter_year']
    assert created['id_nationality'] == student_data['id_nationality']
    assert created['id_baccalaureate_series'] == student_data['id_baccalaureate_series']


def test_update_student_api(client, db):
    """Update Student via API."""
    # Auth setup
    user_data = {
        'email': 'v8TNM@bjjyl.com',
        'last_name': 'Un241',
        'password': 'PZsUO',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='RPPNy',
        slug='c60q9',
        abbreviation='EKIQl',
        plugged='wwjPr',
        background='TEyW5',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='F1hBJ',
        code='MY7Ar',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='Fp0O8',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='EoqFE',
        value='9nj6I',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    student_data = {
        'num_carte': 'HDCGA',
        'email': '1X6p9@l3nn6.com',
        'num_select': '0aOyM',
        'last_name': 'HFjXF',
        'first_name': '4yAeX',
        'date_of_birth': '2025-11-15',
        'place_of_birth': '0plMF',
        'address': 'njN3TENTz64RZSJNdOJ6Cj1F89MlA2V4csrDaU7kN3t0wsqBY2ZTyEAV4veIeDPlkRR',
        'sex': 'Masculin',
        'martial_status': 'Marié(e)',
        'phone_number': 'uSOzd',
        'num_of_cin': 'OZ2fm',
        'date_of_cin': '2025-11-15',
        'place_of_cin': '65Axz',
        'repeat_status': '1',
        'picture': 'gvIGH',
        'num_of_baccalaureate': 'mPQyQ',
        'center_of_baccalaureate': 'qokNI',
        'year_of_baccalaureate': '2025-11-15',
        'job': 'bdHAu',
        'father_name': '3NCSe',
        'father_job': 'AOzUd',
        'mother_name': 'DqDrN',
        'mother_job': 'bPEVF',
        'parent_address': 'ZEsnHBs5RxVCvNNqjgbDPJiAfX7FgFZsOpwA4joSK6YGXIip8VczaIhZRxX1A9Z',
        'level': 'M1',
        'mean': 3.6983797739982047,
        'enrollment_status': 'ancien(ne)',
        'imported_id': '8GDWO',
        'id_mention': mention.id,
        'id_enter_year': academic_year.id,
        'id_nationality': nationality.id,
        'id_baccalaureate_series': baccalaureate_serie.id,
    }

    # Precompute enum values for update
    enum_values_map = {}
    enum_values_map['sex'] = ['Masculin', 'Féminin']
    enum_values_map['martial_status'] = ['Célibataire', 'Marié(e)', 'Divorcé(e)', 'Veuf/Veuve']
    enum_values_map['repeat_status'] = ['0', '1', '2']
    enum_values_map['level'] = ['L1', 'L2', 'L3', 'M1', 'M2']
    enum_values_map['enrollment_status'] = ['En attente', 'Sélectionné(e)', 'Inscrit(e)', 'ancien(ne)']

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
        if k in ['date_of_birth', 'date_of_cin', 'year_of_baccalaureate']:
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

    resp_c = client.post('/api/v1/students/', json=student_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = ['id_mention', 'id_enter_year', 'id_nationality', 'id_baccalaureate_series']

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in student_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/students/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['num_carte'] == update_data['num_carte']
    assert updated['email'] == update_data['email']
    assert updated['num_select'] == update_data['num_select']
    assert updated['last_name'] == update_data['last_name']
    assert updated['first_name'] == update_data['first_name']
    assert updated['date_of_birth'] == update_data['date_of_birth']
    assert updated['place_of_birth'] == update_data['place_of_birth']
    assert updated['address'] == update_data['address']
    assert updated['sex'] == update_data['sex']
    assert updated['martial_status'] == update_data['martial_status']
    assert updated['phone_number'] == update_data['phone_number']
    assert updated['num_of_cin'] == update_data['num_of_cin']
    assert updated['date_of_cin'] == update_data['date_of_cin']
    assert updated['place_of_cin'] == update_data['place_of_cin']
    assert updated['repeat_status'] == update_data['repeat_status']
    assert updated['picture'] == update_data['picture']
    assert updated['num_of_baccalaureate'] == update_data['num_of_baccalaureate']
    assert updated['center_of_baccalaureate'] == update_data['center_of_baccalaureate']
    assert updated['year_of_baccalaureate'] == update_data['year_of_baccalaureate']
    assert updated['job'] == update_data['job']
    assert updated['father_name'] == update_data['father_name']
    assert updated['father_job'] == update_data['father_job']
    assert updated['mother_name'] == update_data['mother_name']
    assert updated['mother_job'] == update_data['mother_job']
    assert updated['parent_address'] == update_data['parent_address']
    assert updated['level'] == update_data['level']
    assert updated['mean'] == update_data['mean']
    assert updated['enrollment_status'] == update_data['enrollment_status']
    assert updated['imported_id'] == update_data['imported_id']


def test_get_student_api(client, db):
    """Get Student via API."""
    # Auth setup
    user_data = {
        'email': 'XbbzG@pnlej.com',
        'last_name': 'nXf4r',
        'password': 'eGJOo',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='HYsoq',
        slug='2Vjxk',
        abbreviation='EuPFd',
        plugged='xyaly',
        background='V85QI',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='bE4Tb',
        code='RWHcM',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='c64Pd',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='RaRpO',
        value='0dtAn',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    student_data = {
        'num_carte': 'UYcfo',
        'email': 'SnB6i@z2l3f.com',
        'num_select': 'VlAkQ',
        'last_name': 'rIADS',
        'first_name': '9unYP',
        'date_of_birth': '2025-11-15',
        'place_of_birth': 'XUWMQ',
        'address': 'ii6',
        'sex': 'Féminin',
        'martial_status': 'Célibataire',
        'phone_number': '4u80n',
        'num_of_cin': 'MP2XF',
        'date_of_cin': '2025-11-15',
        'place_of_cin': 'AthS4',
        'repeat_status': '2',
        'picture': 'AmlNK',
        'num_of_baccalaureate': 'ZTSD3',
        'center_of_baccalaureate': 'QTWzr',
        'year_of_baccalaureate': '2025-11-15',
        'job': 'lXTQ7',
        'father_name': 'BFBWt',
        'father_job': 'kXkss',
        'mother_name': 'QTyyB',
        'mother_job': '1y8kN',
        'parent_address': 'hhfTJ5Sd3TvDto0pixP44OE9XbW1Z39BE9EG32GCOt3',
        'level': 'L2',
        'mean': 3.7859929335925586,
        'enrollment_status': 'En attente',
        'imported_id': 'j0moH',
        'id_mention': mention.id,
        'id_enter_year': academic_year.id,
        'id_nationality': nationality.id,
        'id_baccalaureate_series': baccalaureate_serie.id,
    }

    client.post('/api/v1/students/', json=student_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/students/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_student_api(client, db):
    """Get_by_id Student via API."""
    # Auth setup
    user_data = {
        'email': '41NQK@g8x3n.com',
        'last_name': 'CGmPY',
        'password': 'TDKEI',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='fdPEI',
        slug='ZN02A',
        abbreviation='S3D79',
        plugged='ALtWe',
        background='ovQZG',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='7EjWH',
        code='lSdXR',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='czl93',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='5QvYd',
        value='0CZlb',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    student_data = {
        'num_carte': 'JKhE0',
        'email': 'NITVH@x4vj2.com',
        'num_select': 'LbYg4',
        'last_name': 'eB8h9',
        'first_name': 'ci0sz',
        'date_of_birth': '2025-11-15',
        'place_of_birth': 'ejhqV',
        'address': 'pDPIbJ',
        'sex': 'Masculin',
        'martial_status': 'Veuf/Veuve',
        'phone_number': '3zvBe',
        'num_of_cin': 'Rjxds',
        'date_of_cin': '2025-11-15',
        'place_of_cin': 'UO0fE',
        'repeat_status': '1',
        'picture': 'FRbLu',
        'num_of_baccalaureate': 'JUma3',
        'center_of_baccalaureate': 'P6GPg',
        'year_of_baccalaureate': '2025-11-15',
        'job': 'LNWVY',
        'father_name': '4ix3Y',
        'father_job': 'Cp8cg',
        'mother_name': 'Ec9jG',
        'mother_job': 'Nlygy',
        'parent_address': 'OQIK44tAJmMVZVl6dbGwf75r',
        'level': 'M1',
        'mean': 4.589903194912653,
        'enrollment_status': 'Sélectionné(e)',
        'imported_id': 'wAzMO',
        'id_mention': mention.id,
        'id_enter_year': academic_year.id,
        'id_nationality': nationality.id,
        'id_baccalaureate_series': baccalaureate_serie.id,
    }

    resp_c = client.post('/api/v1/students/', json=student_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/students/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_student_api(client, db):
    """Delete Student via API."""
    # Auth setup
    user_data = {
        'email': 'dUUJp@y1eai.com',
        'last_name': 'iuOva',
        'password': 'Vca7W',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='BcdnH',
        slug='z3O3m',
        abbreviation='9OIWc',
        plugged='2MbT2',
        background='wdmaA',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='wexVV',
        code='2kXUf',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='qdrmW',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='F77qw',
        value='BKTlV',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    student_data = {
        'num_carte': 'J4Jij',
        'email': 'F99Kw@vaotu.com',
        'num_select': 'zZ8yP',
        'last_name': '3PlXd',
        'first_name': 'fvCVN',
        'date_of_birth': '2025-11-15',
        'place_of_birth': 'q7BCU',
        'address': '4GiJQjZ3MAOSovwhMSeehonjNTkhRUETvK0yqLrMQ4Y9G4TEanCiIU',
        'sex': 'Masculin',
        'martial_status': 'Marié(e)',
        'phone_number': 'SvLpM',
        'num_of_cin': 'L8IZi',
        'date_of_cin': '2025-11-15',
        'place_of_cin': 'Pzy21',
        'repeat_status': '1',
        'picture': 'phrw1',
        'num_of_baccalaureate': 'bP0pW',
        'center_of_baccalaureate': 'XJqJf',
        'year_of_baccalaureate': '2025-11-15',
        'job': 'eKT3H',
        'father_name': '7018X',
        'father_job': '35sVT',
        'mother_name': 'ATmrR',
        'mother_job': 'BotMY',
        'parent_address': '68ko8bvgqMgXuQJQWPc',
        'level': 'M2',
        'mean': 3.573850613777101,
        'enrollment_status': 'ancien(ne)',
        'imported_id': 'UUHKV',
        'id_mention': mention.id,
        'id_enter_year': academic_year.id,
        'id_nationality': nationality.id,
        'id_baccalaureate_series': baccalaureate_serie.id,
    }

    resp_c = client.post('/api/v1/students/', json=student_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/students/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'Student deleted successfully'
    resp_chk = client.get(f'/api/v1/students/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

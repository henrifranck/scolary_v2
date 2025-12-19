# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_annual_register_api(client, db):
    """Create AnnualRegister via API."""
    # Auth setup
    user_data = {
        'email': 'AaHvg@iy8ye.com',
        'last_name': 'U5RgX',
        'password': 'mcrQt',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='pqbLT',
        slug='TPIZF',
        abbreviation='RlifV',
        plugged='T7d5x',
        background='tv6T2',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='fWxNO',
        code='jD3x5',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='e7ql3',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='H4CAp',
        value='MPp9m',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='fhmEz',
        email='5OcUs@ti1ey.com',
        num_select='JCRbB',
        last_name='IX6mI',
        first_name='fxips',
        date_of_birth='2025-11-15',
        place_of_birth='rdf6m',
        address='GiyP0OmpNrAT0xeR05MzPudBPsPAluMF70AZqvyqiV0cIkifPto2cObM9ehuzXepw5065dinNUwadfwOml',
        sex='Féminin',
        martial_status='Marié(e)',
        phone_number='dxQ1p',
        num_of_cin='BOmoJ',
        date_of_cin='2025-11-15',
        place_of_cin='aSaVb',
        repeat_status='2',
        picture='74jtW',
        num_of_baccalaureate='2nu7L',
        center_of_baccalaureate='sisFj',
        year_of_baccalaureate='2025-11-15',
        job='7qbjD',
        father_name='5DqWZ',
        father_job='9epPo',
        mother_name='V9yBK',
        mother_job='D9ZeE',
        parent_address='U75pv22mLh6vkQlQjrlwnjPxWZ3g9xXH',
        level='L1',
        mean=4.33551359634863,
        enrollment_status='ancien(ne)',
        imported_id='k0y1k',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='VZtfx',
        code='ppkN5',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=1.674637940368671,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    annual_register_data = {
        'num_carte': student.num_carte,
        'id_academic_year': academic_year.id,
        'semester_count': 20,
        'id_enrollment_fee': enrollment_fee.id,
    }

    resp = client.post('/api/v1/annual_registers/', json=annual_register_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['num_carte'] == annual_register_data['num_carte']
    assert created['id_academic_year'] == annual_register_data['id_academic_year']
    assert created['semester_count'] == annual_register_data['semester_count']
    assert created['id_enrollment_fee'] == annual_register_data['id_enrollment_fee']


def test_update_annual_register_api(client, db):
    """Update AnnualRegister via API."""
    # Auth setup
    user_data = {
        'email': 'iWVDf@9s4ep.com',
        'last_name': 'lx6nU',
        'password': '8vHA1',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='7b4d5',
        slug='S4P5I',
        abbreviation='x2F5J',
        plugged='I8PM6',
        background='kyW7y',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='PhwKH',
        code='qZjX1',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='kYHkR',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='PnBVV',
        value='1ozrA',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='dNflE',
        email='M58Wx@8piov.com',
        num_select='rsrJ8',
        last_name='Edl79',
        first_name='vtfQk',
        date_of_birth='2025-11-15',
        place_of_birth='U4FM9',
        address='J7YdGNzt6u3qHwwBY2BLmQV904AGiJbg23bh13yHrynyG',
        sex='Masculin',
        martial_status='Divorcé(e)',
        phone_number='2GkxB',
        num_of_cin='tEY0N',
        date_of_cin='2025-11-15',
        place_of_cin='K2aIF',
        repeat_status='1',
        picture='yKcnN',
        num_of_baccalaureate='vWQCT',
        center_of_baccalaureate='o2mbC',
        year_of_baccalaureate='2025-11-15',
        job='DvHRn',
        father_name='MSbeo',
        father_job='JdhWx',
        mother_name='wVMB2',
        mother_job='cSsHQ',
        parent_address='eSWB6Yttin2MJq34xskf2BVH389sFtfge2hIk',
        level='L2',
        mean=1.7013801315843775,
        enrollment_status='ancien(ne)',
        imported_id='9RSpE',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='t7IVr',
        code='vNfGM',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=1.5668793968747026,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    annual_register_data = {
        'num_carte': student.num_carte,
        'id_academic_year': academic_year.id,
        'semester_count': 3,
        'id_enrollment_fee': enrollment_fee.id,
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

    resp_c = client.post('/api/v1/annual_registers/', json=annual_register_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = ['num_carte', 'id_academic_year', 'id_enrollment_fee']

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in annual_register_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/annual_registers/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['semester_count'] == update_data['semester_count']


def test_get_annual_register_api(client, db):
    """Get AnnualRegister via API."""
    # Auth setup
    user_data = {
        'email': 'Zojty@2dsf5.com',
        'last_name': 'lFIHi',
        'password': 'hU61l',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='iTKFP',
        slug='4WvKw',
        abbreviation='f7sLl',
        plugged='akDfc',
        background='p0q6O',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='0ZJG4',
        code='6vcRw',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='QSsBc',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='8c6ku',
        value='wO316',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='e1Y0x',
        email='gkL2f@yzbkg.com',
        num_select='hRwO7',
        last_name='pO4JN',
        first_name='51cRW',
        date_of_birth='2025-11-15',
        place_of_birth='Meshi',
        address='1',
        sex='Masculin',
        martial_status='Célibataire',
        phone_number='2KN4S',
        num_of_cin='Lwt6Z',
        date_of_cin='2025-11-15',
        place_of_cin='RYc2H',
        repeat_status='1',
        picture='7Cj0w',
        num_of_baccalaureate='5BzP7',
        center_of_baccalaureate='WW1R7',
        year_of_baccalaureate='2025-11-15',
        job='llDon',
        father_name='ESktl',
        father_job='qSZ2i',
        mother_name='cm33F',
        mother_job='PGafH',
        parent_address='nJic9Uk7i3OX6kSHFKBt',
        level='M2',
        mean=4.297319253979691,
        enrollment_status='Inscrit(e)',
        imported_id='nByZU',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='6F95o',
        code='Xygnt',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=4.006810174551051,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    annual_register_data = {
        'num_carte': student.num_carte,
        'id_academic_year': academic_year.id,
        'semester_count': 16,
        'id_enrollment_fee': enrollment_fee.id,
    }

    client.post('/api/v1/annual_registers/', json=annual_register_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/annual_registers/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_annual_register_api(client, db):
    """Get_by_id AnnualRegister via API."""
    # Auth setup
    user_data = {
        'email': 'G6OEB@wcouf.com',
        'last_name': 'Hr1Wg',
        'password': 'ND7o4',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='2S8dM',
        slug='PPyAO',
        abbreviation='f1xc2',
        plugged='pQj3e',
        background='ANZrp',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='N4xzS',
        code='vwckc',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='NQb7s',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='8zazx',
        value='YezAp',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='L4nnd',
        email='zJEmh@mhf46.com',
        num_select='OzRvY',
        last_name='DsR43',
        first_name='SBLuz',
        date_of_birth='2025-11-15',
        place_of_birth='Pc4Hk',
        address='JZ8KCWZMUbGo2vWp9tckai',
        sex='Féminin',
        martial_status='Veuf/Veuve',
        phone_number='crZxZ',
        num_of_cin='6C1TD',
        date_of_cin='2025-11-15',
        place_of_cin='K5w4S',
        repeat_status='0',
        picture='Tmulb',
        num_of_baccalaureate='vryvZ',
        center_of_baccalaureate='QurFU',
        year_of_baccalaureate='2025-11-15',
        job='BWo3N',
        father_name='Yb7HI',
        father_job='nToUo',
        mother_name='YrLCg',
        mother_job='Zj40y',
        parent_address='mcEKZMxLLMIVfKHSqRRBCV9zJ8obAvCFwydQSXq0L4ZFkqgb4AgkspHCw9ufWqh9rsYcUOrTWKhGJaPH',
        level='L3',
        mean=4.888270078176465,
        enrollment_status='En attente',
        imported_id='drnxN',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='Yq38d',
        code='JNQWv',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=1.6753534886460444,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    annual_register_data = {
        'num_carte': student.num_carte,
        'id_academic_year': academic_year.id,
        'semester_count': 6,
        'id_enrollment_fee': enrollment_fee.id,
    }

    resp_c = client.post('/api/v1/annual_registers/', json=annual_register_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/annual_registers/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_annual_register_api(client, db):
    """Delete AnnualRegister via API."""
    # Auth setup
    user_data = {
        'email': 'SdU1K@xr38n.com',
        'last_name': '3zf1c',
        'password': 'rPvqG',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='g7oCs',
        slug='VR4bY',
        abbreviation='wsRzM',
        plugged='sjCRc',
        background='7RuAq',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='IeyJE',
        code='PfW7n',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='OoNDg',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='9aHej',
        value='9M0wm',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='Pp26J',
        email='Hbdwq@phtqw.com',
        num_select='NkjcE',
        last_name='Rtq9O',
        first_name='ynHfK',
        date_of_birth='2025-11-15',
        place_of_birth='3Cg4n',
        address='GkLCyMpzmA7gwfnJbCkiVHQtZPmBm8jAWyyVJqkF7GSaDEYikkLtSsEQKMLaUhtua5tNd38FK',
        sex='Féminin',
        martial_status='Marié(e)',
        phone_number='jbQ4Z',
        num_of_cin='HcXmQ',
        date_of_cin='2025-11-15',
        place_of_cin='V7oU6',
        repeat_status='1',
        picture='0k7cS',
        num_of_baccalaureate='USVBT',
        center_of_baccalaureate='vwaGR',
        year_of_baccalaureate='2025-11-15',
        job='mnqVA',
        father_name='dzXLx',
        father_job='jaRtw',
        mother_name='Hpr9e',
        mother_job='r7t6l',
        parent_address='hrfyoEYuky9GKO4j64lz2QfLf0O83t',
        level='L2',
        mean=4.229214679411633,
        enrollment_status='ancien(ne)',
        imported_id='ICBr6',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='0Z7MA',
        code='i96ve',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='1',
        price=3.3400119341541883,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    annual_register_data = {
        'num_carte': student.num_carte,
        'id_academic_year': academic_year.id,
        'semester_count': 16,
        'id_enrollment_fee': enrollment_fee.id,
    }

    resp_c = client.post('/api/v1/annual_registers/', json=annual_register_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/annual_registers/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'AnnualRegister deleted successfully'
    resp_chk = client.get(f'/api/v1/annual_registers/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

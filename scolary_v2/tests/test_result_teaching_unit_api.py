# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_result_teaching_unit_api(client, db):
    """Create ResultTeachingUnit via API."""
    # Auth setup
    user_data = {
        'email': 'v4KQt@rwflr.com',
        'last_name': '6miDX',
        'password': 'V63x6',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='lVKjN',
        slug='riV3a',
        abbreviation='12KmA',
        plugged='C65BX',
        background='nXISl',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='6MdJt',
        code='jaNQh',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='tyCiG',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='ViVfC',
        value='hgB5v',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='Ua6Je',
        email='Rsikj@3kai5.com',
        num_select='M5wfU',
        last_name='9SF3O',
        first_name='A6WQX',
        date_of_birth='2025-11-15',
        place_of_birth='QAoNf',
        address='34w7je9sFYzjtJSprOXoawa7iGeZf75URR57pUnGWkOCSqkRpdpNDxKe',
        sex='Masculin',
        martial_status='Marié(e)',
        phone_number='9uDRM',
        num_of_cin='rdWsX',
        date_of_cin='2025-11-15',
        place_of_cin='J41rj',
        repeat_status='0',
        picture='NRU96',
        num_of_baccalaureate='oP9et',
        center_of_baccalaureate='giY7C',
        year_of_baccalaureate='2025-11-15',
        job='YIPZD',
        father_name='MpwiQ',
        father_job='k6tdT',
        mother_name='CSPwQ',
        mother_job='IE1XQ',
        parent_address='WEA3hMwlThrqhOtAbOIXrVVq5RPF9udwhWiG47Zzu3lQs2SlhvOQlgZGDPXubTYxVs4DqL464uEdd4w9S6FZR1CnwaU',
        level='M2',
        mean=5.162381196188569,
        enrollment_status='En attente',
        imported_id='uqKbB',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=5.435412285094282,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=11,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='5Px2M',
        abbreviation='IYiwY',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='sXq0s',
        repeat_status='0',
        id_journey=journey.id,
        imported_id='TbFrO',
        is_valid=False,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    result_teaching_unit_data = {
        'id_register_semester': register_semester.id,
        'note': 2.155871309361012,
        'is_valid': False,
        'date_validation': '2025-11-15T18:57:08.835776',
        'comment': 'kzgE3RAoHXEUAyP2lbU8DUSnuZJ59sttl',
    }

    resp = client.post('/api/v1/result_teaching_units/', json=result_teaching_unit_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['id_register_semester'] == result_teaching_unit_data['id_register_semester']
    assert created['note'] == result_teaching_unit_data['note']
    assert created['is_valid'] == result_teaching_unit_data['is_valid']
    assert created['comment'] == result_teaching_unit_data['comment']


def test_update_result_teaching_unit_api(client, db):
    """Update ResultTeachingUnit via API."""
    # Auth setup
    user_data = {
        'email': 'OUoa9@r7rmc.com',
        'last_name': 'Mm3qW',
        'password': 'woClw',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='j6IsU',
        slug='m151F',
        abbreviation='3TVFw',
        plugged='0MRy1',
        background='8o4IO',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='TQsmY',
        code='u566Q',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='zrMnV',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='7axLq',
        value='yijTL',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='g5bt3',
        email='0XAxD@tonou.com',
        num_select='3vcop',
        last_name='Jf0IU',
        first_name='XTk8S',
        date_of_birth='2025-11-15',
        place_of_birth='b6wMx',
        address='4z1Mc7ezC2cwGKeAhHKkDXtoDR',
        sex='Masculin',
        martial_status='Marié(e)',
        phone_number='8JSj4',
        num_of_cin='BYkAX',
        date_of_cin='2025-11-15',
        place_of_cin='mwQhK',
        repeat_status='0',
        picture='JMH4t',
        num_of_baccalaureate='e5RBg',
        center_of_baccalaureate='7yjer',
        year_of_baccalaureate='2025-11-15',
        job='46NGm',
        father_name='fWEyU',
        father_job='TGedA',
        mother_name='bghQ1',
        mother_job='LTxE1',
        parent_address='03kiGSiryDcILhEhFwayjIRpgL9y',
        level='L1',
        mean=3.956673511316406,
        enrollment_status='Sélectionné(e)',
        imported_id='Vy2xR',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=2.0813236746732,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=17,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='nK5bt',
        abbreviation='zsc7t',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='Iiloq',
        repeat_status='0',
        id_journey=journey.id,
        imported_id='fFMNv',
        is_valid=False,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    result_teaching_unit_data = {
        'id_register_semester': register_semester.id,
        'note': 3.528840960011259,
        'is_valid': False,
        'date_validation': '2025-11-15T18:57:08.836936',
        'comment': 'rMwLJzIFxZPabnY5yXEZjvoHjlpGClIICxr',
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
        if k in ['date_validation']:
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

    resp_c = client.post('/api/v1/result_teaching_units/', json=result_teaching_unit_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = ['id_register_semester']

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in result_teaching_unit_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/result_teaching_units/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['note'] == update_data['note']
    assert updated['is_valid'] == update_data['is_valid']
    assert updated['date_validation'] == update_data['date_validation']
    assert updated['comment'] == update_data['comment']


def test_get_result_teaching_unit_api(client, db):
    """Get ResultTeachingUnit via API."""
    # Auth setup
    user_data = {
        'email': 'xOWtZ@u5eg2.com',
        'last_name': 'ebUhk',
        'password': 'o6REd',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='YtXc1',
        slug='TfzCd',
        abbreviation='XS84L',
        plugged='dNJI9',
        background='HEa9Z',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='Rpolb',
        code='uq4h5',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='wiAzS',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='QVVlV',
        value='cI6Kp',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='3s1rW',
        email='0i463@cpcwc.com',
        num_select='Xqzg5',
        last_name='q8Jj0',
        first_name='mbX5M',
        date_of_birth='2025-11-15',
        place_of_birth='9p8iu',
        address='E5SNhqtfyGhUyy2qAhb25IHH3QSXYcqFeynFUd2XQkJQxQG89lfKAdZ4fQJQHNQHlYQVwfsZt',
        sex='Masculin',
        martial_status='Veuf/Veuve',
        phone_number='epYJ4',
        num_of_cin='D46bx',
        date_of_cin='2025-11-15',
        place_of_cin='Y3B0L',
        repeat_status='1',
        picture='CJkWM',
        num_of_baccalaureate='LWuDt',
        center_of_baccalaureate='zvLTW',
        year_of_baccalaureate='2025-11-15',
        job='JZhSw',
        father_name='BYW5T',
        father_job='ZDYcz',
        mother_name='dzNlF',
        mother_job='Mdjph',
        parent_address='lJNM',
        level='L2',
        mean=1.967048334950352,
        enrollment_status='ancien(ne)',
        imported_id='GdNmW',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=3.6021863687712283,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=12,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='z1djP',
        abbreviation='N24T1',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='GAU62',
        repeat_status='0',
        id_journey=journey.id,
        imported_id='S3vJ7',
        is_valid=True,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    result_teaching_unit_data = {
        'id_register_semester': register_semester.id,
        'note': 5.2129380909161736,
        'is_valid': True,
        'date_validation': '2025-11-15T18:57:08.838117',
        'comment': 'j12qOZfK9bpSfdkx',
    }

    client.post('/api/v1/result_teaching_units/', json=result_teaching_unit_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/result_teaching_units/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_result_teaching_unit_api(client, db):
    """Get_by_id ResultTeachingUnit via API."""
    # Auth setup
    user_data = {
        'email': 'EVaDA@szh2w.com',
        'last_name': '0M6Os',
        'password': 'tcZTH',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='yrWSy',
        slug='aoJhQ',
        abbreviation='AtNLz',
        plugged='hh4Kb',
        background='gA70u',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='jp6LQ',
        code='0Q0U6',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='EDbgg',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='0OAcB',
        value='mqbVD',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='bGd27',
        email='qZTlM@vozvu.com',
        num_select='1yX4W',
        last_name='EWFqR',
        first_name='NQoI6',
        date_of_birth='2025-11-15',
        place_of_birth='f5yCh',
        address='fTV1GpvHiqrRPh6qAVyEoyZWacam4l1LAIFlePDe9BM3',
        sex='Masculin',
        martial_status='Veuf/Veuve',
        phone_number='gHEtS',
        num_of_cin='O53sI',
        date_of_cin='2025-11-15',
        place_of_cin='zFA0F',
        repeat_status='1',
        picture='eUqw9',
        num_of_baccalaureate='3U4sI',
        center_of_baccalaureate='VpENK',
        year_of_baccalaureate='2025-11-15',
        job='KvCGb',
        father_name='O38he',
        father_job='ddKjf',
        mother_name='lM7DH',
        mother_job='gfDeY',
        parent_address='JEUXm5ewG84U0mm5FtXnAaLnt3VDgDCPdIY62CyEZ3TPpm7uD6zos6nfoOBIVbObH28WsNMgVLtDSVvF5N',
        level='L1',
        mean=2.6703140547735535,
        enrollment_status='En attente',
        imported_id='m3taX',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=5.001959725298841,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=2,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='zczzI',
        abbreviation='PenG5',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='hwTwj',
        repeat_status='2',
        id_journey=journey.id,
        imported_id='z8qLX',
        is_valid=False,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    result_teaching_unit_data = {
        'id_register_semester': register_semester.id,
        'note': 2.102654499198117,
        'is_valid': False,
        'date_validation': '2025-11-15T18:57:08.840239',
        'comment': 'qNvcy5NHEnc1AAV0p8sVXA5mqR43bz',
    }

    resp_c = client.post('/api/v1/result_teaching_units/', json=result_teaching_unit_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/result_teaching_units/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_result_teaching_unit_api(client, db):
    """Delete ResultTeachingUnit via API."""
    # Auth setup
    user_data = {
        'email': '01iWB@64om5.com',
        'last_name': '7KMqa',
        'password': 'iPUQW',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='58nXc',
        slug='gtMT2',
        abbreviation='EFpP6',
        plugged='K7qEZ',
        background='iJW2V',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='TaeO1',
        code='5VNQL',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='MqoJ0',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='ydfrT',
        value='5izex',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='ae4ig',
        email='rhdwr@d5ndb.com',
        num_select='xzhpG',
        last_name='iKHmd',
        first_name='VOZc0',
        date_of_birth='2025-11-15',
        place_of_birth='r1kd5',
        address='PF6tGALhEW1nEb',
        sex='Féminin',
        martial_status='Divorcé(e)',
        phone_number='GBWua',
        num_of_cin='p7rOA',
        date_of_cin='2025-11-15',
        place_of_cin='1kNmk',
        repeat_status='2',
        picture='rHxeh',
        num_of_baccalaureate='8zC7g',
        center_of_baccalaureate='xAO7x',
        year_of_baccalaureate='2025-11-15',
        job='ThCx6',
        father_name='GcrXS',
        father_job='kIryL',
        mother_name='M2fwW',
        mother_job='CNVKq',
        parent_address='oYiTn5ajfROwhB3mrrsna5eW6yi9dPIu8C7ODqabLhaXXbxfOOvbbjRioTDiEZxckkFI4quTUTOl22aEdZIXUcEEfZ',
        level='L2',
        mean=1.9633556541246246,
        enrollment_status='ancien(ne)',
        imported_id='oo0ws',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=2.77878260112064,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=6,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='F4NlN',
        abbreviation='ckQP4',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='JRXP5',
        repeat_status='1',
        id_journey=journey.id,
        imported_id='R7uiL',
        is_valid=True,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    result_teaching_unit_data = {
        'id_register_semester': register_semester.id,
        'note': 4.880823317768529,
        'is_valid': False,
        'date_validation': '2025-11-15T18:57:08.876356',
        'comment': 'zFxFXa1ITyZELbz4B5z5W5kJTK6CMnrhDPGJIBsUSgyi85s9nE60q9efr7J3viA3xbA0Yx2rz6n5jvezO7o',
    }

    resp_c = client.post('/api/v1/result_teaching_units/', json=result_teaching_unit_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/result_teaching_units/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'ResultTeachingUnit deleted successfully'
    resp_chk = client.get(f'/api/v1/result_teaching_units/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

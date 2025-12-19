# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_register_semester_api(client, db):
    """Create RegisterSemester via API."""
    # Auth setup
    user_data = {
        'email': 'vjzR4@ja1ix.com',
        'last_name': 'lfsPw',
        'password': 'wZsEQ',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='JboB6',
        slug='sVCE2',
        abbreviation='ZmH9E',
        plugged='qSe3V',
        background='xfT9a',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='IzL2R',
        code='WuGDT',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='rA4DC',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='EeTID',
        value='0zyr5',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='6eQAQ',
        email='yPSmY@vme9o.com',
        num_select='RLP5y',
        last_name='3zpPr',
        first_name='h5tPU',
        date_of_birth='2025-11-15',
        place_of_birth='mEq8u',
        address='9bWEMseJrvNNdP82jOH9',
        sex='Masculin',
        martial_status='Célibataire',
        phone_number='WFLRT',
        num_of_cin='TX4pa',
        date_of_cin='2025-11-15',
        place_of_cin='QE85X',
        repeat_status='2',
        picture='2CX2E',
        num_of_baccalaureate='bfBt9',
        center_of_baccalaureate='XXd0s',
        year_of_baccalaureate='2025-11-15',
        job='QMcVb',
        father_name='CUq2P',
        father_job='sBlT6',
        mother_name='h4YYp',
        mother_job='oo83b',
        parent_address='DKmOGcY326l1m95M3aOeSrd4L3nDYn0te7QAOti5tFYlH3CBGJvt2u9llcboOvuw7bAUWGgICJClG0Pzrmhdz8xo7F',
        level='L1',
        mean=1.93955943516549,
        enrollment_status='ancien(ne)',
        imported_id='4jwkW',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=2.4637824582046033,
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
        name='f28Kw',
        abbreviation='q4cEY',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    register_semester_data = {
        'id_annual_register': annual_register.id,
        'semester': 'VOra7',
        'repeat_status': '0',
        'id_journey': journey.id,
        'imported_id': 'WvuBf',
        'is_valid': False,
    }

    resp = client.post('/api/v1/register_semesters/', json=register_semester_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['id_annual_register'] == register_semester_data['id_annual_register']
    assert created['semester'] == register_semester_data['semester']
    assert created['repeat_status'] == register_semester_data['repeat_status']
    assert created['id_journey'] == register_semester_data['id_journey']
    assert created['imported_id'] == register_semester_data['imported_id']
    assert created['is_valid'] == register_semester_data['is_valid']


def test_update_register_semester_api(client, db):
    """Update RegisterSemester via API."""
    # Auth setup
    user_data = {
        'email': 'fgh7y@cmrel.com',
        'last_name': 'mNFDY',
        'password': '14hG8',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='zlfiQ',
        slug='JIXKP',
        abbreviation='uvTw0',
        plugged='77jWh',
        background='95Qfn',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='ygKw2',
        code='7h3U6',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='aNQke',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='62LB8',
        value='hnAly',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='1jJiw',
        email='5QW6Y@sabqm.com',
        num_select='ECf0K',
        last_name='uVGLg',
        first_name='SxprP',
        date_of_birth='2025-11-15',
        place_of_birth='jM0ZY',
        address='YGJ3JOQpeulfrLyExCegdTHaup72qNIaWSqFE5XcH9zKir2T9e5MvIG2aES4MptBhaoco2sMQZr0TdH2SJAhHSo3MhO1ytcdcb',
        sex='Masculin',
        martial_status='Divorcé(e)',
        phone_number='7nGU8',
        num_of_cin='TbwIj',
        date_of_cin='2025-11-15',
        place_of_cin='ppbN1',
        repeat_status='1',
        picture='oBuH1',
        num_of_baccalaureate='WWTGl',
        center_of_baccalaureate='5U0qk',
        year_of_baccalaureate='2025-11-15',
        job='ebKKC',
        father_name='S0HYy',
        father_job='D8N99',
        mother_name='lXFvM',
        mother_job='wxjZm',
        parent_address='TGcFsKLnnxSOXz7Ze7GsGax2LtFou0jc1a0VljOclwJgnb16hJUITOI2e0713X9m36gi4N66GKoY8JP3t4RtR',
        level='M2',
        mean=2.3845070465958234,
        enrollment_status='Sélectionné(e)',
        imported_id='WjRRv',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='1',
        price=1.542250581204892,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=5,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='NuIEH',
        abbreviation='FOHnC',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    register_semester_data = {
        'id_annual_register': annual_register.id,
        'semester': 'rkWGh',
        'repeat_status': '2',
        'id_journey': journey.id,
        'imported_id': 'icVwx',
        'is_valid': True,
    }

    # Precompute enum values for update
    enum_values_map = {}
    enum_values_map['repeat_status'] = ['0', '1', '2']

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

    resp_c = client.post('/api/v1/register_semesters/', json=register_semester_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = ['id_annual_register', 'id_journey']

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in register_semester_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/register_semesters/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['semester'] == update_data['semester']
    assert updated['repeat_status'] == update_data['repeat_status']
    assert updated['imported_id'] == update_data['imported_id']
    assert updated['is_valid'] == update_data['is_valid']


def test_get_register_semester_api(client, db):
    """Get RegisterSemester via API."""
    # Auth setup
    user_data = {
        'email': 'DiDO3@friud.com',
        'last_name': 'SClan',
        'password': 'NmLlB',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='fmamy',
        slug='7K3DG',
        abbreviation='4gOnh',
        plugged='IxiXd',
        background='sEe5z',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='2uMsc',
        code='wn5Zj',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='S00Fx',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='4Ys52',
        value='KhMOM',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='Da9Wn',
        email='ei63w@cz6ty.com',
        num_select='Ahetn',
        last_name='HQbWc',
        first_name='9zkLa',
        date_of_birth='2025-11-15',
        place_of_birth='QaEjo',
        address='SMs8yzy1sof3KVBhxqGozOuKPBVajiZ4ex',
        sex='Masculin',
        martial_status='Divorcé(e)',
        phone_number='uncFM',
        num_of_cin='G5Z0e',
        date_of_cin='2025-11-15',
        place_of_cin='h9Ylf',
        repeat_status='2',
        picture='7q4gE',
        num_of_baccalaureate='3vWru',
        center_of_baccalaureate='UA0wF',
        year_of_baccalaureate='2025-11-15',
        job='79JAJ',
        father_name='hCgdV',
        father_job='bX0Xj',
        mother_name='hA4gr',
        mother_job='pWN20',
        parent_address='bvn3EDjbcRt8',
        level='M1',
        mean=2.1031744497442006,
        enrollment_status='ancien(ne)',
        imported_id='ABK4J',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=2.7000973553151084,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=4,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='B6CWY',
        abbreviation='gsm7P',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    register_semester_data = {
        'id_annual_register': annual_register.id,
        'semester': 'G5ZzY',
        'repeat_status': '1',
        'id_journey': journey.id,
        'imported_id': 'XB4wx',
        'is_valid': True,
    }

    client.post('/api/v1/register_semesters/', json=register_semester_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/register_semesters/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_register_semester_api(client, db):
    """Get_by_id RegisterSemester via API."""
    # Auth setup
    user_data = {
        'email': 'DhUTf@vcyet.com',
        'last_name': 'O1YXV',
        'password': 'H0YGu',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='pPfs0',
        slug='bB42S',
        abbreviation='DBpjU',
        plugged='IWEiW',
        background='sQIFO',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='5mVpU',
        code='cCHlA',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='2qPS5',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='nZ7Z1',
        value='6oddk',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='XWGUa',
        email='lMmBH@defzu.com',
        num_select='E76qe',
        last_name='yPDx0',
        first_name='A450O',
        date_of_birth='2025-11-15',
        place_of_birth='VlYtJ',
        address='tyMLGXS7cDKZoRl7s6ufcBqa9DBuPCOSVPZiW3oIzMMG',
        sex='Féminin',
        martial_status='Marié(e)',
        phone_number='z37Pu',
        num_of_cin='xqvgf',
        date_of_cin='2025-11-15',
        place_of_cin='bQJPF',
        repeat_status='0',
        picture='I72rL',
        num_of_baccalaureate='BKKJn',
        center_of_baccalaureate='JjBU6',
        year_of_baccalaureate='2025-11-15',
        job='kn5cB',
        father_name='JwBb5',
        father_job='6I3pL',
        mother_name='57GuK',
        mother_job='nD5KB',
        parent_address='9j9XIl36Dk2ik9fS',
        level='L1',
        mean=2.9068150240836266,
        enrollment_status='Sélectionné(e)',
        imported_id='gKf2S',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=2.612315684369723,
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
        name='H9zLQ',
        abbreviation='xoliB',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    register_semester_data = {
        'id_annual_register': annual_register.id,
        'semester': 'ytW9a',
        'repeat_status': '0',
        'id_journey': journey.id,
        'imported_id': 'wRu0W',
        'is_valid': False,
    }

    resp_c = client.post('/api/v1/register_semesters/', json=register_semester_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/register_semesters/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_register_semester_api(client, db):
    """Delete RegisterSemester via API."""
    # Auth setup
    user_data = {
        'email': 'Ttpzr@4h5s5.com',
        'last_name': 'UEfdD',
        'password': 'kvDLI',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='Yog7J',
        slug='ab1qL',
        abbreviation='SxWGs',
        plugged='eKzds',
        background='VdqhH',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='bF1hZ',
        code='bV7ED',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='BosOi',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='gv0c7',
        value='zzojN',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='gfpbe',
        email='j8FXe@xrnfl.com',
        num_select='aZcT5',
        last_name='uIddk',
        first_name='1G5oA',
        date_of_birth='2025-11-15',
        place_of_birth='pA2w9',
        address='SDx2zcGpKI1OvpEab7lbV2x0HK',
        sex='Masculin',
        martial_status='Célibataire',
        phone_number='xer4L',
        num_of_cin='ll21L',
        date_of_cin='2025-11-15',
        place_of_cin='r95uS',
        repeat_status='2',
        picture='isxLZ',
        num_of_baccalaureate='1LtbW',
        center_of_baccalaureate='4DN6R',
        year_of_baccalaureate='2025-11-15',
        job='KvYaI',
        father_name='69zqW',
        father_job='3gFnx',
        mother_name='QU67t',
        mother_job='goMLv',
        parent_address='YfcAWpZfSXirwB2FjmcAo1rc3tKY5FTmL9SPrPMpMxIblaPIWqKbNlGPrj5iMikDwxNN6MGKV7RFN',
        level='L3',
        mean=4.566617659534366,
        enrollment_status='ancien(ne)',
        imported_id='WMIc0',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=5.3255447478327405,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=13,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='Ha1jD',
        abbreviation='Frye8',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    register_semester_data = {
        'id_annual_register': annual_register.id,
        'semester': 'fLutB',
        'repeat_status': '2',
        'id_journey': journey.id,
        'imported_id': 'tEOeC',
        'is_valid': False,
    }

    resp_c = client.post('/api/v1/register_semesters/', json=register_semester_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/register_semesters/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'RegisterSemester deleted successfully'
    resp_chk = client.get(f'/api/v1/register_semesters/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

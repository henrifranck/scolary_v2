# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_payment_api(client, db):
    """Create Payment via API."""
    # Auth setup
    user_data = {
        'email': 'OHoOI@vszcf.com',
        'last_name': 'oKRbG',
        'password': 'HsN7r',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='vb2oF',
        slug='T0KO2',
        abbreviation='qQcFx',
        plugged='fMKLc',
        background='WseKq',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='uqKuR',
        code='gdfCl',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='szYTB',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='QREWj',
        value='Oc6in',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='i6pO4',
        email='FE8ot@hs7ob.com',
        num_select='fx6ed',
        last_name='oAHgw',
        first_name='kSAt3',
        date_of_birth='2025-11-15',
        place_of_birth='wPSVZ',
        address='avotSeufn29HVpUDHS6nRhiFRnEpnJQUV7CpKjJ9kManO3YvFVmIUOjA',
        sex='Féminin',
        martial_status='Marié(e)',
        phone_number='ZmF1G',
        num_of_cin='ohYfV',
        date_of_cin='2025-11-15',
        place_of_cin='CR6UY',
        repeat_status='0',
        picture='tobgK',
        num_of_baccalaureate='jZKQ0',
        center_of_baccalaureate='peyvn',
        year_of_baccalaureate='2025-11-15',
        job='Ol4nF',
        father_name='JiSW9',
        father_job='Ve0y5',
        mother_name='R2qSb',
        mother_job='FFlOn',
        parent_address='oo2rjPAXHF',
        level='L1',
        mean=1.710808341641271,
        enrollment_status='ancien(ne)',
        imported_id='mBMKf',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=3.0399428835622624,
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

    payment_data = {
        'id_annual_register': annual_register.id,
        'payed': 4.989034798739679,
        'num_receipt': 'OMnpt',
        'date_receipt': '2025-11-15',
    }

    resp = client.post('/api/v1/payments/', json=payment_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['id_annual_register'] == payment_data['id_annual_register']
    assert created['payed'] == payment_data['payed']
    assert created['num_receipt'] == payment_data['num_receipt']
    assert created['date_receipt'] == payment_data['date_receipt']


def test_update_payment_api(client, db):
    """Update Payment via API."""
    # Auth setup
    user_data = {
        'email': 'SuNHO@f1yjd.com',
        'last_name': 'Wxjlw',
        'password': 'UGNrB',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='gjHuG',
        slug='41uRx',
        abbreviation='RiCz2',
        plugged='omBeY',
        background='6YXrU',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='pQAvo',
        code='XPeLX',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='uMUrr',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='ehW9P',
        value='PqFyn',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='jftth',
        email='MN5Pj@d2s8c.com',
        num_select='UWD0h',
        last_name='tXCm6',
        first_name='xBSmO',
        date_of_birth='2025-11-15',
        place_of_birth='mf0S4',
        address='qwxWbHoPHZJlMIH6QjkDuc3SJyZiLspjMJ',
        sex='Masculin',
        martial_status='Marié(e)',
        phone_number='vDLJ3',
        num_of_cin='qPwIO',
        date_of_cin='2025-11-15',
        place_of_cin='CrX30',
        repeat_status='2',
        picture='JRrZR',
        num_of_baccalaureate='1VyTp',
        center_of_baccalaureate='GoYeJ',
        year_of_baccalaureate='2025-11-15',
        job='jY7e4',
        father_name='Ygqvk',
        father_job='BZbQk',
        mother_name='GAztP',
        mother_job='m8dza',
        parent_address='gJxsMETRiB8p4tXPKFQbh6e90PKS0uoc0QFkgepmLDfE2dFojiXRrJdeA7zSl5BWKSM7sR71m',
        level='M2',
        mean=1.8813076143757308,
        enrollment_status='Inscrit(e)',
        imported_id='NokXV',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='1',
        price=2.221045891372305,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=7,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    payment_data = {
        'id_annual_register': annual_register.id,
        'payed': 4.690342045177832,
        'num_receipt': '4BWeF',
        'date_receipt': '2025-11-15',
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
        if k in ['date_receipt']:
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

    resp_c = client.post('/api/v1/payments/', json=payment_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = ['id_annual_register']

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in payment_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/payments/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['payed'] == update_data['payed']
    assert updated['num_receipt'] == update_data['num_receipt']
    assert updated['date_receipt'] == update_data['date_receipt']


def test_get_payment_api(client, db):
    """Get Payment via API."""
    # Auth setup
    user_data = {
        'email': 'FtTeO@1os4y.com',
        'last_name': 'PSNSQ',
        'password': 'mNNUy',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='24MrP',
        slug='YWfG7',
        abbreviation='sIXLN',
        plugged='PJgtp',
        background='CQnuk',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='p2vk8',
        code='DNIMC',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='Box3o',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='utjKC',
        value='fHU9n',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='O9HfL',
        email='AcDZs@r0x0u.com',
        num_select='LaOEW',
        last_name='OlbU2',
        first_name='Dp0eq',
        date_of_birth='2025-11-15',
        place_of_birth='ufMh9',
        address='Vtr',
        sex='Féminin',
        martial_status='Divorcé(e)',
        phone_number='AYMr8',
        num_of_cin='zH9Eo',
        date_of_cin='2025-11-15',
        place_of_cin='xTSI9',
        repeat_status='1',
        picture='oM6gs',
        num_of_baccalaureate='vyr0N',
        center_of_baccalaureate='BOuxH',
        year_of_baccalaureate='2025-11-15',
        job='DTyhl',
        father_name='L8yYn',
        father_job='ccYj9',
        mother_name='dqbHN',
        mother_job='goPHC',
        parent_address='ioZmu09Zhu3LKm7At00WsVteHi70y19WL0QmHTNFhrtyCYMgLCmTqD1Ne5sjNbdLFvnP9J',
        level='M2',
        mean=4.169558875166653,
        enrollment_status='Inscrit(e)',
        imported_id='WsqCK',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=3.7273800907358825,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=9,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    payment_data = {
        'id_annual_register': annual_register.id,
        'payed': 5.4994656817158525,
        'num_receipt': 'yyNE4',
        'date_receipt': '2025-11-15',
    }

    client.post('/api/v1/payments/', json=payment_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/payments/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_payment_api(client, db):
    """Get_by_id Payment via API."""
    # Auth setup
    user_data = {
        'email': 'h5QzT@0gqrx.com',
        'last_name': 'gP7tb',
        'password': 'iZNNy',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='ZED7T',
        slug='bK46H',
        abbreviation='bwxK5',
        plugged='LYcSW',
        background='waexk',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='SdVSE',
        code='T60fr',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='LOhNN',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='lT9WD',
        value='PD3Xv',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='Uii1p',
        email='DrVtp@wvobi.com',
        num_select='hLJnL',
        last_name='OYu32',
        first_name='hgKpX',
        date_of_birth='2025-11-15',
        place_of_birth='S15PN',
        address='Si7WXfBxqtDW5RYfhEBxgwbnyRmBAwwu2yDWnyGpNu',
        sex='Masculin',
        martial_status='Veuf/Veuve',
        phone_number='HrPAn',
        num_of_cin='HrvQP',
        date_of_cin='2025-11-15',
        place_of_cin='GAVO2',
        repeat_status='0',
        picture='fnzlE',
        num_of_baccalaureate='Ni2NB',
        center_of_baccalaureate='a58lD',
        year_of_baccalaureate='2025-11-15',
        job='dFpP4',
        father_name='mfMfw',
        father_job='pyCWD',
        mother_name='Gn3p5',
        mother_job='cV5dI',
        parent_address='0mQ9DpOlKIGie5g7kFCOKub',
        level='L3',
        mean=5.249869630893402,
        enrollment_status='Inscrit(e)',
        imported_id='5MJs4',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='1',
        price=2.4740519034388146,
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

    payment_data = {
        'id_annual_register': annual_register.id,
        'payed': 5.279006029755937,
        'num_receipt': 'Uksyo',
        'date_receipt': '2025-11-15',
    }

    resp_c = client.post('/api/v1/payments/', json=payment_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/payments/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_payment_api(client, db):
    """Delete Payment via API."""
    # Auth setup
    user_data = {
        'email': 'YabRf@s1n8j.com',
        'last_name': 'rT6Xv',
        'password': 'qIFCr',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='aR9Fu',
        slug='kM4Ro',
        abbreviation='sIl3y',
        plugged='lnMWX',
        background='fhai4',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='9QXuP',
        code='RJQX9',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='UimFt',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='jxsfl',
        value='6Rq6z',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='njdpf',
        email='Pfnxx@efa1f.com',
        num_select='FTnOm',
        last_name='zcp0b',
        first_name='r545Z',
        date_of_birth='2025-11-15',
        place_of_birth='HN022',
        address='xkkWWv2TuZeU8BDFPVItwbJMHTAEcz2uMIX',
        sex='Féminin',
        martial_status='Célibataire',
        phone_number='s1USE',
        num_of_cin='rrWqE',
        date_of_cin='2025-11-15',
        place_of_cin='7yCis',
        repeat_status='2',
        picture='PieOt',
        num_of_baccalaureate='3c23w',
        center_of_baccalaureate='xICI3',
        year_of_baccalaureate='2025-11-15',
        job='3TLJs',
        father_name='h2P27',
        father_job='m16bq',
        mother_name='K2n0O',
        mother_job='pQ46J',
        parent_address='1LArwle4wmWXyuRDIY2WHpVhEFjDNIoaKCneaKw3LrNdZK3yXt8TrFTODPntXkfO3pMdYJWJZr3NmEPmPZhv1x7iAH5pgxeU',
        level='L2',
        mean=3.8456930345180456,
        enrollment_status='En attente',
        imported_id='Hj1as',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=5.195672260606386,
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

    payment_data = {
        'id_annual_register': annual_register.id,
        'payed': 4.745963441959802,
        'num_receipt': '5YWtV',
        'date_receipt': '2025-11-15',
    }

    resp_c = client.post('/api/v1/payments/', json=payment_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/payments/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'Payment deleted successfully'
    resp_chk = client.get(f'/api/v1/payments/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

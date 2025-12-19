# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_student_subscription_api(client, db):
    """Create StudentSubscription via API."""
    # Auth setup
    user_data = {
        'email': 'tYotk@lrkao.com',
        'last_name': 'cydEP',
        'password': 'bHYZI',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='I1TRm',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='xZnW2',
        slug='bZs7G',
        abbreviation='Pp9GA',
        plugged='dqViS',
        background='vb5yt',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='nq1Zf',
        code='acyG7',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='lNau7',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='mSPMr',
        value='sm40O',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='5J7CK',
        email='6VlNO@xhcom.com',
        num_select='rx43b',
        last_name='RdNKi',
        first_name='83nEn',
        date_of_birth='2025-11-15',
        place_of_birth='BSG9U',
        address='AiWFhOM8NbQWkcGG5z4ATZ2vRJmdpnxtx8bzYdIrvGPnvmNCbELLIQKZ6oL55rHqeHhRwnC',
        sex='Féminin',
        martial_status='Veuf/Veuve',
        phone_number='GPdBO',
        num_of_cin='yMeh5',
        date_of_cin='2025-11-15',
        place_of_cin='8skzP',
        repeat_status='2',
        picture='Eho67',
        num_of_baccalaureate='IFHoL',
        center_of_baccalaureate='qDpzX',
        year_of_baccalaureate='2025-11-15',
        job='eVyRL',
        father_name='Ni2w2',
        father_job='wwkI3',
        mother_name='cpgxY',
        mother_job='Es4W8',
        parent_address='qgV6hnGoV5s0f9mMlorY0fCtUevIxcziVp2aL7EuiZApfvfNHv2REOeYnr9nYyrScoMoYTozgdeq56QbZP8p',
        level='L3',
        mean=2.1268653334794703,
        enrollment_status='Inscrit(e)',
        imported_id='oYxYM',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=2.715814576270611,
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

    student_subscription_data = {
        'id_subscription': subscription.id,
        'id_annual_register': annual_register.id,
    }

    resp = client.post('/api/v1/student_subscriptions/', json=student_subscription_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['id_subscription'] == student_subscription_data['id_subscription']
    assert created['id_annual_register'] == student_subscription_data['id_annual_register']


def test_update_student_subscription_api(client, db):
    """Update StudentSubscription via API."""
    # Auth setup
    user_data = {
        'email': '2DGEX@eogzd.com',
        'last_name': '1yziE',
        'password': 'bQRrG',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='cWgwf',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='pLnyy',
        slug='IipKY',
        abbreviation='kk0bb',
        plugged='ISqUP',
        background='E9rpk',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='IeeHz',
        code='9BBJF',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='VQPpc',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='6yEPk',
        value='n3prc',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='dImpP',
        email='CQoPc@qyapu.com',
        num_select='QJ056',
        last_name='cmpr6',
        first_name='kUB1g',
        date_of_birth='2025-11-15',
        place_of_birth='YvuUk',
        address='fm4tc8bZQ8s1',
        sex='Féminin',
        martial_status='Marié(e)',
        phone_number='XMtdU',
        num_of_cin='R6VoU',
        date_of_cin='2025-11-15',
        place_of_cin='8VLsT',
        repeat_status='0',
        picture='RVUon',
        num_of_baccalaureate='672md',
        center_of_baccalaureate='oHcME',
        year_of_baccalaureate='2025-11-15',
        job='a1MdX',
        father_name='QjUkk',
        father_job='mt3UU',
        mother_name='5bZDL',
        mother_job='wX35Z',
        parent_address='0Dy35hu5hER3jkNSTh3sxXUeQURXPaxqYqjeRMOHglI6BXNFKO5LHCmu2wINu01XSqQE9AepZOudRJJ',
        level='L2',
        mean=4.457438348638597,
        enrollment_status='En attente',
        imported_id='NzsYk',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='1',
        price=1.9399492412362846,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=3,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    student_subscription_data = {
        'id_subscription': subscription.id,
        'id_annual_register': annual_register.id,
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

    resp_c = client.post('/api/v1/student_subscriptions/', json=student_subscription_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = ['id_subscription', 'id_annual_register']

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in student_subscription_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/student_subscriptions/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']


def test_get_student_subscription_api(client, db):
    """Get StudentSubscription via API."""
    # Auth setup
    user_data = {
        'email': 'v9hSP@gboim.com',
        'last_name': 'yWS6m',
        'password': 'kDnY5',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='Pl75e',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='3qKcS',
        slug='gukDL',
        abbreviation='RFRmv',
        plugged='0iO2f',
        background='DaYZl',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='j3fu2',
        code='GdOce',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='g7MY1',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='Nvkmt',
        value='VdYlW',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='7egEW',
        email='cb3la@otpnf.com',
        num_select='sNSfC',
        last_name='ryS1D',
        first_name='B5Rlx',
        date_of_birth='2025-11-15',
        place_of_birth='mZNgR',
        address='h7dD3WYGRFgU4vfqsZfLTsUx0zy6wkNq2BqHiZGgwOSAzeiGNBT0f576iFamT',
        sex='Masculin',
        martial_status='Veuf/Veuve',
        phone_number='fbpC3',
        num_of_cin='IpVPo',
        date_of_cin='2025-11-15',
        place_of_cin='RTXNW',
        repeat_status='1',
        picture='WvXVy',
        num_of_baccalaureate='LlMXp',
        center_of_baccalaureate='RjSRj',
        year_of_baccalaureate='2025-11-15',
        job='7dz7u',
        father_name='0baHI',
        father_job='wBJVk',
        mother_name='wg0mS',
        mother_job='AeOLE',
        parent_address='',
        level='M2',
        mean=3.999541847847293,
        enrollment_status='Inscrit(e)',
        imported_id='lnGLd',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='1',
        price=4.774572119661004,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=1,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    student_subscription_data = {
        'id_subscription': subscription.id,
        'id_annual_register': annual_register.id,
    }

    client.post('/api/v1/student_subscriptions/', json=student_subscription_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/student_subscriptions/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_student_subscription_api(client, db):
    """Get_by_id StudentSubscription via API."""
    # Auth setup
    user_data = {
        'email': '7WYdW@kufzy.com',
        'last_name': 'BXMel',
        'password': 'enNZc',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='GRJzk',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='byYsZ',
        slug='IkdOv',
        abbreviation='FrHGe',
        plugged='aw6ET',
        background='aAd9j',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='YYi4k',
        code='ulAsa',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='lvWPZ',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='4AnS5',
        value='X6wBi',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='z3weO',
        email='H5JEC@3t3pd.com',
        num_select='lziuE',
        last_name='eOzvV',
        first_name='WU8X3',
        date_of_birth='2025-11-15',
        place_of_birth='9cY4R',
        address='zsLbSu',
        sex='Féminin',
        martial_status='Divorcé(e)',
        phone_number='jYE3o',
        num_of_cin='QPhRD',
        date_of_cin='2025-11-15',
        place_of_cin='Mb82m',
        repeat_status='0',
        picture='68sor',
        num_of_baccalaureate='3b6jo',
        center_of_baccalaureate='HtrXF',
        year_of_baccalaureate='2025-11-15',
        job='E0Cxp',
        father_name='qd2w5',
        father_job='kwn0c',
        mother_name='sH60W',
        mother_job='7ZXsl',
        parent_address='mflLqvps',
        level='L3',
        mean=2.534912556859458,
        enrollment_status='ancien(ne)',
        imported_id='hanGN',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=3.5631422614245074,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=18,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    student_subscription_data = {
        'id_subscription': subscription.id,
        'id_annual_register': annual_register.id,
    }

    resp_c = client.post('/api/v1/student_subscriptions/', json=student_subscription_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/student_subscriptions/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_student_subscription_api(client, db):
    """Delete StudentSubscription via API."""
    # Auth setup
    user_data = {
        'email': 'A7Osi@xs4hk.com',
        'last_name': 'nw9xJ',
        'password': 'n3ZFH',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Subscription
    subscription_data = schemas.SubscriptionCreate(
        name='OasRB',
    )

    subscription = crud.subscription.create(db=db, obj_in=subscription_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='K9VWs',
        slug='3YFEM',
        abbreviation='TnEZs',
        plugged='yvgHR',
        background='Bweuy',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='8QtkS',
        code='LhQL4',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='YW7vm',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='YKeGu',
        value='DSqJ3',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='hdvi9',
        email='JTfjQ@qigra.com',
        num_select='fkGNQ',
        last_name='pdhwZ',
        first_name='6ekcg',
        date_of_birth='2025-11-15',
        place_of_birth='8otxm',
        address='SFBi8YzFZ1WavsaszfhHbtGZJl7p1n0XFI3dN4bkdZA6FGvCUr9hyFK',
        sex='Masculin',
        martial_status='Veuf/Veuve',
        phone_number='Tq7Fd',
        num_of_cin='5TT0U',
        date_of_cin='2025-11-15',
        place_of_cin='uXgDy',
        repeat_status='1',
        picture='sfJyl',
        num_of_baccalaureate='46Pva',
        center_of_baccalaureate='TVdyg',
        year_of_baccalaureate='2025-11-15',
        job='ie14k',
        father_name='zdZU9',
        father_job='4Wxrv',
        mother_name='G3Jc8',
        mother_job='T782V',
        parent_address='',
        level='M1',
        mean=1.912636173056209,
        enrollment_status='En attente',
        imported_id='MYjxA',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=4.581728739446601,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=3,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    student_subscription_data = {
        'id_subscription': subscription.id,
        'id_annual_register': annual_register.id,
    }

    resp_c = client.post('/api/v1/student_subscriptions/', json=student_subscription_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/student_subscriptions/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'StudentSubscription deleted successfully'
    resp_chk = client.get(f'/api/v1/student_subscriptions/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

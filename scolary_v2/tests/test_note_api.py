# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from datetime import datetime, timedelta, date, time
import random
from app.core import security


def test_create_note_api(client, db):
    """Create Note via API."""
    # Auth setup
    user_data = {
        'email': '5AAMM@maidv.com',
        'last_name': 'aCPql',
        'password': 'IZXBm',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='mlLu3',
        slug='vIIqJ',
        abbreviation='PTF8r',
        plugged='O5Gee',
        background='f5X0i',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='X81Nk',
        code='0FegV',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='euFz9',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='xJY45',
        value='4ohtv',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='jpnoB',
        email='6qtCt@pyigj.com',
        num_select='Khv37',
        last_name='erde7',
        first_name='rSOO7',
        date_of_birth='2025-11-15',
        place_of_birth='DgbLz',
        address='QVrRH6pt5tOifSBZJ1bxSkV9mVmboRI7tjrEnW8hkaULPJrvdmhduSMdBXOgNHXpXGowmF6kBTN0ZmagWGKQHIFVR1VT9',
        sex='Féminin',
        martial_status='Célibataire',
        phone_number='4PMZA',
        num_of_cin='pSN6o',
        date_of_cin='2025-11-15',
        place_of_cin='awqgF',
        repeat_status='0',
        picture='SCV1p',
        num_of_baccalaureate='tBRvN',
        center_of_baccalaureate='r7C6m',
        year_of_baccalaureate='2025-11-15',
        job='iFlmy',
        father_name='JrLNM',
        father_job='wfxEI',
        mother_name='p9dNR',
        mother_job='z5DGt',
        parent_address='',
        level='M2',
        mean=1.5489375095061066,
        enrollment_status='Inscrit(e)',
        imported_id='8Y3Qi',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=4.416638657408047,
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
        name='6MYVD',
        abbreviation='y5odJ',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='3exS7',
        repeat_status='2',
        id_journey=journey.id,
        imported_id='CNpEe',
        is_valid=False,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='r2FnR',
        semester='6ktmt',
        id_journey=journey.id,
        color='56KIv',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='LTMG9',
        semester='PthIb',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='E60t0',
        selection_regle='EBdYGoZmiPTDOpsSUVNOEkPrflktcY4GGBQv0mtxICg6Hc8QTqrn4h04Rm2vQmBeuI3QFEy0ZfL',
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
        selection_regle='ZAKWEbiV43CHuGwnW31u6J3Af3ZLtIdJywZk4LEfJErsZd35MBJkEDl6vb5e',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=4.899927520522986,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

    # Test data for User
    user_data = schemas.UserCreate(
        email='xgNO8@324cr.com',
        first_name='tVaDL',
        last_name='dIwxq',
        password='9cvWk',
        is_superuser=False,
        picture='iyPQF',
        is_active=False,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    note_data = {
        'id_register_semester': register_semester.id,
        'id_constituent_element_offering': constituent_element_offering.id,
        'session': 'Rattrapage',
        'note': 5.47792364747548,
        'id_user': user.id,
        'comment': 'WWTGXs4ykwni7XN7lXhzSjx',
    }

    resp = client.post('/api/v1/notes/', json=note_data, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    created = resp.json()
    assert created['id'] is not None
    assert created['id_register_semester'] == note_data['id_register_semester']
    assert created['id_constituent_element_offering'] == note_data['id_constituent_element_offering']
    assert created['session'] == note_data['session']
    assert created['note'] == note_data['note']
    assert created['id_user'] == note_data['id_user']
    assert created['comment'] == note_data['comment']


def test_update_note_api(client, db):
    """Update Note via API."""
    # Auth setup
    user_data = {
        'email': 'Z7UBh@buwzx.com',
        'last_name': 'YJuOT',
        'password': 'gOKfs',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='vwHwF',
        slug='H2m9S',
        abbreviation='BPTBK',
        plugged='WQWXj',
        background='wyHwk',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='0ZC6Z',
        code='0OcJd',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='wfGq9',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='pThj3',
        value='pWx25',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='2AGpy',
        email='NSXWK@z5zr8.com',
        num_select='ImO03',
        last_name='y6tXz',
        first_name='L7Dik',
        date_of_birth='2025-11-15',
        place_of_birth='oLXEk',
        address='tS7oHyX3HciKuauIRVirWXY3OCYIuyuRPpcKm5WvhJUWosMFmbZQ1DWnqRDxw8eUBtedcdWlQimoJfP',
        sex='Masculin',
        martial_status='Divorcé(e)',
        phone_number='iNEbi',
        num_of_cin='bvQTa',
        date_of_cin='2025-11-15',
        place_of_cin='fmtYC',
        repeat_status='1',
        picture='wnJAD',
        num_of_baccalaureate='t8rxs',
        center_of_baccalaureate='jiG4X',
        year_of_baccalaureate='2025-11-15',
        job='HxY28',
        father_name='SuV9N',
        father_job='t9Apr',
        mother_name='OkD63',
        mother_job='1M1IC',
        parent_address='IcoEMviIgqYZEsiAqpmMtNNR5I6BlVEaFmvM5GcNvIlpGcTa0zCVTTSqIW1e6z9b4H9wjoSwGg4ZmgkY7yuNbU',
        level='L2',
        mean=4.979636243572502,
        enrollment_status='Sélectionné(e)',
        imported_id='VGD6O',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=3.1729782948287717,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=0,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='sRoGE',
        abbreviation='LxDsU',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='idMRD',
        repeat_status='2',
        id_journey=journey.id,
        imported_id='fUNmU',
        is_valid=True,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='hzQYi',
        semester='Em9Lk',
        id_journey=journey.id,
        color='3EDmD',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='wVimv',
        semester='SmJ2V',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='Xgdue',
        selection_regle='ReHw2Cm',
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
        selection_regle='rLI58uHXWlQPXvERw',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=3.775905403484479,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

    # Test data for User
    user_data = schemas.UserCreate(
        email='Cfts6@xdwrf.com',
        first_name='jphfz',
        last_name='ZZIUM',
        password='jsLUA',
        is_superuser=True,
        picture='C42ZF',
        is_active=True,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    note_data = {
        'id_register_semester': register_semester.id,
        'id_constituent_element_offering': constituent_element_offering.id,
        'session': 'Rattrapage',
        'note': 1.6459764204691818,
        'id_user': user.id,
        'comment': 'pEGXgbpBRhzGh1QoTfAXrBn0oDIHUWbSdTsNKC6xDxoZfJd6uLZYqE5gHS6eb6wJ4wmMbaf2t32LtW77tkul0qscPdnA9',
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

    resp_c = client.post('/api/v1/notes/', json=note_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_c.status_code == status.HTTP_200_OK
    created = resp_c.json()
    fk_fields = ['id_register_semester', 'id_constituent_element_offering', 'id_user']

    # Build update_data for API
    update_data = {
        k: _updated_value(k, v)
        for k, v in note_data.items()
        if k not in ('id', 'hashed_password') and k not in fk_fields and not isinstance(v, dict)
    }

    resp_u = client.put(f'/api/v1/notes/{created["id"]}', json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert resp_u.status_code == status.HTTP_200_OK, resp_u.json()
    updated = resp_u.json()
    assert updated['id'] == created['id']
    assert updated['session'] == update_data['session']
    assert updated['note'] == update_data['note']
    assert updated['comment'] == update_data['comment']


def test_get_note_api(client, db):
    """Get Note via API."""
    # Auth setup
    user_data = {
        'email': 'T0Wra@o1hsi.com',
        'last_name': 'QlC8x',
        'password': '1qgBH',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='jHipk',
        slug='PBlQ9',
        abbreviation='Ci3U8',
        plugged='cgGoo',
        background='f5TUm',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='hlDNR',
        code='nkiLL',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='q9EsC',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='dCppf',
        value='EMkpU',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='VLZII',
        email='Eh6o7@48ipt.com',
        num_select='WnhpH',
        last_name='c3cKn',
        first_name='d8snV',
        date_of_birth='2025-11-15',
        place_of_birth='5VEic',
        address='ZB2rI52XteJVOzyEba9AzZAU615FqYAyrend78iCJgI2jAsUIm0CRqxVBXEvQYUHFc9Rzp4Ka',
        sex='Féminin',
        martial_status='Célibataire',
        phone_number='Dl7bh',
        num_of_cin='lKSHc',
        date_of_cin='2025-11-15',
        place_of_cin='JAvkX',
        repeat_status='0',
        picture='NL5Qy',
        num_of_baccalaureate='dllJs',
        center_of_baccalaureate='sul1x',
        year_of_baccalaureate='2025-11-15',
        job='ulJt9',
        father_name='1NkI0',
        father_job='kaRIT',
        mother_name='NPtlb',
        mother_job='stJSj',
        parent_address='PN9hyjohXXUBuyubaOqupYaypTeRNDsQunodeOPQ7RTcSGQeLSmaDarriRAJjhmJyBREH04CDpdGAB',
        level='M2',
        mean=3.2547474148674893,
        enrollment_status='Inscrit(e)',
        imported_id='hewPI',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=2.9117695449373437,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Test data for AnnualRegister
    annual_register_data = schemas.AnnualRegisterCreate(
        num_carte=student.num_carte,
        id_academic_year=academic_year.id,
        semester_count=16,
        id_enrollment_fee=enrollment_fee.id,
    )

    annual_register = crud.annual_register.create(db=db, obj_in=annual_register_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='luQIS',
        abbreviation='63eBR',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='lEzrr',
        repeat_status='0',
        id_journey=journey.id,
        imported_id='07pGY',
        is_valid=False,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='VgHQq',
        semester='cnHmb',
        id_journey=journey.id,
        color='DsLaO',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='xpJG4',
        semester='UM2t2',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='FgegJ',
        selection_regle='hRH1RnxN0fedtlyZnARWV4GrOO3kXRMsrbXL8ncQOgV6paFmrOwd27EI5u8qzb0X8FWhxpT7ef6E0t',
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
        selection_regle='eDtYA3sYtXcpT6',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=1.9343063520145245,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

    # Test data for User
    user_data = schemas.UserCreate(
        email='YHFIo@z9a08.com',
        first_name='bKRDT',
        last_name='7jh81',
        password='Mh2dh',
        is_superuser=False,
        picture='LOej9',
        is_active=False,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    note_data = {
        'id_register_semester': register_semester.id,
        'id_constituent_element_offering': constituent_element_offering.id,
        'session': 'Rattrapage',
        'note': 4.672522171600612,
        'id_user': user.id,
        'comment': 'U0YrActoI3f8SLS9dXnPTahL85GQNMLToZT1vKirodADDgytLM1jftlzfoF9kKlDTcOXEHL6F1lkGVNg4P1yZFN',
    }

    client.post('/api/v1/notes/', json=note_data, headers={"Authorization": f"Bearer {token}"})
    resp_g = client.get('/api/v1/notes/', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    items = resp_g.json()['data']
    assert any(item.get('id') for item in items)


def test_get_by_id_note_api(client, db):
    """Get_by_id Note via API."""
    # Auth setup
    user_data = {
        'email': 'uhtwi@rgycw.com',
        'last_name': 'TqdeM',
        'password': 'F8CPX',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='pcQ1B',
        slug='9VcQZ',
        abbreviation='uKXFa',
        plugged='SK6EC',
        background='SPh0e',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='urAjJ',
        code='gnJ5u',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='v72pq',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='neGUI',
        value='fu0HZ',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='zVOLb',
        email='CmLuH@cbfeu.com',
        num_select='lWW1t',
        last_name='oNnkN',
        first_name='8foZC',
        date_of_birth='2025-11-15',
        place_of_birth='RaQxK',
        address='XGfwL0hr',
        sex='Féminin',
        martial_status='Veuf/Veuve',
        phone_number='tGmpK',
        num_of_cin='MrVZz',
        date_of_cin='2025-11-15',
        place_of_cin='U26U1',
        repeat_status='1',
        picture='omNrC',
        num_of_baccalaureate='JOTdI',
        center_of_baccalaureate='5dfof',
        year_of_baccalaureate='2025-11-15',
        job='8hk6P',
        father_name='hZMib',
        father_job='vSJAI',
        mother_name='TrxaB',
        mother_job='VTE9v',
        parent_address='adgXI6Jw8O5WfyNUDk5E4axdjj1zM7GBnpBylNEkkhaP52n8oKbDrg7HiI6Gaq6lfPkjk1zcdxS074wGkOj6acA',
        level='L3',
        mean=3.823644084821256,
        enrollment_status='En attente',
        imported_id='7ws60',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=1.6696799038920522,
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
        name='WJRj2',
        abbreviation='5ZVCm',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='R1yMM',
        repeat_status='1',
        id_journey=journey.id,
        imported_id='UyrL3',
        is_valid=True,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='CmM95',
        semester='UElTw',
        id_journey=journey.id,
        color='LbwVF',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='7c3QL',
        semester='TvjLT',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='DkfnE',
        selection_regle='tpUoeybHlsCsnPd4BCMC5rNXosXBkEAW',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=17,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='8MckVuHWOdjobi9rcy49BWIe4t0QE8cY99wj4oiiMftxPwhfheS8kFJgrNMY8sT0EnYlXJ9ygYR5S0sURksjhMBGVCSJ',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=3.7249953946802155,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

    # Test data for User
    user_data = schemas.UserCreate(
        email='JzDFl@f1bix.com',
        first_name='aj6T3',
        last_name='xYqgD',
        password='VDqqP',
        is_superuser=True,
        picture='UwxQo',
        is_active=False,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    note_data = {
        'id_register_semester': register_semester.id,
        'id_constituent_element_offering': constituent_element_offering.id,
        'session': 'Normal',
        'note': 3.19283291214691,
        'id_user': user.id,
        'comment': 'pjznpK6lelTERpHenQWo5sIn2pXN52O68BIvvX35Rjo9obbLK20tSoo2kqPBUseJkitI',
    }

    resp_c = client.post('/api/v1/notes/', json=note_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_g = client.get(f'/api/v1/notes/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_g.status_code == status.HTTP_200_OK
    retrieved = resp_g.json()
    assert retrieved['id'] == created['id']


def test_delete_note_api(client, db):
    """Delete Note via API."""
    # Auth setup
    user_data = {
        'email': 'V8Aou@tynuh.com',
        'last_name': 'jnpqp',
        'password': 'N1x50',
        'is_superuser': False,
        'is_active': True,
    }
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(user.id), 'email': user.email})

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='2q1q9',
        slug='Rwzwh',
        abbreviation='wqoqy',
        plugged='suFDF',
        background='sN6eO',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='QMu2g',
        code='DQ5FI',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for Nationality
    nationality_data = schemas.NationalityCreate(
        name='rYcZ0',
    )

    nationality = crud.nationality.create(db=db, obj_in=nationality_data)

    # Test data for BaccalaureateSerie
    baccalaureate_serie_data = schemas.BaccalaureateSerieCreate(
        name='JeT2X',
        value='dplUq',
    )

    baccalaureate_serie = crud.baccalaureate_serie.create(db=db, obj_in=baccalaureate_serie_data)

    # Test data for Student
    student_data = schemas.StudentCreate(
        num_carte='WRKke',
        email='v46rC@qx7yd.com',
        num_select='bqFK0',
        last_name='vD3RJ',
        first_name='uY4HE',
        date_of_birth='2025-11-15',
        place_of_birth='cdf35',
        address='dO3P',
        sex='Masculin',
        martial_status='Veuf/Veuve',
        phone_number='gbSPf',
        num_of_cin='G468C',
        date_of_cin='2025-11-15',
        place_of_cin='Kfzsf',
        repeat_status='0',
        picture='1uhip',
        num_of_baccalaureate='0o3t4',
        center_of_baccalaureate='GNAxw',
        year_of_baccalaureate='2025-11-15',
        job='dsdNV',
        father_name='665K7',
        father_job='0Lfzc',
        mother_name='2OTZh',
        mother_job='acMe5',
        parent_address='ZXXKdtXJA7ZmbADb6KZQpYF6EWACCzXynXCTm43UsmwZcIuJ60vx6cilrPyzdhW',
        level='L3',
        mean=5.160246063587678,
        enrollment_status='Inscrit(e)',
        imported_id='Ux5zd',
        id_mention=mention.id,
        id_enter_year=academic_year.id,
        id_nationality=nationality.id,
        id_baccalaureate_series=baccalaureate_serie.id,
    )

    student = crud.student.create(db=db, obj_in=student_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=1.7534902589793586,
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

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='eSV94',
        abbreviation='NK6im',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for RegisterSemester
    register_semester_data = schemas.RegisterSemesterCreate(
        id_annual_register=annual_register.id,
        semester='qY4HY',
        repeat_status='2',
        id_journey=journey.id,
        imported_id='ikzNs',
        is_valid=True,
    )

    register_semester = crud.register_semester.create(db=db, obj_in=register_semester_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='WDuND',
        semester='9uuyO',
        id_journey=journey.id,
        color='Oc1nv',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='rDCBI',
        semester='ps1uz',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='Mxhz1',
        selection_regle='6VsCzK0bcNEwp7OFP1S4sqk71qvqpK01HWC58iZ4zZRZye59xfWKf4qHcdC21ES4kxVtB1Lvbe5tIYCP6OyIeea3zzarNslif',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=16,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='DEn0Th3fXGzLBPy4f8k6qmIgYbudIDOXTA6keNyr1BGTaAEvHB70561tk7OnbHbfMTdV',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=1.6906109695243319,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

    # Test data for User
    user_data = schemas.UserCreate(
        email='UFTCA@jcyxb.com',
        first_name='b98zL',
        last_name='UkEVf',
        password='6R5bb',
        is_superuser=True,
        picture='bPE6i',
        is_active=True,
    )

    user = crud.user.create(db=db, obj_in=user_data)

    note_data = {
        'id_register_semester': register_semester.id,
        'id_constituent_element_offering': constituent_element_offering.id,
        'session': 'Normal',
        'note': 4.799738319372654,
        'id_user': user.id,
        'comment': 'aNonTJQ23gN6z0uPvPZGEdwGZqmeAQXk0a8',
    }

    resp_c = client.post('/api/v1/notes/', json=note_data, headers={"Authorization": f"Bearer {token}"})
    created = resp_c.json()
    resp_d = client.delete(f'/api/v1/notes/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_d.status_code == status.HTTP_200_OK
    deleted = resp_d.json()
    assert deleted['msg'] == 'Note deleted successfully'
    resp_chk = client.get(f'/api/v1/notes/{created["id"]}', headers={"Authorization": f"Bearer {token}"})
    assert resp_chk.status_code == status.HTTP_404_NOT_FOUND

# begin #
# ---write your code here--- #
# end #

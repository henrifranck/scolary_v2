from datetime import date
import random

from fastapi import status

from app import crud, models, schemas
from app.core import security
from app.enum.enrollment_status import EnrollmentStatusEnum
from app.enum.marital_status import MaritalStatusEnum
from app.enum.sex import SexEnum


def test_dashboard_summary_counts(client, db):
    """Dashboard endpoint should return aggregate counts."""
    admin_data = {
        'email': f'dashboard_admin_{random.randint(1, 10000)}@example.com',
        'last_name': 'Admin',
        'password': 'Secret1',
        'is_superuser': True,
        'is_active': True,
    }
    admin = crud.user.create(db, obj_in=schemas.UserCreate(**admin_data))
    db.commit()
    token = security.create_access_token(sub={'id': str(admin.id), 'email': admin.email})

    mention = crud.mention.create(
        db=db,
        obj_in=schemas.MentionCreate(
            name=f'Mention {random.randint(1, 10000)}',
            slug=f'mention-{random.randint(1, 10000)}',
            abbreviation='MENT',
            plugged='Plug',
            background='bg',
        ),
    )

    crud.journey.create(
        db=db,
        obj_in=schemas.JourneyCreate(
            name=f'Journey {random.randint(1, 10000)}',
            abbreviation='JNY',
            id_mention=mention.id,
        ),
    )

    crud.student.create(
        db=db,
        obj_in=schemas.StudentCreate(
            num_carte=f'NC-{random.randint(1, 10000)}',
            last_name='Doe',
            date_of_birth=date(2000, 1, 1),
            place_of_birth='City',
            address='123 Street',
            sex=SexEnum.MALE,
            martial_status=MaritalStatusEnum.SINGLE,
            picture='pic.png',
            num_of_baccalaureate=f'BAC-{random.randint(1, 10000)}',
            center_of_baccalaureate='Center',
            job='Job',
            enrollment_status=EnrollmentStatusEnum.pending,
            id_mention=mention.id,
        ),
    )

    crud.user.create(
        db=db,
        obj_in=schemas.UserCreate(
            email=f'dashboard_user_{random.randint(1, 10000)}@example.com',
            last_name='Member',
            password='Secret1',
            is_superuser=False,
            is_active=True,
        ),
    )

    resp = client.get('/api/v1/dashboard/', headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == status.HTTP_200_OK, resp.text
    payload = resp.json()

    def _count(model):
        return db.query(model).filter(model.deleted_at.is_(None)).count()

    assert payload['total_students'] == _count(models.Student)
    assert payload['total_mentions'] == _count(models.Mention)
    assert payload['total_journeys'] == _count(models.Journey)
    assert payload['total_users'] == _count(models.User)

# begin #
# ---write your code here--- #
# end #

from fastapi import status
from app import crud, schemas
from sqlalchemy.orm import Session
from typing import Any, Dict
import pytest
from datetime import datetime, date, time, timedelta
import uuid
import random
"""Tests for CRUD operations on University model."""


def test_create_university(db: Session):
    """Test create operation for University."""
    # Test data for University
    university_data = schemas.UniversityCreate(
        province='55G2W',
        department_name='joVur',
        department_other_information='GKqzI',
        department_address='OjKWIp2HOJP',
        email='yl6en@rszfw.com',
        logo_university='zUELs',
        logo_departement='QGax1',
        phone_number='XN95Z',
        admin_signature='3r9E8',
    )

    university = crud.university.create(db=db, obj_in=university_data)

    # Assertions
    assert university.id is not None
    assert university.province == university_data.province
    assert university.department_name == university_data.department_name
    assert university.department_other_information == university_data.department_other_information
    assert university.department_address == university_data.department_address
    assert university.email == university_data.email
    assert university.logo_university == university_data.logo_university
    assert university.logo_departement == university_data.logo_departement
    assert university.phone_number == university_data.phone_number
    assert university.admin_signature == university_data.admin_signature


def test_update_university(db: Session):
    """Test update operation for University."""
    # Test data for University
    university_data = schemas.UniversityCreate(
        province='L6XRc',
        department_name='KIxln',
        department_other_information='8stfZ',
        department_address='BydLX3y7oFP08xZS33IMBnmpnfpD4FlgKyRh',
        email='FK03g@wu2pk.com',
        logo_university='GyoxZ',
        logo_departement='en548',
        phone_number='zO2YX',
        admin_signature='GCUvC',
    )

    university = crud.university.create(db=db, obj_in=university_data)

    # Precompute enum values for update
    enum_values_map = {}

    # Helper to compute a new value different from the current one
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
            current = v.value if hasattr(v, 'value') else v
            values = enum_values_map[k]
            try:
                idx = values.index(current)
                if len(values) > 1:
                    return values[(idx + 1) % len(values)]
                else:
                    return current
            except ValueError:
                # If current not in list, fallback to first value
                return values[0] if values else v

        # datetime +1 day
        if k in [] and isinstance(v, str):
            return (datetime.fromisoformat(v) + timedelta(days=1)).isoformat()
        if k in [] and isinstance(v, datetime):
            return v + timedelta(days=1)

        # date +1 day
        if k in [] and isinstance(v, str):
            return (date.fromisoformat(v) + timedelta(days=1)).isoformat()
        if k in [] and isinstance(v, date):
            return v + timedelta(days=1)

        # time +1 hour
        if k in [] and isinstance(v, str):
            return (datetime.strptime(v, '%H:%M:%S') + timedelta(hours=1)).time().strftime('%H:%M:%S')
        if k in [] and isinstance(v, time):
            return (datetime.combine(date.today(), v) + timedelta(hours=1)).time()

        # fallback -> prefix 'updated_'
        return f'updated_{v}'

    # Update data
    province_value = university.province
    department_name_value = university.department_name
    department_other_information_value = university.department_other_information
    department_address_value = university.department_address
    email_value = university.email
    logo_university_value = university.logo_university
    logo_departement_value = university.logo_departement
    phone_number_value = university.phone_number
    admin_signature_value = university.admin_signature
    update_data = schemas.UniversityUpdate(**{
        k: _updated_value(k, v)
        for k, v in university_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_university = crud.university.update(
        db=db, db_obj=university, obj_in=update_data
    )

    # Assertions
    assert updated_university.id == university.id
    assert updated_university.province != province_value
    assert updated_university.department_name != department_name_value
    assert updated_university.department_other_information != department_other_information_value
    assert updated_university.department_address != department_address_value
    assert updated_university.email != email_value
    assert updated_university.logo_university != logo_university_value
    assert updated_university.logo_departement != logo_departement_value
    assert updated_university.phone_number != phone_number_value
    assert updated_university.admin_signature != admin_signature_value


def test_get_university(db: Session):
    """Test get operation for University."""
    # Test data for University
    university_data = schemas.UniversityCreate(
        province='bsF6s',
        department_name='VvsVy',
        department_other_information='NpIZG',
        department_address='LC0MYLK81fgD',
        email='sE5YK@w3vwj.com',
        logo_university='e2Szv',
        logo_departement='y5F3J',
        phone_number='ogLlN',
        admin_signature='M42qi',
    )

    university = crud.university.create(db=db, obj_in=university_data)

    # Get all records
    records = crud.university.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == university.id for r in records)


def test_get_by_id_university(db: Session):
    """Test get_by_id operation for University."""
    # Test data for University
    university_data = schemas.UniversityCreate(
        province='I12Jw',
        department_name='SEKQS',
        department_other_information='tRcRw',
        department_address='mQybk7uvhYpiH6Dqgux3e6CHJ2nn9y5',
        email='GET02@ohh1y.com',
        logo_university='ZW0FE',
        logo_departement='YchL6',
        phone_number='o2gCL',
        admin_signature='8YAcS',
    )

    university = crud.university.create(db=db, obj_in=university_data)

    # Get by ID
    retrieved_university = crud.university.get(db=db, id=university.id)

    # Assertions
    assert retrieved_university is not None
    assert retrieved_university.id == university.id
    assert retrieved_university.province == university.province
    assert retrieved_university.department_name == university.department_name
    assert retrieved_university.department_other_information == university.department_other_information
    assert retrieved_university.department_address == university.department_address
    assert retrieved_university.email == university.email
    assert retrieved_university.logo_university == university.logo_university
    assert retrieved_university.logo_departement == university.logo_departement
    assert retrieved_university.phone_number == university.phone_number
    assert retrieved_university.admin_signature == university.admin_signature


def test_delete_university(db: Session):
    """Test delete operation for University."""
    # Test data for University
    university_data = schemas.UniversityCreate(
        province='vX7C5',
        department_name='C1RVS',
        department_other_information='E0zUu',
        department_address='emL',
        email='g5vrk@lhf5k.com',
        logo_university='MZdhy',
        logo_departement='hCnQa',
        phone_number='KlgME',
        admin_signature='Mpmf2',
    )

    university = crud.university.create(db=db, obj_in=university_data)

    # Delete record
    deleted_university = crud.university.remove(db=db, id=university.id)

    # Assertions
    assert deleted_university is not None
    assert deleted_university.id == university.id

    # Verify deletion
    assert crud.university.get(db=db, id=university.id) is None

# begin #
# ---write your code here--- #
# end #

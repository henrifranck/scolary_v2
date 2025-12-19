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
"""Tests for CRUD operations on EnrollmentFee model."""


def test_create_enrollment_fee(db: Session):
    """Test create operation for EnrollmentFee."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='Jy1vr',
        slug='L9p8O',
        abbreviation='NMm3F',
        plugged='38zD1',
        background='Gic3c',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='VxFs9',
        code='igcar',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=5.385392568586504,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Assertions
    assert enrollment_fee.id is not None
    assert enrollment_fee.level == enrollment_fee_data.level
    assert enrollment_fee.price == enrollment_fee_data.price
    assert enrollment_fee.id_mention == enrollment_fee_data.id_mention
    assert enrollment_fee.id_academic_year == enrollment_fee_data.id_academic_year


def test_update_enrollment_fee(db: Session):
    """Test update operation for EnrollmentFee."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='5G6Yi',
        slug='We9uK',
        abbreviation='YBZ2u',
        plugged='1glTj',
        background='61yjw',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='YufRx',
        code='yUwpo',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='1',
        price=3.370070486164595,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Precompute enum values for update
    enum_values_map = {}
    enum_values_map['level'] = ['0', '1', '2']

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
    level_value = enrollment_fee.level
    price_value = enrollment_fee.price
    update_data = schemas.EnrollmentFeeUpdate(**{
        k: _updated_value(k, v)
        for k, v in enrollment_fee_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_enrollment_fee = crud.enrollment_fee.update(
        db=db, db_obj=enrollment_fee, obj_in=update_data
    )

    # Assertions
    assert updated_enrollment_fee.id == enrollment_fee.id
    assert updated_enrollment_fee.level != level_value
    assert updated_enrollment_fee.price != price_value


def test_get_enrollment_fee(db: Session):
    """Test get operation for EnrollmentFee."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='YBwfd',
        slug='SaDZB',
        abbreviation='OVcRJ',
        plugged='bwYlJ',
        background='1Mjq3',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='ynOCs',
        code='1oPRw',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=4.324645495573559,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Get all records
    records = crud.enrollment_fee.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == enrollment_fee.id for r in records)


def test_get_by_id_enrollment_fee(db: Session):
    """Test get_by_id operation for EnrollmentFee."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='2uL79',
        slug='cWlBy',
        abbreviation='oDsFv',
        plugged='kz9U9',
        background='4h3Zt',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='MDwfD',
        code='GZIiF',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='2',
        price=5.029332990806535,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Get by ID
    retrieved_enrollment_fee = crud.enrollment_fee.get(db=db, id=enrollment_fee.id)

    # Assertions
    assert retrieved_enrollment_fee is not None
    assert retrieved_enrollment_fee.id == enrollment_fee.id
    assert retrieved_enrollment_fee.level == enrollment_fee.level
    assert retrieved_enrollment_fee.price == enrollment_fee.price
    assert retrieved_enrollment_fee.id_mention == enrollment_fee.id_mention
    assert retrieved_enrollment_fee.id_academic_year == enrollment_fee.id_academic_year


def test_delete_enrollment_fee(db: Session):
    """Test delete operation for EnrollmentFee."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='vWlb3',
        slug='tBnWj',
        abbreviation='ZI53g',
        plugged='gXkLt',
        background='j1fro',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='eWnJS',
        code='zyXig',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for EnrollmentFee
    enrollment_fee_data = schemas.EnrollmentFeeCreate(
        level='0',
        price=5.295133526115653,
        id_mention=mention.id,
        id_academic_year=academic_year.id,
    )

    enrollment_fee = crud.enrollment_fee.create(db=db, obj_in=enrollment_fee_data)

    # Delete record
    deleted_enrollment_fee = crud.enrollment_fee.remove(db=db, id=enrollment_fee.id)

    # Assertions
    assert deleted_enrollment_fee is not None
    assert deleted_enrollment_fee.id == enrollment_fee.id

    # Verify deletion
    assert crud.enrollment_fee.get(db=db, id=enrollment_fee.id) is None

# begin #
# ---write your code here--- #
# end #

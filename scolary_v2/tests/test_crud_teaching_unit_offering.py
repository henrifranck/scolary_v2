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
"""Tests for CRUD operations on TeachingUnitOffering model."""


def test_create_teaching_unit_offering(db: Session):
    """Test create operation for TeachingUnitOffering."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='9ArZq',
        slug='EPLrJ',
        abbreviation='3IhYv',
        plugged='TNTU7',
        background='BY3sw',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='M8bMu',
        abbreviation='dr6GV',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='Saic8',
        semester='FFCka',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='vUB9h',
        code='OJ80C',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='QDBKO',
        selection_regle='PwZdQmgwFDmwN9tTXEgYBi7RpFFldyMz8Tj1U1KLGqoGSsqAIB0',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=6,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Assertions
    assert teaching_unit_offering.id is not None
    assert teaching_unit_offering.id_teaching_unit == teaching_unit_offering_data.id_teaching_unit
    assert teaching_unit_offering.credit == teaching_unit_offering_data.credit
    assert teaching_unit_offering.id_academic_year == teaching_unit_offering_data.id_academic_year
    assert teaching_unit_offering.id_teaching_unit_goup == teaching_unit_offering_data.id_teaching_unit_goup


def test_update_teaching_unit_offering(db: Session):
    """Test update operation for TeachingUnitOffering."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='notSg',
        slug='i8Re6',
        abbreviation='4MJMy',
        plugged='nkbxU',
        background='XcAQM',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='1cBnR',
        abbreviation='jTbqS',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='28GOn',
        semester='CjL8m',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='G8iMS',
        code='MGAo1',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='iv94S',
        selection_regle='vF1fcGf1EMdV0s',
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
    credit_value = teaching_unit_offering.credit
    update_data = schemas.TeachingUnitOfferingUpdate(**{
        k: _updated_value(k, v)
        for k, v in teaching_unit_offering_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_teaching_unit_offering = crud.teaching_unit_offering.update(
        db=db, db_obj=teaching_unit_offering, obj_in=update_data
    )

    # Assertions
    assert updated_teaching_unit_offering.id == teaching_unit_offering.id
    assert updated_teaching_unit_offering.credit != credit_value


def test_get_teaching_unit_offering(db: Session):
    """Test get operation for TeachingUnitOffering."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='YEndr',
        slug='FU7dm',
        abbreviation='2L7FR',
        plugged='wToL8',
        background='jOD6e',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='YxaeL',
        abbreviation='m1dwH',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='2cgRF',
        semester='22kWf',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='iDrl0',
        code='kmA3p',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='yShHD',
        selection_regle='mX4XYzGcJr40YpTsByh4CoK2Rwu2GfJG0hUkpUEQ6AheIxffe9l2GRVdIFeKG42PevjICUre5',
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

    # Get all records
    records = crud.teaching_unit_offering.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == teaching_unit_offering.id for r in records)


def test_get_by_id_teaching_unit_offering(db: Session):
    """Test get_by_id operation for TeachingUnitOffering."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='l1mZx',
        slug='Ae35H',
        abbreviation='quDVL',
        plugged='fEHfB',
        background='z5wub',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='nAu9u',
        abbreviation='yVRfO',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='LZO5c',
        semester='ynxgQ',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='4t8bY',
        code='8Z3fL',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='71Z9I',
        selection_regle='iEh340gTDl2jcPYuhFVSWganG2PlHRnvzNRxvbRUd3M1ANQGOq7yn1dNsnOQV0GusMXVP5DgamRsE',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=3,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Get by ID
    retrieved_teaching_unit_offering = crud.teaching_unit_offering.get(db=db, id=teaching_unit_offering.id)

    # Assertions
    assert retrieved_teaching_unit_offering is not None
    assert retrieved_teaching_unit_offering.id == teaching_unit_offering.id
    assert retrieved_teaching_unit_offering.id_teaching_unit == teaching_unit_offering.id_teaching_unit
    assert retrieved_teaching_unit_offering.credit == teaching_unit_offering.credit
    assert retrieved_teaching_unit_offering.id_academic_year == teaching_unit_offering.id_academic_year
    assert retrieved_teaching_unit_offering.id_teaching_unit_goup == teaching_unit_offering.id_teaching_unit_goup


def test_delete_teaching_unit_offering(db: Session):
    """Test delete operation for TeachingUnitOffering."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='aSKmB',
        slug='7Ybbf',
        abbreviation='Lj5EW',
        plugged='ci76P',
        background='RU6GY',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='CdT49',
        abbreviation='dQrNf',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='VMhan',
        semester='wgscg',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='RylFZ',
        code='UsRyB',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='RgiBr',
        selection_regle='jLVxiyeovvMCzmJ6iMMC5IOipocIkpsIR7e6QF4vMM23YZTdkzSxMZ',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=7,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Delete record
    deleted_teaching_unit_offering = crud.teaching_unit_offering.remove(db=db, id=teaching_unit_offering.id)

    # Assertions
    assert deleted_teaching_unit_offering is not None
    assert deleted_teaching_unit_offering.id == teaching_unit_offering.id

    # Verify deletion
    assert crud.teaching_unit_offering.get(db=db, id=teaching_unit_offering.id) is None

# begin #
# ---write your code here--- #
# end #

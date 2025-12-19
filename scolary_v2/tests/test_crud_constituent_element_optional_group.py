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
"""Tests for CRUD operations on ConstituentElementOptionalGroup model."""


def test_create_constituent_element_optional_group(db: Session):
    """Test create operation for ConstituentElementOptionalGroup."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='kbHVe',
        slug='1l8cg',
        abbreviation='8qFg7',
        plugged='31Bzg',
        background='dNQDy',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='uHnwj',
        abbreviation='YLCP6',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='XxxQa',
        semester='HMwv1',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='aBVfx',
        code='LufKN',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='S3SqN',
        selection_regle='dUvIPjdN8DPBMllziH7AH0hpsvzoza1nRZTvcdbfblJdz1yqUIbivv5tIXziaaYJx9UUzp4Ql',
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
        selection_regle='SU1I3zSIWfkqbkaGDueOCdsogLPQUaDbZkuN',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Assertions
    assert constituent_element_optional_group.id is not None
    assert constituent_element_optional_group.id_teaching_unit_offering == constituent_element_optional_group_data.id_teaching_unit_offering
    assert constituent_element_optional_group.selection_regle == constituent_element_optional_group_data.selection_regle


def test_update_constituent_element_optional_group(db: Session):
    """Test update operation for ConstituentElementOptionalGroup."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='vslmn',
        slug='LrThM',
        abbreviation='myxMS',
        plugged='w2HQ5',
        background='BMzWp',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='5r7my',
        abbreviation='yRBfa',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='SvoHr',
        semester='yXPjG',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='wCljQ',
        code='ScQbm',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='TdXNG',
        selection_regle='nO2rh8ZxsF8O1ix6lEGkjvfW4BojhLHe6nYkgIjJFwzmhb1o2px4D2oIOfj2gUriUsoSiFv3XsGU4YyUIV',
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
        selection_regle='5bMYuOjlqbTIdx3jPwQslL1d1Se4Lg73lYvO63eSf5fRTM0SfSElcLE7ig',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

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
    selection_regle_value = constituent_element_optional_group.selection_regle
    update_data = schemas.ConstituentElementOptionalGroupUpdate(**{
        k: _updated_value(k, v)
        for k, v in constituent_element_optional_group_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_constituent_element_optional_group = crud.constituent_element_optional_group.update(
        db=db, db_obj=constituent_element_optional_group, obj_in=update_data
    )

    # Assertions
    assert updated_constituent_element_optional_group.id == constituent_element_optional_group.id
    assert updated_constituent_element_optional_group.selection_regle != selection_regle_value


def test_get_constituent_element_optional_group(db: Session):
    """Test get operation for ConstituentElementOptionalGroup."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='atU1L',
        slug='O8kHw',
        abbreviation='t4NPh',
        plugged='cpTFT',
        background='GLtGi',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='2g2Jg',
        abbreviation='L3Q5Y',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='KGbDd',
        semester='SITI6',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='1EeU6',
        code='ZkI5a',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='FwFbi',
        selection_regle='u9eqaJeoms0RZXecSdvhJXIHUg7up9xbPWWwcu4qcCGq7DRXITqgPO9WkgY2JExD9b3xPRzRhT3tZbmUreyYVuOxxmcdkscSMt',
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

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='JH7wQCAMnyFlEQXKoX1CPS5TJ7W3SHbcXrrJEoJf32IWXcTfeTeXWakySWTFcD5Kl62Jkjv0QeVvA1fOF',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Get all records
    records = crud.constituent_element_optional_group.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == constituent_element_optional_group.id for r in records)


def test_get_by_id_constituent_element_optional_group(db: Session):
    """Test get_by_id operation for ConstituentElementOptionalGroup."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='zvMeo',
        slug='mle9i',
        abbreviation='dsy2v',
        plugged='zOamx',
        background='xBHkv',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='e5lV2',
        abbreviation='taUci',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='CNpYb',
        semester='aZaxm',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='sfA6T',
        code='RiWu1',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='KNEsu',
        selection_regle='k1hm6xxW1m5vV5R3n0jBGLDi5pa2JlEeo26ys4SzT5qz3m',
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
        selection_regle='UDgu5GbjjkxgUsFP5OhYRSJTVDikRCTSIvz4R5C80MlW4DopLsW8181wGaMN45iN3ifvMIN3',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Get by ID
    retrieved_constituent_element_optional_group = crud.constituent_element_optional_group.get(db=db, id=constituent_element_optional_group.id)

    # Assertions
    assert retrieved_constituent_element_optional_group is not None
    assert retrieved_constituent_element_optional_group.id == constituent_element_optional_group.id
    assert retrieved_constituent_element_optional_group.id_teaching_unit_offering == constituent_element_optional_group.id_teaching_unit_offering
    assert retrieved_constituent_element_optional_group.selection_regle == constituent_element_optional_group.selection_regle


def test_delete_constituent_element_optional_group(db: Session):
    """Test delete operation for ConstituentElementOptionalGroup."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='RHxSW',
        slug='FXKsR',
        abbreviation='e3KJw',
        plugged='j7vyK',
        background='mPkkV',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='GHIgX',
        abbreviation='6mCHS',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='DaYtf',
        semester='lGKdv',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='vzank',
        code='BjpVY',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='8ULoY',
        selection_regle='kYG19OHAgIxm',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=2,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='h14gjjlDU8ljzLpYr',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Delete record
    deleted_constituent_element_optional_group = crud.constituent_element_optional_group.remove(db=db, id=constituent_element_optional_group.id)

    # Assertions
    assert deleted_constituent_element_optional_group is not None
    assert deleted_constituent_element_optional_group.id == constituent_element_optional_group.id

    # Verify deletion
    assert crud.constituent_element_optional_group.get(db=db, id=constituent_element_optional_group.id) is None

# begin #
# ---write your code here--- #
# end #

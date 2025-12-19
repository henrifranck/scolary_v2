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
"""Tests for CRUD operations on ConstituentElementOffering model."""


def test_create_constituent_element_offering(db: Session):
    """Test create operation for ConstituentElementOffering."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='3zwUd',
        slug='smaze',
        abbreviation='UUB72',
        plugged='p2m3g',
        background='KMOQC',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='VP8mQ',
        abbreviation='SIQll',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='hmN3A',
        semester='LAKBS',
        id_journey=journey.id,
        color='Jkbs4',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='PkNwB',
        code='S44tu',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='AjGhc',
        semester='XZvft',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='7eRSY',
        selection_regle='yGzTiXinbUwtOtRhdgDS3sruH5vjLiMIP3N1ksfuLAZ8avnlNUvkRKgOTytItiVPjuv',
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
        selection_regle='3DDeO7t75UdepVzRSN2OMWgYDU5a6GgA5j9ZHER5vyT5R7vwCd3gk17J13olz27UEbEhK803m8YeCGKpN7DzDQGE',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=3.0992127775981824,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

    # Assertions
    assert constituent_element_offering.id is not None
    assert constituent_element_offering.id_constituent_element == constituent_element_offering_data.id_constituent_element
    assert constituent_element_offering.weight == constituent_element_offering_data.weight
    assert constituent_element_offering.id_academic_year == constituent_element_offering_data.id_academic_year
    assert constituent_element_offering.id_constituent_element_optional_group == constituent_element_offering_data.id_constituent_element_optional_group
    assert constituent_element_offering.id_teching_unit_offering == constituent_element_offering_data.id_teching_unit_offering


def test_update_constituent_element_offering(db: Session):
    """Test update operation for ConstituentElementOffering."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='oFxXD',
        slug='TL0Kg',
        abbreviation='ko1BS',
        plugged='MaJy1',
        background='5dGxx',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='3YnwQ',
        abbreviation='OIWWj',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='R8Lbo',
        semester='EQC8X',
        id_journey=journey.id,
        color='bHqhl',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='Zv6xo',
        code='tKCe2',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='Mta7X',
        semester='oZCtp',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='k13Zt',
        selection_regle='Tx34PAl965zUcZ1BsCiyWqb3iiVnFiWvT7vL0UN0so8brmdRKlxpjD0DQ3q',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=8,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='VSH8dC8EoafWQOXNp0IXimCLLm1w6ymJezU7EcbSnx32UtIzexjMRp3ETuITR0d5EgN5olNPYCoHCslfLxmJS0mjg2UJ8KRigv',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=3.6543233095649628,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

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
    weight_value = constituent_element_offering.weight
    update_data = schemas.ConstituentElementOfferingUpdate(**{
        k: _updated_value(k, v)
        for k, v in constituent_element_offering_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_constituent_element_offering = crud.constituent_element_offering.update(
        db=db, db_obj=constituent_element_offering, obj_in=update_data
    )

    # Assertions
    assert updated_constituent_element_offering.id == constituent_element_offering.id
    assert updated_constituent_element_offering.weight != weight_value


def test_get_constituent_element_offering(db: Session):
    """Test get operation for ConstituentElementOffering."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='jzTqN',
        slug='WKy1U',
        abbreviation='OyPKT',
        plugged='p2FZ4',
        background='ETzBX',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='berAo',
        abbreviation='DfmhE',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='H3zMY',
        semester='7Ztvy',
        id_journey=journey.id,
        color='nE2tl',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='uORjH',
        code='61DZ7',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='DjDWq',
        semester='rAYIu',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='omdiS',
        selection_regle='0slnuw7DHMvb38Y04rmYY23mcvpPcIO',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=18,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='nNlyJFGxlXHEBcGSETJzCb6ZOjiIBSMnlZyWfNve',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=4.418783116571351,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

    # Get all records
    records = crud.constituent_element_offering.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == constituent_element_offering.id for r in records)


def test_get_by_id_constituent_element_offering(db: Session):
    """Test get_by_id operation for ConstituentElementOffering."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='sg5oc',
        slug='JeLqh',
        abbreviation='SruuD',
        plugged='OahBe',
        background='7alGt',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='TKCYy',
        abbreviation='RHqh4',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='3rTz3',
        semester='rkHSJ',
        id_journey=journey.id,
        color='iNDqd',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='29ILH',
        code='wQsLd',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='Y5piF',
        semester='TVvu2',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='Haasg',
        selection_regle='aEXzKNxTI9OHzGQwAGu6ZZ7DodKVsSbxOqYFbtPgXsEs2',
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
        selection_regle='vDqBy3lzGQ95S8Uxz371Si7y4YJAE0TTc98onzWsenbAuhw8Jtg5nYkWMcAxcFux971do90oLXLQ0QErYchNVu8Jf9i1POVv',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=2.6339097863557708,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

    # Get by ID
    retrieved_constituent_element_offering = crud.constituent_element_offering.get(db=db, id=constituent_element_offering.id)

    # Assertions
    assert retrieved_constituent_element_offering is not None
    assert retrieved_constituent_element_offering.id == constituent_element_offering.id
    assert retrieved_constituent_element_offering.id_constituent_element == constituent_element_offering.id_constituent_element
    assert retrieved_constituent_element_offering.weight == constituent_element_offering.weight
    assert retrieved_constituent_element_offering.id_academic_year == constituent_element_offering.id_academic_year
    assert retrieved_constituent_element_offering.id_constituent_element_optional_group == constituent_element_offering.id_constituent_element_optional_group
    assert retrieved_constituent_element_offering.id_teching_unit_offering == constituent_element_offering.id_teching_unit_offering


def test_delete_constituent_element_offering(db: Session):
    """Test delete operation for ConstituentElementOffering."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='cPCIs',
        slug='AKtat',
        abbreviation='jqHeY',
        plugged='sRihy',
        background='kGw18',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='mRiqE',
        abbreviation='UH7Om',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for ConstituentElement
    constituent_element_data = schemas.ConstituentElementCreate(
        name='GvX4T',
        semester='O76x5',
        id_journey=journey.id,
        color='pyUES',
    )

    constituent_element = crud.constituent_element.create(db=db, obj_in=constituent_element_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='uSu87',
        code='QS3Xw',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for TeachingUnit
    teaching_unit_data = schemas.TeachingUnitCreate(
        name='xBnpm',
        semester='rOHps',
        id_journey=journey.id,
    )

    teaching_unit = crud.teaching_unit.create(db=db, obj_in=teaching_unit_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='mafP7',
        selection_regle='5N7vOOaxKbNMAfyqSxlvio288jZWI5UoAl2xBUk1SapV9RYEufI5QR8h4WYnfbZNbJjBU9184RJBxg1P8z2OE',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Test data for TeachingUnitOffering
    teaching_unit_offering_data = schemas.TeachingUnitOfferingCreate(
        id_teaching_unit=teaching_unit.id,
        credit=14,
        id_academic_year=academic_year.id,
        id_teaching_unit_goup=teaching_unit_optional_group.id,
    )

    teaching_unit_offering = crud.teaching_unit_offering.create(db=db, obj_in=teaching_unit_offering_data)

    # Test data for ConstituentElementOptionalGroup
    constituent_element_optional_group_data = schemas.ConstituentElementOptionalGroupCreate(
        id_teaching_unit_offering=teaching_unit_offering.id,
        selection_regle='5dEPDcOmQ8j8TnCifDs8iRUsoTIj',
    )

    constituent_element_optional_group = crud.constituent_element_optional_group.create(db=db, obj_in=constituent_element_optional_group_data)

    # Test data for ConstituentElementOffering
    constituent_element_offering_data = schemas.ConstituentElementOfferingCreate(
        id_constituent_element=constituent_element.id,
        weight=3.932013209650039,
        id_academic_year=academic_year.id,
        id_constituent_element_optional_group=constituent_element_optional_group.id,
        id_teching_unit_offering=teaching_unit_offering.id,
    )

    constituent_element_offering = crud.constituent_element_offering.create(db=db, obj_in=constituent_element_offering_data)

    # Delete record
    deleted_constituent_element_offering = crud.constituent_element_offering.remove(db=db, id=constituent_element_offering.id)

    # Assertions
    assert deleted_constituent_element_offering is not None
    assert deleted_constituent_element_offering.id == constituent_element_offering.id

    # Verify deletion
    assert crud.constituent_element_offering.get(db=db, id=constituent_element_offering.id) is None

# begin #
# ---write your code here--- #
# end #

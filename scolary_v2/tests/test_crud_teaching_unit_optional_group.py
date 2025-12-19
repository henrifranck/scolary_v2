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
"""Tests for CRUD operations on TeachingUnitOptionalGroup model."""


def test_create_teaching_unit_optional_group(db: Session):
    """Test create operation for TeachingUnitOptionalGroup."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='1HvnI',
        slug='qLtVb',
        abbreviation='LhSg4',
        plugged='ejMUK',
        background='D0G7h',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='1JPxy',
        abbreviation='Q8J6J',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='IuupW',
        selection_regle='cmYySbij2z1ReITDXE9tjc',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Assertions
    assert teaching_unit_optional_group.id is not None
    assert teaching_unit_optional_group.id_journey == teaching_unit_optional_group_data.id_journey
    assert teaching_unit_optional_group.semester == teaching_unit_optional_group_data.semester
    assert teaching_unit_optional_group.selection_regle == teaching_unit_optional_group_data.selection_regle


def test_update_teaching_unit_optional_group(db: Session):
    """Test update operation for TeachingUnitOptionalGroup."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='RG8oL',
        slug='4yeq6',
        abbreviation='f98wQ',
        plugged='C6ogV',
        background='QppZ6',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='BewvA',
        abbreviation='4DUMX',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='q0jLA',
        selection_regle='6z8VP',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

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
    semester_value = teaching_unit_optional_group.semester
    selection_regle_value = teaching_unit_optional_group.selection_regle
    update_data = schemas.TeachingUnitOptionalGroupUpdate(**{
        k: _updated_value(k, v)
        for k, v in teaching_unit_optional_group_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_teaching_unit_optional_group = crud.teaching_unit_optional_group.update(
        db=db, db_obj=teaching_unit_optional_group, obj_in=update_data
    )

    # Assertions
    assert updated_teaching_unit_optional_group.id == teaching_unit_optional_group.id
    assert updated_teaching_unit_optional_group.semester != semester_value
    assert updated_teaching_unit_optional_group.selection_regle != selection_regle_value


def test_get_teaching_unit_optional_group(db: Session):
    """Test get operation for TeachingUnitOptionalGroup."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='T4acY',
        slug='XMoZk',
        abbreviation='dl8ai',
        plugged='GFYTK',
        background='mHwe2',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='Z5C4n',
        abbreviation='tm1BQ',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='tM8bM',
        selection_regle='vIADl8M1qYDsXQbOcvZRNEvKbcmD7KS4hkkzOlWrolLOGhYHyLHI7ibeJCcfwJC69wNt7Sqd244AX597Wuln',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Get all records
    records = crud.teaching_unit_optional_group.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == teaching_unit_optional_group.id for r in records)


def test_get_by_id_teaching_unit_optional_group(db: Session):
    """Test get_by_id operation for TeachingUnitOptionalGroup."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='n4wZY',
        slug='8FjLS',
        abbreviation='wMrv4',
        plugged='GTmwI',
        background='DjpIx',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='3a63E',
        abbreviation='MV5IK',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='QIRqB',
        selection_regle='AFTcSj',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Get by ID
    retrieved_teaching_unit_optional_group = crud.teaching_unit_optional_group.get(db=db, id=teaching_unit_optional_group.id)

    # Assertions
    assert retrieved_teaching_unit_optional_group is not None
    assert retrieved_teaching_unit_optional_group.id == teaching_unit_optional_group.id
    assert retrieved_teaching_unit_optional_group.id_journey == teaching_unit_optional_group.id_journey
    assert retrieved_teaching_unit_optional_group.semester == teaching_unit_optional_group.semester
    assert retrieved_teaching_unit_optional_group.selection_regle == teaching_unit_optional_group.selection_regle


def test_delete_teaching_unit_optional_group(db: Session):
    """Test delete operation for TeachingUnitOptionalGroup."""
    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='73m8F',
        slug='zBzxa',
        abbreviation='16t3B',
        plugged='Yhysl',
        background='TxNFh',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='ScUWE',
        abbreviation='7xRIk',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for TeachingUnitOptionalGroup
    teaching_unit_optional_group_data = schemas.TeachingUnitOptionalGroupCreate(
        id_journey=journey.id,
        semester='Z0O2w',
        selection_regle='DF1eMeSdpzHY00whZBICIkLglJF9KnLXnlq4WnLJK50taKh2fD',
    )

    teaching_unit_optional_group = crud.teaching_unit_optional_group.create(db=db, obj_in=teaching_unit_optional_group_data)

    # Delete record
    deleted_teaching_unit_optional_group = crud.teaching_unit_optional_group.remove(db=db, id=teaching_unit_optional_group.id)

    # Assertions
    assert deleted_teaching_unit_optional_group is not None
    assert deleted_teaching_unit_optional_group.id == teaching_unit_optional_group.id

    # Verify deletion
    assert crud.teaching_unit_optional_group.get(db=db, id=teaching_unit_optional_group.id) is None

# begin #
# ---write your code here--- #
# end #

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
"""Tests for CRUD operations on ExamGroup model."""


def test_create_exam_group(db: Session):
    """Test create operation for ExamGroup."""
    # Test data for Classroom
    classroom_data = schemas.ClassroomCreate(
        name='DwXk0',
        capacity=17,
    )

    classroom = crud.classroom.create(db=db, obj_in=classroom_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='HW6e5',
        slug='wJpHJ',
        abbreviation='vexSl',
        plugged='a5AJ8',
        background='o2UaR',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='CQJzT',
        abbreviation='Icqxy',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='vbNcT',
        code='a0GZv',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for ExamGroup
    exam_group_data = schemas.ExamGroupCreate(
        id_classroom=classroom.id,
        id_journey=journey.id,
        semester='mC87t',
        num_from=4,
        num_to=12,
        session='Normal',
        id_accademic_year=academic_year.id,
    )

    exam_group = crud.exam_group.create(db=db, obj_in=exam_group_data)

    # Assertions
    assert exam_group.id is not None
    assert exam_group.id_classroom == exam_group_data.id_classroom
    assert exam_group.id_journey == exam_group_data.id_journey
    assert exam_group.semester == exam_group_data.semester
    assert exam_group.num_from == exam_group_data.num_from
    assert exam_group.num_to == exam_group_data.num_to
    assert exam_group.session == exam_group_data.session
    assert exam_group.id_accademic_year == exam_group_data.id_accademic_year


def test_update_exam_group(db: Session):
    """Test update operation for ExamGroup."""
    # Test data for Classroom
    classroom_data = schemas.ClassroomCreate(
        name='882e9',
        capacity=5,
    )

    classroom = crud.classroom.create(db=db, obj_in=classroom_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='zjZgU',
        slug='PjNwr',
        abbreviation='JKe2c',
        plugged='SMYzs',
        background='Hg6qH',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='NLVUd',
        abbreviation='84XuB',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='2Iv6s',
        code='OafbA',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for ExamGroup
    exam_group_data = schemas.ExamGroupCreate(
        id_classroom=classroom.id,
        id_journey=journey.id,
        semester='mnsf3',
        num_from=14,
        num_to=19,
        session='Rattrapage',
        id_accademic_year=academic_year.id,
    )

    exam_group = crud.exam_group.create(db=db, obj_in=exam_group_data)

    # Precompute enum values for update
    enum_values_map = {}
    enum_values_map['session'] = ['Normal', 'Rattrapage']

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
    semester_value = exam_group.semester
    num_from_value = exam_group.num_from
    num_to_value = exam_group.num_to
    session_value = exam_group.session
    update_data = schemas.ExamGroupUpdate(**{
        k: _updated_value(k, v)
        for k, v in exam_group_data.dict().items()
        if k not in ('id', 'hashed_password') and not isinstance(v, dict)
    })
    updated_exam_group = crud.exam_group.update(
        db=db, db_obj=exam_group, obj_in=update_data
    )

    # Assertions
    assert updated_exam_group.id == exam_group.id
    assert updated_exam_group.semester != semester_value
    assert updated_exam_group.num_from != num_from_value
    assert updated_exam_group.num_to != num_to_value
    assert updated_exam_group.session != session_value


def test_get_exam_group(db: Session):
    """Test get operation for ExamGroup."""
    # Test data for Classroom
    classroom_data = schemas.ClassroomCreate(
        name='DBpDn',
        capacity=0,
    )

    classroom = crud.classroom.create(db=db, obj_in=classroom_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='uF6tr',
        slug='5Jlli',
        abbreviation='6poPa',
        plugged='1Or6E',
        background='kApFj',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='ndn7L',
        abbreviation='5mSfM',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='ntMrl',
        code='pCyW6',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for ExamGroup
    exam_group_data = schemas.ExamGroupCreate(
        id_classroom=classroom.id,
        id_journey=journey.id,
        semester='6s2Gn',
        num_from=0,
        num_to=18,
        session='Rattrapage',
        id_accademic_year=academic_year.id,
    )

    exam_group = crud.exam_group.create(db=db, obj_in=exam_group_data)

    # Get all records
    records = crud.exam_group.get_multi_where_array(db=db)

    # Assertions
    assert len(records) > 0
    assert any(r.id == exam_group.id for r in records)


def test_get_by_id_exam_group(db: Session):
    """Test get_by_id operation for ExamGroup."""
    # Test data for Classroom
    classroom_data = schemas.ClassroomCreate(
        name='ZwAQH',
        capacity=20,
    )

    classroom = crud.classroom.create(db=db, obj_in=classroom_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='coZYo',
        slug='vNUzL',
        abbreviation='CsScd',
        plugged='aUVDo',
        background='SZ5Uo',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='vx0w8',
        abbreviation='NJ9dH',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='Weao6',
        code='l7n04',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for ExamGroup
    exam_group_data = schemas.ExamGroupCreate(
        id_classroom=classroom.id,
        id_journey=journey.id,
        semester='pGjEM',
        num_from=17,
        num_to=20,
        session='Normal',
        id_accademic_year=academic_year.id,
    )

    exam_group = crud.exam_group.create(db=db, obj_in=exam_group_data)

    # Get by ID
    retrieved_exam_group = crud.exam_group.get(db=db, id=exam_group.id)

    # Assertions
    assert retrieved_exam_group is not None
    assert retrieved_exam_group.id == exam_group.id
    assert retrieved_exam_group.id_classroom == exam_group.id_classroom
    assert retrieved_exam_group.id_journey == exam_group.id_journey
    assert retrieved_exam_group.semester == exam_group.semester
    assert retrieved_exam_group.num_from == exam_group.num_from
    assert retrieved_exam_group.num_to == exam_group.num_to
    assert retrieved_exam_group.session == exam_group.session
    assert retrieved_exam_group.id_accademic_year == exam_group.id_accademic_year


def test_delete_exam_group(db: Session):
    """Test delete operation for ExamGroup."""
    # Test data for Classroom
    classroom_data = schemas.ClassroomCreate(
        name='9ATmo',
        capacity=4,
    )

    classroom = crud.classroom.create(db=db, obj_in=classroom_data)

    # Test data for Mention
    mention_data = schemas.MentionCreate(
        name='IgDmq',
        slug='JtHxe',
        abbreviation='A8n4v',
        plugged='TtjIc',
        background='GvfiD',
    )

    mention = crud.mention.create(db=db, obj_in=mention_data)

    # Test data for Journey
    journey_data = schemas.JourneyCreate(
        name='1lOO9',
        abbreviation='Ct0Xy',
        id_mention=mention.id,
    )

    journey = crud.journey.create(db=db, obj_in=journey_data)

    # Test data for AcademicYear
    academic_year_data = schemas.AcademicYearCreate(
        name='nz1DQ',
        code='4OUx8',
    )

    academic_year = crud.academic_year.create(db=db, obj_in=academic_year_data)

    # Test data for ExamGroup
    exam_group_data = schemas.ExamGroupCreate(
        id_classroom=classroom.id,
        id_journey=journey.id,
        semester='kzH5t',
        num_from=0,
        num_to=7,
        session='Normal',
        id_accademic_year=academic_year.id,
    )

    exam_group = crud.exam_group.create(db=db, obj_in=exam_group_data)

    # Delete record
    deleted_exam_group = crud.exam_group.remove(db=db, id=exam_group.id)

    # Assertions
    assert deleted_exam_group is not None
    assert deleted_exam_group.id == exam_group.id

    # Verify deletion
    assert crud.exam_group.get(db=db, id=exam_group.id) is None

# begin #
# ---write your code here--- #
# end #

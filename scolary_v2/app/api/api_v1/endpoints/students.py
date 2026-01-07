from typing import Any
from pathlib import Path
from datetime import datetime
import shutil

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
import ast
from datetime import date
import re

from app.enum.register_type import RegisterTypeEnum
from app.utils import get_level_from_number
from app.core.notifications import schedule_notification

router = APIRouter()
from app.api import deps

UPLOAD_DIR = Path("files") / "pictures"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/jpg"}


def generate_num_select(db: Session, id_mention: int) -> str:
    """
    Generate selection number: <AB>-<YYYY><NNN>
    - AB: first two letters of mention abbreviation/name (uppercased)
    - YYYY: current year
    - NNN: zero-padded counter per mention/year
    Example for Mathématiques in 2026: MA-2026001
    """
    mention = crud.mention.get(db=db, id=id_mention)
    mention_label = mention.abbreviation or mention.name if mention else "XX"
    prefix_letters = (
        (mention_label or "XX")[:2].upper().ljust(2, "X")
    )
    current_year = date.today().year
    base_prefix = f"{prefix_letters}-{current_year}"

    latest = (
        db.query(models.Student.num_select)
        .filter(models.Student.num_select.like(f"{base_prefix}%"))
        .order_by(models.Student.num_select.desc())
        .first()
    )

    if latest and latest[0]:
        match = re.search(rf"{re.escape(base_prefix)}(\d+)$", latest[0])
        last_num = int(match.group(1)) if match else 0
    else:
        last_num = 0

    next_num = last_num + 1
    return f"{base_prefix}{next_num:03d}"


@router.get('/', response_model=schemas.ResponseStudent)
def read_students(
        *,
        offset: int = 0,
        limit: int = 20,
        relation: str = "[]",
        where_relation: str = "[]",
        base_column: str = "[]",
        where: str = "[]",
        include_deleted: bool = False,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve students.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
        relations += ast.literal_eval(relation)

    wheres_relations = []
    if where_relation is not None and where_relation != "" and where_relation != []:
        wheres_relations += ast.literal_eval(where_relation)

    base_columns = []
    if base_column is not None and base_column != "" and base_column != []:
        base_columns += ast.literal_eval(base_column)

    wheres = []
    if where is not None and where != "" and where != []:
        wheres += ast.literal_eval(where)

    students = crud.student.get_multi_where_array(
        db=db,
        relations=relations,
        skip=offset,
        limit=limit,
        where=wheres,
        base_columns=base_columns,
        where_relation=wheres_relations,
        include_deleted=include_deleted
    )
    count = crud.student.get_count_where_array(
        db=db,
        where=wheres,
        include_deleted=include_deleted
    )
    response = schemas.ResponseStudent(**{'count': count, 'data': jsonable_encoder(students)})
    return response


@router.get('/one_student', response_model=schemas.StudentWithRelation)
def read_one_student(
        *,
        relation: str = "[]",
        where: str = "[]",
        where_relation: str = "[]",
        where_custom: str = "[]",
        base_column: str = "[]",
        route_ui: str = "re-registration",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve students.
    """
    relations = []
    if relation is not None and relation != "" and relation != []:
        relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
        wheres += ast.literal_eval(where)

    wheres_relations = []
    if where_relation is not None and where_relation != "" and where_relation != []:
        wheres_relations += ast.literal_eval(where_relation)

    base_columns = []
    if base_column is not None and base_column != "" and base_column != []:
        base_columns += ast.literal_eval(base_column)

    student = crud.student.get_first_where_array(
        db=db, relations=relations, where=wheres, base_columns=base_columns, where_relation=wheres_relations)
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')

    max_semester = 0
    # Compute document completion status for the given route_ui
    try:
        service = crud.available_service.get_by_field(
            db=db, field="route_ui", value=route_ui
        )
        if service:
            required_ids = [
                link.id_required_document
                for link in (service.available_service_required_document or [])
                if link.id_required_document
            ]
            required_ids = [rid for rid in required_ids if rid is not None]

            if required_ids:
                annual_ids_subquery = (
                    db.query(models.AnnualRegister.id)
                    .filter(
                        models.AnnualRegister.num_carte == student.num_carte,
                        models.AnnualRegister.register_type == RegisterTypeEnum.REGISTRATION
                    )
                    .subquery()
                )
                uploaded_required_ids = {
                    doc.id_required_document
                    for doc in db.query(models.Document).filter(
                        models.Document.id_annual_register.in_(annual_ids_subquery)
                    )
                    if doc.id_required_document is not None
                }
                missing_ids = [
                    rid for rid in required_ids if rid not in uploaded_required_ids
                ]
                status = (
                    "none"
                    if not uploaded_required_ids
                    else "complete"
                    if not missing_ids
                    else "missing"
                )
                document_status = {
                    "status": status,
                    "missing_required_document_ids": missing_ids,
                    "required_document_ids": required_ids,
                }
            else:
                document_status = {
                    "status": "not_applicable",
                    "missing_required_document_ids": [],
                    "required_document_ids": [],
                }
        else:
            document_status = {
                "status": "not_applicable",
                "missing_required_document_ids": [],
                "required_document_ids": [],
            }

    except Exception:
        # We deliberately swallow errors here to avoid breaking the endpoint
        document_status = None

    wheres_customs = []
    if where_custom is not None and where_custom != "" and where_custom != []:
        wheres_customs += ast.literal_eval(where_custom)

    annual_register = crud.annual_register.get_first_where_array(db=db, where=wheres_customs)
    if annual_register:
        max_semester_value = crud.register_semester.get_max_semester(db=db, id_annual_register=annual_register.id)
        if max_semester_value != (None,):
            max_semester = int(dict(max_semester_value)["S"])

    data = jsonable_encoder(student)
    if document_status is not None:
        data["document_status"] = document_status
        data["generated_level"] = get_level_from_number(max_semester)

    return data


@router.post('/', response_model=schemas.Student)
def create_student(
        *,
        db: Session = Depends(deps.get_db),
        student_in: schemas.StudentNewCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new student.
    """
    data = student_in.model_dump()
    data.pop("new_registration", None)
    if not data.get("num_select"):
        data["num_select"] = generate_num_select(db, data.get("id_mention"))

    student = crud.student.create(db=db, obj_in=schemas.StudentNewCreate(**data))
    try:
        schedule_notification(
            {
                "type": "student_created",
                "student_id": student.id,
                "full_name": f"{student.last_name} {student.first_name}".strip(),
                "mention_id": student.id_mention,
                "journey_id": data.get("id_journey") or None,
                "target_roles": ["admin"],
            }
        )
    except Exception:
        pass
    return student


@router.put('/{student_id}', response_model=schemas.Student)
def update_student(
        *,
        db: Session = Depends(deps.get_db),
        student_id: int,
        student_in: schemas.StudentUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an student.
    """
    student = crud.student.get(db=db, id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')
    data = student_in.model_dump(exclude_none=True)
    new_registration = data.pop("new_registration", False)

    if new_registration and not student.num_carte:
        mention_id = data.get("id_mention") or getattr(student, "id_mention", None)
        prefix = "F"
        if mention_id:
            where = [
                {
                    "key":"id",
                    "operator":"==",
                    "value":mention_id
                }
            ]
            mention = crud.mention.get_first_where_array(db=db, where=where, relations=["plugged{name}"])
            plugged = mention.plugged
            if plugged and plugged.name:
                prefix = plugged.name[0].upper()
            else:
                raise HTTPException(status_code=404, detail='Branch not found')
        latest = (
            db.query(models.Student.num_carte)
            .filter(models.Student.num_carte.like(f"{prefix}%"))
            .order_by(models.Student.num_carte.desc())
            .first()
        )
        next_num = 1
        if latest and latest[0]:
            match = re.match(rf"^{re.escape(prefix)}(\d+)$", latest[0])
            if match:
                next_num = int(match.group(1)) + 1
        data["num_carte"] = f"{prefix}{next_num:06d}"

    student = crud.student.update(db=db, db_obj=student, obj_in=data)
    return student


@router.get('/{student_id}', response_model=schemas.Student)
def read_student(
        *,
        relation: str = "[]",
        where: str = "[]",
        db: Session = Depends(deps.get_db),
        student_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get student by ID.
    """
    relations = []
    if relation is not None and relation != "" and relation != [] and relation != "[]":
        relations += ast.literal_eval(relation)

    wheres = []
    if where is not None and where != "" and where != []:
        wheres += ast.literal_eval(where)

    student = crud.student.get(db=db, id=student_id, relations=relations, where=wheres)
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')
    return student


@router.post('/{student_id}/picture', response_model=schemas.Student)
async def upload_student_picture(
        *,
        db: Session = Depends(deps.get_db),
        student_id: int,
        file: UploadFile = File(...),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Upload and attach a profile picture to a student.
    """
    student = crud.student.get(db=db, id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail='Unsupported file type')

    extension = Path(file.filename).suffix.lower()
    if extension not in {'.png', '.jpg', '.jpeg'}:
        extension = '.png' if file.content_type == 'image/png' else '.jpg'

    filename = f"{student.num_carte}{extension}"
    relative_url = f"/files/pictures/{filename}"
    if student.picture:
        old_path = Path(student.picture.lstrip("/"))
        if old_path.as_posix() != relative_url.lstrip("/") and old_path.parts[:2] == ("files", "pictures"):
            try:
                (Path(".") / old_path).unlink(missing_ok=True)
            except TypeError:
                if (Path(".") / old_path).exists():
                    (Path(".") / old_path).unlink()

    file_path = UPLOAD_DIR / filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    updated_student = crud.student.update(
        db=db,
        db_obj=student,
        obj_in={'picture': relative_url},
    )
    return updated_student


@router.delete('/{student_id}', response_model=schemas.Msg)
def delete_student(
        *,
        db: Session = Depends(deps.get_db),
        student_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an student.
    """
    student = crud.student.get(db=db, id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')
    student = crud.student.remove(db=db, id=student_id)
    return schemas.Msg(msg='Student deleted successfully')


@router.post('/{student_id}/soft_delete', response_model=schemas.Student)
def soft_delete_student(
        *,
        db: Session = Depends(deps.get_db),
        student_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Soft delete a student by setting deleted_at.
    """
    student = crud.student.get(db=db, id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')
    student = crud.student.update(
        db=db,
        db_obj=student,
        obj_in={'deleted_at': datetime.utcnow()},
    )
    return student


@router.post('/{student_id}/restore', response_model=schemas.Student)
def restore_student(
        *,
        db: Session = Depends(deps.get_db),
        student_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Restore a soft-deleted student.
    """
    student = crud.student.get(db=db, id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')
    student = crud.student.update(
        db=db,
        db_obj=student,
        obj_in={'deleted_at': None},
    )
    return student


@router.delete('/{student_id}/hard_delete', response_model=schemas.Msg)
def hard_delete_student(
        *,
        db: Session = Depends(deps.get_db),
        student_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Permanently delete a student and related records.
    """
    student = crud.student.get(db=db, id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')

    annual_registers = crud.annual_register.get_multi_where_array(
        db=db,
        where=[
            [
                {"key": "num_carte", "operator": "==", "value": student.num_carte},
                {"key": "num_carte", "operator": "==", "value": student.num_select}
            ]
        ],
        limit=10
    )
    annual_ids = [annual.id for annual in annual_registers if annual.id]
    if annual_ids:
        register_semesters = crud.register_semester.get_multi_where_array(
            db=db,
            where=[{"key": "id_annual_register", "operator": "in", "value": annual_ids}],
            limit=1000
        )
        register_ids = [semester.id for semester in register_semesters if semester.id]
        if register_ids:
            db.query(models.Note).filter(
                models.Note.id_register_semester.in_(register_ids)
            ).delete(synchronize_session=False)
            db.query(models.ResultTeachingUnit).filter(
                models.ResultTeachingUnit.id_register_semester.in_(register_ids)
            ).delete(synchronize_session=False)
            db.query(models.RegisterSemester).filter(
                models.RegisterSemester.id.in_(register_ids)
            ).delete(synchronize_session=False)

        documents = db.query(models.Document).filter(
            models.Document.id_annual_register.in_(annual_ids)
        ).all()
        for document in documents:
            document_path = Path(document.url.lstrip("/"))
            if document_path.parts[:2] == ("files", "documents"):
                try:
                    (Path(".") / document_path).unlink(missing_ok=True)
                except TypeError:
                    if (Path(".") / document_path).exists():
                        (Path(".") / document_path).unlink()

        if documents:
            db.query(models.Document).filter(
                models.Document.id_annual_register.in_(annual_ids)
            ).delete(synchronize_session=False)

        db.query(models.Payment).filter(
            models.Payment.id_annual_register.in_(annual_ids)
        ).delete(synchronize_session=False)
        db.query(models.StudentSubscription).filter(
            models.StudentSubscription.id_annual_register.in_(annual_ids)
        ).delete(synchronize_session=False)
        db.query(models.AnnualRegister).filter(
            models.AnnualRegister.id.in_(annual_ids)
        ).delete(synchronize_session=False)

    if student.picture:
        picture_path = Path(student.picture.lstrip("/"))
        if picture_path.parts[:2] == ("files", "pictures"):
            try:
                (Path(".") / picture_path).unlink(missing_ok=True)
            except TypeError:
                if (Path(".") / picture_path).exists():
                    (Path(".") / picture_path).unlink()

    db.commit()
    crud.student.remove(db=db, id=student_id)
    return schemas.Msg(msg='Student deleted successfully')

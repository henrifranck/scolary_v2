from typing import Any, Optional, Dict, List
from pathlib import Path
from datetime import datetime
import shutil

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app import crud, models, schemas
from app.utils import generateOnlyValue
from app.utils_sco.list.list_by_year import create_list_registered_by_year
from app.utils_sco.heads_card import parcourir_et as generate_head_cards
from app.utils_sco.tails_card import parcourir_et as generate_tail_cards
import ast

router = APIRouter()
from app.api import deps
UPLOAD_DIR = Path("files") / "pictures"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/jpg"}

PDF_LIST_DIR = Path("files") / "pdf" / "list"
PDF_CARD_DIR = Path("files") / "pdf" / "carte"
PDF_LIST_DIR.mkdir(parents=True, exist_ok=True)
PDF_CARD_DIR.mkdir(parents=True, exist_ok=True)


def _parse_semester(semester: Optional[str]) -> int:
    if not semester:
        return 0
    digits = "".join(char for char in str(semester) if char.isdigit())
    return int(digits) if digits.isdigit() else 0


def _build_pdf_response(result: dict) -> schemas.PdfFileResponse:
    path = str(result.get("path", "")).lstrip("/")
    filename = str(result.get("filename", ""))
    if path and not path.endswith("/"):
        path = f"{path}/"
    url = f"/files/{path}{filename}" if filename else ""
    return schemas.PdfFileResponse(path=f"{path}", filename=filename, url=url)


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
        base_column: str = "[]",
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

    return jsonable_encoder(student)


@router.post('/', response_model=schemas.Student)
def create_student(
        *,
        db: Session = Depends(deps.get_db),
        student_in: schemas.StudentCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new student.
    """
    student = crud.student.create(db=db, obj_in=student_in)
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
    student = crud.student.update(db=db, db_obj=student, obj_in=student_in)
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
        where=[{"key": "num_carte", "operator": "==", "value": student.num_carte}],
        limit=1000
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

        db.query(models.Payement).filter(
            models.Payement.id_annual_register.in_(annual_ids)
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


@router.get('/print-list', response_model=schemas.PdfFileResponse)
def print_students_list(
        *,
        id_year: int = Query(..., description="Academic year id"),
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    academic_year = crud.academic_year.get(db=db, id=id_year)
    if not academic_year:
        raise HTTPException(status_code=404, detail="Academic year not found")

    annual_registers = db.query(models.AnnualRegister).filter(
        models.AnnualRegister.id_academic_year == id_year
    ).all()

    student_map: Dict[str, Dict[str, str]] = {}
    for annual in annual_registers:
        student = annual.student
        if not student or not student.num_carte:
            continue

        max_semester_value = 0
        for register_semester in annual.register_semester or []:
            max_semester_value = max(
                max_semester_value,
                _parse_semester(register_semester.semester)
            )

        if max_semester_value <= 0:
            continue

        level_label = f"S{max_semester_value}"
        full_name = f"{student.last_name or ''} {student.first_name or ''}".strip()
        existing = student_map.get(student.num_carte)
        if not existing or _parse_semester(existing.get("level")) < max_semester_value:
            student_map[student.num_carte] = {
                "num_carte": student.num_carte,
                "full_name": full_name,
                "level": level_label
            }

    students = sorted(
        student_map.values(),
        key=lambda item: (item.get("full_name") or "", item.get("num_carte") or "")
    )
    if not students:
        raise HTTPException(status_code=404, detail="No students found for this year")

    result = create_list_registered_by_year(academic_year.name or str(id_year), students)
    return _build_pdf_response(result)


@router.get('/print-cards', response_model=schemas.PdfFileResponse)
def print_student_cards(
        *,
        id_mention: int = Query(..., description="Mention id"),
        id_year: Optional[int] = Query(None, description="Academic year id"),
        side: str = Query("heads", description="heads or tails"),
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    mention = crud.mention.get(db=db, id=id_mention)
    if not mention:
        raise HTTPException(status_code=404, detail="Mention not found")

    academic_year = None
    if id_year is not None:
        academic_year = crud.academic_year.get(db=db, id=id_year)
        if not academic_year:
            raise HTTPException(status_code=404, detail="Academic year not found")

    students = db.query(models.Student).filter(
        models.Student.id_mention == id_mention,
        models.Student.deleted_at.is_(None)
    ).all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found for this mention")

    student_rows: List[Dict[str, Any]] = []
    for student in students:
        annual_query = db.query(models.AnnualRegister).filter(
            models.AnnualRegister.num_carte == student.num_carte
        )
        if id_year is not None:
            annual_query = annual_query.filter(
                models.AnnualRegister.id_academic_year == id_year
            )
        annual_registers = annual_query.all()

        best_semester_value = 0
        best_register = None
        for annual in annual_registers:
            for register_semester in annual.register_semester or []:
                semester_value = _parse_semester(register_semester.semester)
                if semester_value >= best_semester_value:
                    best_semester_value = semester_value
                    best_register = register_semester

        level_label = f"S{best_semester_value}" if best_semester_value > 0 else ""
        journey = best_register.journey if best_register else None

        student_rows.append({
            "num_carte": student.num_carte,
            "last_name": student.last_name,
            "first_name": student.first_name,
            "date_birth": student.date_of_birth,
            "place_birth": student.place_of_birth,
            "num_cin": student.num_of_cin,
            "date_cin": student.date_of_cin,
            "place_cin": student.place_of_cin,
            "photo": student.picture or "",
            "title": journey.name if journey else "",
            "abbreviation": journey.abbreviation if journey else "",
            "level": level_label
        })

    university = db.query(models.University).first()
    data = {
        "mention": mention.name or f"Mention {mention.id}",
        "img_carte": mention.background or "",
        "year": academic_year.name if academic_year else "",
        "level": "",
        "supperadmin": getattr(university, "admin_signature", "") if university else "",
        "key": generateOnlyValue()
    }

    side_normalized = side.strip().lower()
    if side_normalized == "heads":
        result = generate_head_cards(student_rows, data, university)
    elif side_normalized == "tails":
        result = generate_tail_cards(student_rows, data)
    else:
        raise HTTPException(status_code=400, detail="Invalid card side")

    return _build_pdf_response(result)

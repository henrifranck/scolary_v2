from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.utils import generateOnlyValue
from app.utils_sco.heads_card import parcourir_et as generate_head_cards
from app.utils_sco.list.list_by_year import create_list_registered_by_year
from app.utils_sco.tails_card import parcourir_et as generate_tail_cards

router = APIRouter()

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


@router.get('/students/list', response_model=schemas.PdfFileResponse)
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


@router.get('/students/cards', response_model=schemas.PdfFileResponse)
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

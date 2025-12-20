import ast
from pathlib import Path
from typing import Any, List, Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.utils import get_level, get_semester
from app.utils_sco import tails_card, heads_card, badge_tails_user, badge_head_user
from app.utils_sco.special import special_heads_card, special_tails_card

router = APIRouter()


def _build_pdf_response(result: Union[dict, str]) -> schemas.PdfFileResponse:
    if isinstance(result, dict):
        path = str(result.get("path", "")).lstrip("/")
        filename = str(result.get("filename", ""))
    else:
        pdf_path = Path(str(result)).as_posix().lstrip("/")
        filename = Path(pdf_path).name
        remainder = Path(pdf_path)
        if remainder.parts and remainder.parts[0] == "files":
            path = Path(*remainder.parts[1:-1]).as_posix()
        else:
            path = Path(*remainder.parts[:-1]).as_posix()

    if path and not path.endswith("/"):
        path = f"{path}/"
    url = f"/files/{path}{filename}" if filename else ""
    return schemas.PdfFileResponse(path=path, filename=filename, url=url)


@router.get("/carte_student/", response_model=List[schemas.PdfFileResponse])
def create_carte_student(
        id_year: str,
        id_mention: str,
        level: str = "M2",
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> List[schemas.PdfFileResponse]:
    """
    create carte
    """
    mention = crud.mention.get(db=db, id=id_mention)
    if not mention:
        raise HTTPException(
            status_code=400,
            detail=f" Mention not found.",
        )

    year = crud.academic_year.get(db=db, id=id_year)
    if not year:
        raise HTTPException(
            status_code=400,
            detail=f"College years not found.",
        )

    data = get_semester(level)
    semester = data[0]
    semester2 = data[1]

    students = crud.student.get_for_carte(
        db=db,
        id_mention=mention.id,
        id_year=id_year,
        semester=semester,
        semester2=semester2,
    )
    data = {"supperadmin": "", "year": year.name}
    user = crud.user.get_card_signer(db=db)
    university = crud.university.get_info(db=db)
    if user:
        data["supperadmin"] = f"{user.last_name} {user.first_name}"
    data["mention"] = mention.name

    data["key"] = year.id, mention.id
    data["level"] = level
    data["img_carte"] = mention.background
    heads = heads_card.parcourir_et(students, data, university)
    tails = tails_card.parcourir_et(students, data)

    return [_build_pdf_response(heads), _build_pdf_response(tails)]


@router.get("/badge_user/", response_model=List[schemas.PdfFileResponse])
def create_badge_user(
        db: Session = Depends(deps.get_db),
        id_user: int = None,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    create carte
    """
    wheres = [
        {
            "key": "is_active",
            "operator": "==",
            "value": True
        }
    ]
    university = crud.university_info.get_university(db=db)
    all_user = []
    if id_user:
        user = crud.user.get(db=db, id=id_user, relations=["role"])
        if user:
            all_user = [user]
    else:
        all_user = crud.user.get_multi(db=db, limit=2000, skip=0, relations=["role"], order_by="id", order="DESC",
                                       where=wheres)
    all_user = jsonable_encoder(all_user)
    tails_badge = badge_tails_user.print_badge(all_user, university)
    head_badge = badge_head_user.print_badge(all_user, university)
    return [_build_pdf_response(head_badge), _build_pdf_response(tails_badge)]


@router.post("/special", response_model=List[schemas.PdfFileResponse])
def create_special_carte(
        *,
        relation: str = "[]",
        db: Session = Depends(deps.get_db),
        where: str = "[]",
        accademic_year_id: int = 2,
        where_relation: str = "[]",
        base_column: str = "[]",
        current_user: models.User = Depends(deps.get_current_active_user),
) -> List[schemas.PdfFileResponse]:
    """
    create carte
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
        where=wheres,
        base_columns=base_columns,
        where_relation=wheres_relations,
    )

    print(students)
    year = crud.academic_year.get(db=db, id=accademic_year_id)
    if not year:
        raise HTTPException(
            status_code=400,
            detail=f"College years not found.",
        )
    data = {"supperadmin": "", "key": year.code}
    user = crud.user.get_card_signer(db=db)
    university = crud.university.get_info(db=db)
    if user:
        data["supperadmin"] = f"{user.last_name} {user.first_name}"

    heads = special_heads_card.parcourir_et(jsonable_encoder(students), data, university)
    tails = special_tails_card.parcourir_et(jsonable_encoder(students))

    return [_build_pdf_response(heads), _build_pdf_response(tails)]

# @router.get("/carte_after/")
# def create_after_carte(
#         id_year: int,
#         id_mention: str,
#         id_journey: str = "",
#         level: str = "M2",
#         db: Session = Depends(deps.get_db),
#         current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     create list au examen
#     """
#     year = crud.college_year.get(db=db, id=id_year)
#     if not year:
#         raise HTTPException(
#             status_code=400,
#             detail=f"College year not found.",
#         )
#     journey = crud.journey.get(db=db, id=id_journey)
#     if not journey:
#         raise HTTPException(
#             status_code=400,
#             detail=f" Journey not found.",
#         )
#     data = get_semester(level)
#     semester = (data[0],)
#     semester2 = data[1]
#     students = crud.ancien_student.get_for_carte(
#         db=db,
#         id_journey=id_journey,
#         id_year=id_year,
#         semester=semester,
#         semester2=semester2,
#     )
#
#     mention = crud.mention.get_by_id(db=db, uuid=id_mention)
#     if not mention:
#         raise HTTPException(
#             status_code=400,
#             detail=f" Mention not found.",
#         )
#
#     data = {
#         "supperadmin": "",
#         "mention": mention.title,
#         "key": year.code,
#         "img_carte": (mention.plugged.lower())[0:1],
#     }
#
#     file = arrire_carte.parcourir_et(students, data)
#
#     return FileResponse(path=file, media_type="application/octet-stream", filename=file)

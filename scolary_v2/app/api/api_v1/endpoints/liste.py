import ast
from pathlib import Path
from typing import Any, List, Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.utils_sco.list import list_bourse, list_exams, list_select
from app.utils_sco.list.list_by_group import create_list_group
from app.utils_sco.list.list_inscrit import create_list_registered
from app.utils import (
    create_model,
    find_in_list,
    get_last_year,
    get_level,
)

from app.pdf.PDFMark import PDFMark as FPDF

router = APIRouter()


def _build_pdf_response(result: Union[dict, str]) -> schemas.PdfFileResponse:
    if isinstance(result, dict):
        path = str(result.get("path", "")).lstrip("/")
        filename = str(result.get("filename", ""))
    else:
        pdf_path = Path(str(result)).as_posix().lstrip("/")
        filename = Path(pdf_path).name
        # strip leading "files/" if present
        remainder = Path(pdf_path)
        if remainder.parts and remainder.parts[0] == "files":
            path = Path(*remainder.parts[1:-1]).as_posix()
        else:
            path = Path(*remainder.parts[:-1]).as_posix()

    if path and not path.endswith("/"):
        path = f"{path}/"
    url = f"/files/{path}{filename}" if filename else ""
    return schemas.PdfFileResponse(path=path, filename=filename, url=url)


@router.get("/list_exam/", response_model=schemas.PdfFileResponse)
def list_examen(
        id_year: int,
        semester: str,
        id_journey: int,
        session: str,
        salle: str,
        skip: int = 1,
        limit: int = 10000,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    create list au examen
    """

    journey = crud.journey.get(db=db, id=id_journey)
    if not journey:
        raise HTTPException(
            status_code=400,
            detail=f" Journey not found.",
        )

    college_year = crud.college_year.get(db=db, id=id_year)
    if not college_year:
        raise HTTPException(
            status_code=400,
            detail=f" year not found.",
        )

    mention = crud.mention.get(db=db, id=journey.id_mention)
    if not mention:
        raise HTTPException(
            status_code=400,
            detail=f" Mention not found.",
        )

    interaction = crud.interaction.get_by_journey_and_year(
        db=db, id_journey=id_journey, id_year=id_year
    )
    interaction_value = jsonable_encoder(interaction)
    list_value = []
    for value in interaction_value[semester.lower()]:
        value = ast.literal_eval(value)
        list_value.append(value)
    interaction = jsonable_encoder(interaction)
    interaction[semester.lower()] = list_value
    columns = interaction[semester.lower()]

    data = {}
    matiers = {}

    university = crud.university_info.get_university(db=db)
    if len(columns) == 0:
        raise HTTPException(
            status_code=400,
            detail="Matiers not found.",
        )
    all_ue = []
    for ue in create_model(columns):
        ues_ = {"name": ue["title"]}
        nbr = 0
        all_ec = []
        for ec in ue["ec"]:
            ecs_ = {"name": ec["title"]}
            nbr += 1
            all_ec.append(ecs_)
        ues_["nbr_ec"] = nbr
        ues_["ec"] = all_ec
        all_ue.append(ues_)
    matiers["ue"] = all_ue

    students = crud.note.read_all_note(
        journey=journey.abbreviation,
        session=session,
        year=id_year,
        semester=semester,
        skip=skip,
        limit=limit - skip,
    )

    all_students = []
    if len(students) == 0:
        raise HTTPException(
            status_code=400,
            detail="Etudiants not found.",
        )
    for on_student in students:
        un_et = crud.ancien_student.get_by_num_carte(
            db=db, num_carte=on_student["num_carte"]
        )
        student_years = crud.student_years.get_num_carte_and_year(
            db=db, id_year=id_year, num_carte=on_student["num_carte"]
        )
        if un_et and student_years:
            student = {
                "last_name": un_et.last_name,
                "first_name": un_et.first_name,
                "num_carte": un_et.num_carte,
            }
            all_students.append(student)
    data["mention"] = mention.title
    data["journey"] = journey.title
    data["anne"] = college_year.title
    data["session"] = session
    data["salle"] = salle
    data["skip"] = skip + 1
    data["limit"] = limit
    file = list_exams.PDF.create_list_examen(
        semester, journey.abbreviation, data, matiers, all_students, university
    )
    return _build_pdf_response(file)


@router.get("/list_registered/", response_model=schemas.PdfFileResponse)
def list_registered(
        id_year: int,
        semester: str,
        id_journey: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    create list registered
    """
    accademic_years = crud.academic_year.get(db=db, id=id_year)
    if not accademic_years:
        raise HTTPException(
            status_code=400,
            detail=f"college_year not found.",
        )
    journey = crud.journey.get(db=db, id=id_journey)
    if not journey:
        raise HTTPException(
            status_code=400,
            detail=f" Journey not found.",
        )

    university = crud.university.get_info(db=db)
    mention = crud.mention.get(db=db, id=journey.id_mention)

    relations = []

    wheres_relations = []

    base_columns = []

    wheres = [
        {
            "key": "annual_register.id_academic_year",
            "operator": "==",
            "value": id_year
        },
        {
            "key": "annual_register.register_semester.id_journey",
            "operator": "==",
            "value": id_journey
        },
        {
            "key": "annual_register.register_semester.semester",
            "operator": "==",
            "value": semester
        }
    ]

    students = crud.student.get_multi_where_array(
        db=db,
        relations=relations,
        where=wheres,
        base_columns=base_columns,
        where_relation=wheres_relations
    )
    all_student = []
    for on_student in students:
        student = {
            "last_name": on_student.last_name,
            "first_name": on_student.first_name,
            "num_carte": on_student.num_carte,
        }
        all_student.append(student)

    data = {
        "mention": mention.name,
        "journey": journey.name,
        "anne": accademic_years.name,
    }
    lists = create_list_registered(
        semester, journey.abbreviation, data, all_student, university
    )
    return _build_pdf_response(lists)


@router.get("/list_by_group/", response_model=schemas.PdfFileResponse)
def list_by_group(
        id_year: int,
        semester: str,
        id_journey: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    create list registered
    """
    accademic_years = crud.college_year.get(db=db, id=id_year)
    if not accademic_years:
        raise HTTPException(
            status_code=400,
            detail=f"college_year not found.",
        )
    journey = crud.journey.get(db=db, id=id_journey)
    if not journey:
        raise HTTPException(
            status_code=400,
            detail=f" Journey not found.",
        )
    student_group = crud.student_group.get_by_journey_and_semester(db=db, id_journey=id_journey, semester=semester)
    mention = crud.mention.get(db=db, id=journey.id_mention)
    count_students = crud.ancien_student.get_count_by_mention_and_year(
        db=db,
        id_journey=id_journey,
        semester=semester,
        id_mention=journey.id_mention,
        id_year=id_year,
    )
    skip = 0
    group = 1
    pdf = FPDF("P", "mm", "a4")

    data = {
        "mention": mention.title,
        "journey": journey.title,
        "anne": accademic_years.title,
    }

    university = crud.university_info.get_university(db=db)
    while skip < count_students:
        students = crud.ancien_student.get_by_mention_and_year(
            db=db,
            id_journey=id_journey,
            semester=semester,
            id_mention=journey.id_mention,
            id_year=id_year,
            limit=student_group.student_count,
            skip=skip,
        )
        all_student = []
        for on_student in students:
            student = {
                "last_name": on_student.last_name,
                "first_name": on_student.first_name,
                "num_carte": on_student.num_carte,
            }
            all_student.append(student)

        create_list_group(pdf, semester, data, all_student, group, university)
        group += 1
        skip += student_group.student_count
    pdf.output(
        f"files/pdf/list/list_by_group_{semester}_{journey}.pdf", "F"
    )
    return _build_pdf_response(
        {"path": "pdf/list/", "filename": f"list_by_group_{semester}_{journey}.pdf"}
    )


@router.get("/list_selection/", response_model=schemas.PdfFileResponse)
def list_selection(
        id_year: str,
        id_mention: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    create list au examen
    """
    accademic_years = crud.academic_year.get(db=db, id=id_year)
    if not accademic_years:
        raise HTTPException(
            status_code=400,
            detail=f"year not found.",
        )
    mention = crud.mention.get(db=db, id=id_mention)
    if not mention:
        raise HTTPException(
            status_code=400,
            detail=f"Mention not found.",
        )
    students = crud.student.get_selected_by_mention_year(
        db=db, id_mention=mention.id, id_year=id_year
    )

    level = ["L1", "M1", "M2"]
    all_students = {}

    university = crud.university.get_info(db=db)
    if students:
        for lev in level:
            student_lev = []
            for on_student in students:
                student = {
                    "last_name": on_student.last_name,
                    "first_name": on_student.first_name,
                    "num_select": on_student.num_select,
                }
                print(on_student.level.value)
                if (on_student.level.value or "") == lev:
                    student_lev.append(student)

            all_students[lev] = student_lev

    data = {"mention": mention.name, "anne": accademic_years.name}

    file = list_select.create_list_select(mention.name, data, all_students, university)
    return _build_pdf_response(file)


@router.get("/list_bourse_passant/", response_model=schemas.PdfFileResponse)
def list_bourse_passant(
        id_year: str,
        id_mention: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    create list bourse

    """
    type_ = "Passant"
    all_data = {}
    all_journey = []
    mention = crud.mention.get_by_id(db=db, uuid=id_mention)
    if not mention:
        raise HTTPException(
            status_code=404,
            detail="The mention with this uuid does not exist in the system.",
        )
    journeys = crud.journey.get_by_mention(db=db, id_mention=id_mention)
    all_data["mention"] = mention.title
    college_year = crud.college_year.get(db=db, id=id_year)
    for journey in journeys:
        journey_ = {"name": journey.title}
        l1 = []
        l2 = []
        l3 = []
        m1 = []
        m2 = []
        students_ = crud.ancien_student.get_by_journey_and_type(
            db=db, id_journey=journey.id, type_=type_
        )

        for student in students_:
            student_year = crud.student_years.get_num_carte_and_year(
                db=db, num_carte=student.num_carte, id_year=id_year
            )

            print(student_year, student.num_carte)
            if student_year:
                students = {
                    "last_name": student.last_name,
                    "first_name": student.first_name,
                    "num_carte": student.num_carte,
                }
                level = get_level(student_year.inf_semester, student_year.sup_semester)
                if level == "L1":
                    if get_last_year(student.baccalaureate_years, college_year.title):
                        l1.append(students)
                if level == "L2":
                    l2.append(students)
                if level == "L3":
                    l3.append(students)
                if level == "M1":
                    m1.append(students)
                if level == "M2":
                    m2.append(students)
        journey_["l1"] = l1
        journey_["l2"] = l2
        journey_["l3"] = l3
        journey_["m1"] = m1
        journey_["m2"] = m2
        all_journey.append(journey_)
    all_data["journey"] = all_journey
    all_data["year"] = college_year.title
    print(all_journey)

    file = list_bourse.PDF.create_list_bourse(mention.title, all_data, type_)
    return _build_pdf_response(file)


@router.get("/list_bourse_redoublant/", response_model=schemas.PdfFileResponse)
def list_bourse_passant(
        college_year: str,
        id_mention: str,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    create list bourse

    """
    type_ = "Redoublant"
    all_data = {}
    all_journey = []
    mention = crud.mention.get_by_id(db=db, uuid=id_mention)
    if not mention:
        raise HTTPException(
            status_code=404,
            detail="The mention with this uuid does not exist in the system.",
        )

    college_year = crud.college_year.get_by_title(db=db, title=college_year)
    if not college_year:
        raise HTTPException(
            status_code=404,
            detail="The college year with this uuid does not exist in the system.",
        )
    journeys = crud.journey.get_by_mention(db=db, id_mention=id_mention)
    all_data["mention"] = mention.title
    for journey in journeys:
        journey_ = {"name": journey.title}
        l1 = []
        l2 = []
        l3 = []
        m1 = []
        m2 = []
        students_ = crud.ancien_student.get_by_journey_and_type_and_mean(
            db=db, id_journey=journey.id, type_=type_, mean=college_year.mean
        )
        for student in students_:
            if find_in_list(student.actual_years, college_year) != -1:
                students = {
                    "last_name": student.last_name,
                    "first_name": student.first_name,
                    "num_carte": student.num_carte,
                }
                level = get_level(student.inf_semester, student.sup_semester)
                if level == "L1":
                    l1.append(students)
                if level == "L2":
                    l2.append(students)
                if level == "L3":
                    l3.append(students)
                if level == "M1":
                    m1.append(students)
                if level == "M2":
                    m2.append(students)
        journey_["l1"] = l1
        journey_["l2"] = l2
        journey_["l3"] = l3
        journey_["m1"] = m1
        journey_["m2"] = m2
        all_journey.append(journey_)
    all_data["journey"] = all_journey
    all_data["year"] = college_year.title

    file = list_bourse.PDF.create_list_bourse(mention.title, all_data, type_)
    return _build_pdf_response(file)

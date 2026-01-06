from typing import Any

from app.pdf.PDFMark import PDFMark as FPDF
from .header import header
from app.utils import clear_name


def add_title(pdf: FPDF, data: Any, sems: str, title: str):
    pdf.add_font("alger", "", "font/Algerian.ttf", uni=True)

    header(pdf)
    mention = "MENTION:"
    mention_student = f"{data['mention']}"
    journey = "PARCOURS:"
    journey_student = f"{data['journey']}"
    semester = "SEMESTRE:"
    semester_student = f"{sems.upper()}"
    anne = "ANNÉE UNIVERSITAIRE:"
    anne_univ = f"{data['anne']}"

    pdf.set_font("alger", "", 22)
    pdf.cell(0, 15, txt="", ln=1, align="C")
    pdf.cell(0, 15, txt=title, ln=1, align="C")

    pdf.set_font("arial", "BI", 13)
    pdf.cell(24, 8, txt=mention, ln=0, align="L")

    pdf.set_font("arial", "I", 12)
    pdf.cell(0, 8, mention_student, 0, 1)

    pdf.set_font("arial", "BI", 13)
    pdf.cell(29, 8, txt=journey, ln=0, align="L")

    pdf.set_font("arial", "I", 12)
    pdf.cell(0, 8, txt=journey_student, ln=1)

    pdf.set_font("arial", "BI", 13)
    pdf.cell(28, 8, txt=semester, ln=0, align="L")

    pdf.set_font("arial", "I", 12)
    pdf.cell(0, 8, txt=semester_student, ln=1)

    pdf.set_font("arial", "BI", 13)
    pdf.cell(56, 8, txt=anne, ln=0, align="L")

    pdf.set_font("arial", "I", 12)
    pdf.cell(0, 8, txt=anne_univ, ln=1)


def create_list_registered(
    sems: str,
    journey: str,
    data: Any,
    students: Any,
    university,
    start_number: int = 1
):
    pdf = FPDF("P", "mm", "a4")
    pdf.watermark(f"{str(university.department_name).capitalize()}", y=175, font_style="BI")
    pdf.add_page()
    titre = "LISTE DES ÉTUDIANTS INSCRITS"
    add_title(pdf=pdf, data=data, sems=sems, title=titre)

    num = "N°"
    card_number = "N° Carte"
    nom_et_prenom = "Nom et prénom"

    pdf.cell(1, 7, txt="", ln=1)
    pdf.set_font("arial", "BI", 10)
    pdf.cell(1, 5, txt="")
    pdf.cell(20, 5, txt=num, border=1, align="C")
    pdf.cell(1, 5, txt="")
    pdf.cell(30, 5, txt=card_number, border=1, align="C")
    pdf.cell(1, 5, txt="")
    pdf.cell(138, 5, txt=nom_et_prenom, border=1, ln=0, align="C")
    num_ = start_number
    for i, student in enumerate(students):
        num_select_ = str(student.get("num_carte") or "")
        name = f"{clear_name(student['last_name'])} {student['first_name']}"
        pdf.cell(1, 7, txt="", ln=1)
        pdf.set_font("arial", "I", 10)
        pdf.cell(1, 5, txt="")
        pdf.cell(20, 5, txt=str(num_), border=1, ln=0, align="C")
        pdf.cell(1, 5, txt="")
        pdf.cell(30, 5, txt=num_select_, border=1, ln=0, align="C")
        pdf.cell(1, 5, txt="")
        pdf.set_font("arial", "I", 10)
        pdf.cell(138, 5, txt=name, border=1, ln=0, align="L")
        num_ += 1
    pdf.output(
        f"files/pdf/list/list_register_{sems}_{journey}.pdf", "F"
    )
    return {"path": f"pdf/list/", "filename": f"list_register_{sems}_{journey}.pdf"}

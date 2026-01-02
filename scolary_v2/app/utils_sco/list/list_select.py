from typing import Any

from app.pdf.PDFMark import PDFMark as FPDF
from .header import header
from app.utils import clear_name


def add_title(pdf: FPDF, data: Any, title: str):
    header(pdf)
    pdf.add_font("alger", "", "font/Algerian.ttf", uni=True)
    mention = "MENTION:"
    mention_student = f"{data['mention']}"
    anne = "ANNÉE UNIVERSITAIRE:"
    anne_univ = f"{data['anne']}"

    pdf.set_font("alger", "", 14)
    pdf.cell(0, 15, txt="", ln=1, align="C")
    pdf.cell(0, 15, txt=title, ln=1, align="C")

    pdf.set_font("arial", "BI", 13)
    pdf.cell(24, 8, txt=mention, ln=0, align="L")

    pdf.set_font("arial", "I", 12)
    pdf.cell(0, 8, txt=mention_student, ln=1)

    pdf.set_font("arial", "BI", 13)
    pdf.cell(56, 8, txt=anne, ln=0, align="L")

    pdf.set_font("arial", "I", 12)
    pdf.cell(0, 8, txt=anne_univ, ln=1)


def create_list_select(mention: str, data: Any, students: Any, university):
    # Determine levels present; fall back to common order
    base_levels = ["L1", "L2", "L3", "M1", "M2"]
    present_levels = [
        lvl for lvl in base_levels if lvl in students and len(students.get(lvl, [])) > 0
    ]
    levels = present_levels if present_levels else base_levels
    pdf = FPDF("P", "mm", "a4")

    for niv in levels:
        current_students = students.get(niv, [])
        if len(current_students) != 0:
            titre = f"LISTE DES ÉTUDIANTS ADMIS PAR SÉLÉCTION DE DOSSIER EN {niv}"
            pdf.add_page()
            pdf.watermark(f"{str(university.department_name).capitalize()}", y=175, font_style="BI")
            add_title(pdf=pdf, data=data, title=titre)

            num = "N°"
            full_name = "Nom et prénom"

            pdf.cell(1, 7, txt="", ln=1)
            pdf.set_font("arial", "BI", 10)
            pdf.cell(1, 5, txt="")
            pdf.cell(25, 5, txt=num, border=1)
            pdf.cell(1, 5, txt="")
            pdf.cell(163, 5, txt=full_name, border=1, ln=0, align="C")
            num_ = 1
            for i, student in enumerate(current_students):
                num_select_ = student["num_select"]
                name = (
                    f"{clear_name(student['last_name'])} {student['first_name']}"
                )
                pdf.cell(1, 7, txt="", ln=1)
                pdf.set_font("arial", "I", 10)
                pdf.cell(1, 5, txt="")
                pdf.cell(25, 5, txt=num_select_, border=1, ln=0)
                pdf.cell(1, 5, txt="")
                pdf.set_font("arial", "I", 10)
                pdf.cell(163, 5, txt=name, border=1, ln=0, align="L")
                num_ += 1

    pdf.output(f"files/pdf/list/list_select_{mention}.pdf", "F")
    return {"path": f"pdf/list/", "filename": f"list_select_{mention}.pdf"}

from typing import Any, List, Dict
import re

from app.pdf.PDFMark import PDFMark as FPDF
from .header import header
from app.utils import clear_name


def _sanitize_filename(value: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9_-]+", "_", value.strip())
    return safe or "year"


def create_list_registered_by_year(
    year_label: str,
    students: List[Dict[str, Any]]
) -> Dict[str, str]:
    pdf = FPDF("P", "mm", "a4")
    pdf.add_page()
    header(pdf)

    title = "LISTE DES ÉTUDIANTS INSCRITS"
    pdf.set_font("arial", "B", 16)
    pdf.cell(0, 10, txt=title, ln=1, align="C")
    pdf.set_font("arial", "I", 12)
    pdf.cell(0, 8, txt=f"Année universitaire : {year_label}", ln=1, align="C")

    pdf.ln(4)
    pdf.set_font("arial", "B", 10)
    pdf.cell(10, 7, txt="N°", border=1, align="C")
    pdf.cell(35, 7, txt="N° Carte", border=1, align="C")
    pdf.cell(105, 7, txt="Nom et prénom", border=1, align="C")
    pdf.cell(30, 7, txt="Niveau", border=1, align="C")

    pdf.set_font("arial", "", 10)
    for index, student in enumerate(students, start=1):
        card_number = clear_name(student.get("num_carte", ""), 24)
        full_name = clear_name(student.get("full_name", ""), 60)
        level = clear_name(student.get("level", ""), 12) or "-"

        pdf.ln(7)
        pdf.cell(10, 7, txt=str(index), border=1, align="C")
        pdf.cell(35, 7, txt=card_number, border=1)
        pdf.cell(105, 7, txt=full_name, border=1)
        pdf.cell(30, 7, txt=level, border=1, align="C")

    filename_suffix = _sanitize_filename(year_label)
    filename = f"list_register_{filename_suffix}.pdf"
    pdf.output(f"files/pdf/list/{filename}", "F")
    return {"path": "pdf/list/", "filename": filename}

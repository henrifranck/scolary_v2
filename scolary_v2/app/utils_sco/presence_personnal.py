from typing import Any

from app.pdf.PDFMark import PDFMark as FPDF
from app.utils import clear_name
from app.utils_sco.list import header


def getPresence(presence: bool):
    if presence:
        return "Présent"
    return "Absent"


def add_title(pdf: FPDF, data: Any, title: str):
    pdf.add_font("alger", "", "font/Algerian.ttf", uni=True)
    user = data["user"]
    header(pdf)
    full_name = "Nom et Prénom: "
    full_name_user = f"{user['last_name']} {user['first_name']}"

    role = "Role: "
    role_user = f"{user['role']['title']} (Résponsable)" if user['is_admin'] else f"{user['role']['title']}"

    pdf.set_font("alger", "", 22)
    pdf.cell(0, 15, txt="", ln=1, align="C")
    pdf.cell(0, 15, txt=title, ln=1, align="C")

    pdf.set_font("arial", "BI", 18)
    pdf.cell(50, 8, txt=full_name, ln=0, align="L")

    pdf.set_font("arial", "I", 16)
    pdf.cell(0, 8, full_name_user, 0, 1)

    pdf.set_font("arial", "BI", 18)
    pdf.cell(20, 8, txt=role, ln=0, align="L")

    pdf.set_font("arial", "I", 16)
    pdf.cell(0, 8, role_user, 0, 1)


def create_presence(data: Any, university, session):
    pdf = FPDF("P", "mm", "a4")
    pdf.watermark(f"{str(university.department_name).capitalize()}", y=175, font_style="BI")
    for data in data:
        pdf.add_page()
        titre = f"Fiche de présence à l'examen session {session}"
        add_title(pdf=pdf, data=data, title=titre)

        gap = 4.5

        date = "Date"
        morning = "Matin"
        afternoon = "Après-midi"
        classroom = "Salle de classe"

        pdf.cell(1, 7, txt="", ln=1)
        pdf.set_font("arial", "BI", 10)
        pdf.cell(1, 5, txt="")
        pdf.cell(pdf.w / gap, 5, txt=date, border=1)
        pdf.cell(1, 5, txt="")
        pdf.cell(pdf.w / gap, 5, txt=morning, border=1, ln=0, align="C")
        pdf.cell(1, 5, txt="")
        pdf.cell(pdf.w / gap, 5, txt=afternoon, border=1, ln=0, align="C")
        pdf.cell(1, 5, txt="")
        pdf.cell(pdf.w / gap, 5, txt=classroom, border=1, ln=0, align="C")
        num_ = 1
        for i, user_info in enumerate(data["info"]):
            date = user_info["date"]
            morning = getPresence(user_info["morning"])
            afternoon = getPresence(user_info["afternoon"])
            classroom = user_info["classroom"]
            pdf.cell(1, 7, txt="", ln=1)
            pdf.set_font("arial", "I", 10)
            pdf.cell(1, 5, txt="")
            pdf.cell(pdf.w / gap, 5, txt=date, border=1, ln=0)
            pdf.cell(1, 5, txt="")
            pdf.set_font("arial", "I", 10)
            pdf.cell(pdf.w / gap, 5, txt=morning, border=1, ln=0, align="C")
            pdf.cell(1, 5, txt="")
            pdf.cell(pdf.w / gap, 5, txt=afternoon, border=1, ln=0, align="C")
            pdf.cell(1, 5, txt="")
            pdf.cell(pdf.w / gap, 5, txt=classroom, border=1, ln=0, align="C")
            num_ += 1
    pdf.output(
        f"files/pdf/list/presence.pdf", "F"
    )
    return {"path": f"pdf/list/", "filename": f"presence.pdf"}

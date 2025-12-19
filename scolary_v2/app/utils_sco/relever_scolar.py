import os
from typing import Any, Dict

from app.pdf.PDFMark import PDFMark as FPDF
from app.utils import convert_date, is_begin_with_vowel
from app.utils_sco.list import header


def validation(ue: float, code: bool) -> str:
    if not ue:
        return "Non Classée"
    elif float(ue) < 10:
        if code:
            return "Compensé"
        else:
            return "Non Validé"
    else:
        return "Validé"


def note_scolary(num_carte: str, data: Any, note: Any, university) -> dict[str, str]:
    pdf = PDF()

    # set watermark prior to calling add_page()
    pdf.watermark(f"{str(university.department_name).capitalize()}", y=175, font_style="BI")
    pdf.add_page()

    pdf.set_xy(0, 9)
    pdf.l_margin = 0
    pdf.rect(3, 3, 204, 291)
    pdf.rect(2, 2, 206, 293)
    pdf.l_margin = 8
    titre5 = "releve de note"

    pdf.set_text_color(0, 0, 0)
    full_name_ = "Nom et prénom:"
    full_name__student = f"{data['last_name']} {data['first_name'] if data['first_name'] != 'None' else ''} "
    birth = "Né(e) le:"
    birth_student = f"{convert_date(data['date_birth'])} à {data['place_birth']}"
    number_ = "N° carte:"
    semester = f"Semestre:"
    semester_student = f"{data['semester']}"
    mention = "Mention:"
    mention_student = f"{data['mention']}"
    journey = "Parcours:"
    journey_student = f"{data['journey']}"
    session = f"Session:"
    session_student = f"{data['session'].title()}"

    titre_1 = "Les unité d'enseignements"
    titre_2 = "Notes(/20)"
    titre_3 = "Coéfficients"
    titre_4 = "Crédits"
    titre_5 = "Status de l'UE"
    mean = "moyenne générale"

    pdf.add_font("alger", "", "font/Algerian.ttf", uni=True)
    pdf.add_font("aparaj", "", "font/aparaj.ttf", uni=True)

    pdf.set_font("arial", "B", 10)
    header(pdf)
    pdf.set_font("arial", "B", 10)
    pdf.cell(193, 5, ln=1, align="C")
    pdf.cell(193, 5, txt=titre5.upper(), ln=1, align="C")

    pdf.l_margin = 0
    pdf.ln(3)
    pdf.rect(12, 42, 188, 23)

    pdf.set_font("arial", "BI", 11)
    pdf.cell(18, 5, txt="", ln=0, align="L")
    pdf.cell(32, 5, txt=full_name_, ln=0, align="L")

    pdf.set_font("aparaj", "", 11)
    pdf.cell(100, 5, txt=full_name__student, ln=1)

    pdf.set_font("arial", "BI", 11)
    pdf.cell(18, 5, txt="", ln=0, align="L")
    pdf.cell(21, 5, txt=birth, ln=0, align="L")
    pdf.set_font("aparaj", "", 12)
    pdf.cell(100, 5, txt=birth_student, ln=0)

    pdf.set_font("arial", "BI", 11)
    pdf.cell(18, 5, txt="", ln=0, align="L")
    pdf.cell(21, 5, txt=number_, ln=0, align="L")
    pdf.set_font("aparaj", "", 12)
    pdf.cell(0, 5, txt=num_carte, ln=1)

    pdf.set_font("arial", "BI", 11)
    pdf.cell(18, 5, txt="", ln=0, align="L")
    pdf.cell(21, 5, txt=journey, ln=0, align="L")
    pdf.set_font("aparaj", "", 12)
    pdf.cell(100, 5, txt=journey_student, ln=0)

    pdf.set_font("arial", "BI", 11)
    pdf.cell(18, 5, txt="", ln=0, align="L")
    pdf.cell(21, 5, txt=semester, ln=0, align="L")
    pdf.set_font("aparaj", "", 12)
    pdf.cell(0, 5, txt=semester_student, ln=1)

    pdf.set_font("arial", "BI", 11)
    pdf.cell(18, 5, txt="", ln=0, align="L")
    pdf.cell(21, 5, txt=mention, ln=0, align="L")
    pdf.set_font("aparaj", "", 12)
    pdf.cell(100, 5, txt=mention_student, ln=0)

    pdf.set_font("arial", "BI", 11)
    pdf.cell(18, 5, txt="", ln=0, align="L")
    pdf.cell(21, 5, txt=session, ln=0, align="L")
    pdf.set_font("aparaj", "", 12)
    pdf.cell(0, 5, txt=session_student, ln=1)

    # debut de creation du tableau
    pdf.cell(30, 2, txt="", ln=1)
    pdf.set_font("arial", "I", 10)
    pdf.cell(12, 2, txt="", ln=0)

    pdf.set_fill_color(210, 210, 210)
    pdf.cell(98, 5, txt=titre_1.upper(), border=1, ln=0, align="C", fill=True)

    pdf.cell(20, 5, txt=titre_2, border=1, ln=0, align="C", fill=True)

    pdf.cell(25, 5, txt=titre_3, border=1, ln=0, align="C", fill=True)

    pdf.cell(15, 5, txt=titre_4, border=1, ln=0, align="C", fill=True)

    pdf.cell(30, 5, txt=titre_5, border=1, ln=1, align="C", fill=True)

    for index_ue, value_ue in enumerate(note["ue"]):
        pdf.set_top_margin(20)
        pdf.cell(30, 1, txt="", ln=1)
        pdf.cell(12, 2, txt="", ln=0)
        pdf.set_font("arial", "BI", 9)
        pdf.cell(
            98,
            5,
            txt=f"U.E-{index_ue + 1}: {value_ue['name']}",
            border=1,
            ln=0,
            align="C",
        )
        pdf.set_font("arial", "I", 11)
        pdf.cell(1, 1, txt="", ln=0)
        pdf.cell(19, 5, txt="", border=1, ln=0, align="C")
        pdf.cell(1, 1, txt="", ln=0)
        pdf.cell(24, 5, txt="", border=1, ln=0, align="C")
        pdf.cell(1, 1, txt="", ln=0)
        pdf.cell(14, 5, txt="", border=1, ln=0, align="C")
        pdf.cell(1, 1, txt="", ln=0)
        pdf.cell(29, 5, txt="", border=1, ln=1, align="C")
        for index, value in enumerate(value_ue["ec"]):
            pdf.set_top_margin(20)
            pdf.cell(30, 1, txt="", ln=1)
            pdf.cell(12, 2, txt="", ln=0)
            pdf.set_font("arial", "I", 9)
            pdf.cell(
                98,
                5,
                txt=f"E.C-{index + 1}: {value['name']}",
                border=1,
                ln=0,
                align="L",
            )
            pdf.set_font("arial", "I", 11)
            pdf.cell(1, 1, txt="", ln=0)
            pdf.cell(19, 5, txt=str(value["note"]) if value["note"] else "Absent", border=1, ln=0, align="C")
            pdf.cell(1, 1, txt="", ln=0)
            pdf.cell(24, 5, txt=str(value["weight"]), border=1, ln=0, align="C")
            pdf.cell(1, 1, txt="", ln=0)
            pdf.cell(14, 5, txt="", border=1, ln=0, align="C")
            pdf.cell(1, 1, txt="", ln=0)
            pdf.cell(29, 5, txt="", border=1, ln=1, align="C")
        pdf.set_top_margin(20)
        pdf.cell(30, 1, txt="", ln=1)
        pdf.cell(12, 2, txt="", ln=0)
        pdf.set_font("arial", "BI", 9)
        pdf.cell(
            98, 5, txt=f"NOTE SOUS TOTAL U.E-{index_ue + 1}", border=1, ln=0, align="C"
        )
        pdf.set_font("arial", "I", 9)
        pdf.cell(1, 1, txt="", ln=0)
        pdf.cell(
            19, 5, txt=str(format(value_ue["note"], ".2f")), border=1, ln=0, align="C"
        )
        pdf.cell(1, 1, txt="", ln=0)
        pdf.cell(24, 5, txt="", border=1, ln=0, align="C")
        pdf.cell(1, 1, txt="", ln=0)
        pdf.cell(14, 5, txt=str(value_ue["credit"]), border=1, ln=0, align="C")
        pdf.cell(1, 1, txt="", ln=0)
        pdf.set_font("alger", "", 9)
        pdf.cell(
            29,
            5,
            txt=validation(value_ue["note"], data["code"]),
            border=1,
            ln=1,
            align="C",
        )

    pdf.set_top_margin(20)
    pdf.cell(30, 1, txt="", ln=1)
    pdf.cell(12, 2, txt="", ln=0)
    pdf.set_font("arial", "BI", 9)
    pdf.cell(98, 6, txt=mean.upper(), border=1, ln=0, align="C")
    pdf.set_font("arial", "I", 10)
    pdf.cell(1, 1, txt="", ln=0)
    pdf.cell(19, 6, txt=str(format(note["mean"], ".2f")), border=1, ln=0, align="C")
    pdf.cell(1, 1, txt="", ln=0)
    pdf.cell(24, 5, txt="", ln=0)
    pdf.cell(1, 1, txt="", ln=0)
    pdf.cell(14, 5, txt="", ln=0)
    pdf.cell(1, 1, txt="", ln=0)
    pdf.cell(29, 5, txt="", ln=1)

    pdf.set_font("Times", "Bui", 10)
    pdf.cell(40, 10, txt="", ln=0)
    pdf.set_font("arial", "I", 10)
    pdf.cell(130, 1, txt="", ln=1)
    pdf.cell(130, 8, txt="", ln=0)

    pdf.l_margin = 8

    logo_scolar = "images/y_scolar.png"
    logo_scolar = logo_scolar if os.path.exists(logo_scolar) else "images/no_image.png"
    pdf.image(logo_scolar, x=pdf.w - 30, y=pdf.h - 27, w=30, h=25)

    pdf.output(f"files/pdf/relever/{num_carte}_relever.pdf", "F")

    return {"path": f"pdf/relever/", "filename": f"{num_carte}_relever.pdf"}


def note_scola_list(pdf, num_carte: str, data: Any, note: Any, university) -> dict[str, str]:
    # set watermark prior to calling add_page()
    pdf.watermark(f"{str(university.department_name).capitalize()}", y=175, font_style="BI")
    pdf.add_page()
    pdf.l_margin = 0
    pdf.rect(3, 3, 204, 291)
    pdf.rect(2, 2, 206, 293)
    pdf.l_margin = 8
    titre5 = "releve de note"

    pdf.set_text_color(0, 0, 0)
    full_name_ = "Nom et prénom:"
    full_name__student = f"{data['last_name']} {data['first_name'] if data['first_name'] != 'None' else ''} "
    birth = "Né(e) le:"
    birth_student = f"{convert_date(data['date_birth'])} à {data['place_birth']}"
    number_ = "N° carte:"
    semester = f"Semestre:"
    semester_student = f"{data['semester']}"
    mention = "Mention:"
    mention_student = f"{data['mention']}"
    journey = "Parcours:"
    journey_student = f"{data['journey']}"
    session = f"Session:"
    session_student = f"{data['session'].title()}"

    titre_1 = "Les unité d'enseignements"
    titre_2 = "Notes(/20)"
    titre_3 = "Coéfficients"
    titre_4 = "Crédits"
    titre_5 = "Status de l'UE"
    mean = "moyenne générale"

    pdf.add_font("alger", "", "font/Algerian.ttf", uni=True)
    pdf.add_font("aparaj", "", "font/aparaj.ttf", uni=True)

    pdf.set_font("arial", "B", 10)
    pdf.set_xy(0, 9)
    header(pdf)
    pdf.set_font("arial", "B", 10)
    pdf.cell(193, 5, ln=1, align="C")
    pdf.cell(193, 5, txt=titre5.upper(), ln=1, align="C")

    pdf.l_margin = 0
    pdf.ln(3)
    pdf.rect(12, 42, 188, 23)

    pdf.set_font("arial", "BI", 11)
    pdf.cell(18, 5, txt="", ln=0, align="L")
    pdf.cell(32, 5, txt=full_name_, ln=0, align="L")

    pdf.set_font("aparaj", "", 11)
    pdf.cell(100, 5, txt=full_name__student, ln=1)

    pdf.set_font("arial", "BI", 11)
    pdf.cell(18, 5, txt="", ln=0, align="L")
    pdf.cell(21, 5, txt=birth, ln=0, align="L")
    pdf.set_font("aparaj", "", 12)
    pdf.cell(100, 5, txt=birth_student, ln=0)

    pdf.set_font("arial", "BI", 11)
    pdf.cell(18, 5, txt="", ln=0, align="L")
    pdf.cell(21, 5, txt=number_, ln=0, align="L")
    pdf.set_font("aparaj", "", 12)
    pdf.cell(0, 5, txt=num_carte, ln=1)

    pdf.set_font("arial", "BI", 11)
    pdf.cell(18, 5, txt="", ln=0, align="L")
    pdf.cell(21, 5, txt=journey, ln=0, align="L")
    pdf.set_font("aparaj", "", 12)
    pdf.cell(100, 5, txt=journey_student, ln=0)

    pdf.set_font("arial", "BI", 11)
    pdf.cell(18, 5, txt="", ln=0, align="L")
    pdf.cell(21, 5, txt=semester, ln=0, align="L")
    pdf.set_font("aparaj", "", 12)
    pdf.cell(0, 5, txt=semester_student, ln=1)

    pdf.set_font("arial", "BI", 11)
    pdf.cell(18, 5, txt="", ln=0, align="L")
    pdf.cell(21, 5, txt=mention, ln=0, align="L")
    pdf.set_font("aparaj", "", 12)
    pdf.cell(100, 5, txt=mention_student, ln=0)

    pdf.set_font("arial", "BI", 11)
    pdf.cell(18, 5, txt="", ln=0, align="L")
    pdf.cell(21, 5, txt=session, ln=0, align="L")
    pdf.set_font("aparaj", "", 12)
    pdf.cell(0, 5, txt=session_student, ln=1)

    # debut de creation du tableau
    pdf.cell(30, 2, txt="", ln=1)
    pdf.set_font("arial", "I", 10)
    pdf.cell(12, 2, txt="", ln=0)

    pdf.set_fill_color(210, 210, 210)
    pdf.cell(98, 5, txt=titre_1.upper(), border=1, ln=0, align="C", fill=True)

    pdf.cell(20, 5, txt=titre_2, border=1, ln=0, align="C", fill=True)

    pdf.cell(25, 5, txt=titre_3, border=1, ln=0, align="C", fill=True)

    pdf.cell(15, 5, txt=titre_4, border=1, ln=0, align="C", fill=True)

    pdf.cell(30, 5, txt=titre_5, border=1, ln=1, align="C", fill=True)

    for index_ue, value_ue in enumerate(note["ue"]):
        pdf.set_top_margin(20)
        pdf.cell(30, 1, txt="", ln=1)
        pdf.cell(12, 2, txt="", ln=0)
        pdf.set_font("arial", "BI", 9)
        pdf.cell(
            98,
            5,
            txt=f"U.E-{index_ue + 1}: {value_ue['name']}",
            border=1,
            ln=0,
            align="C",
        )
        pdf.set_font("arial", "I", 11)
        pdf.cell(1, 1, txt="", ln=0)
        pdf.cell(19, 5, txt="", border=1, ln=0, align="C")
        pdf.cell(1, 1, txt="", ln=0)
        pdf.cell(24, 5, txt="", border=1, ln=0, align="C")
        pdf.cell(1, 1, txt="", ln=0)
        pdf.cell(14, 5, txt="", border=1, ln=0, align="C")
        pdf.cell(1, 1, txt="", ln=0)
        pdf.cell(29, 5, txt="", border=1, ln=1, align="C")
        for index, value in enumerate(value_ue["ec"]):
            pdf.set_top_margin(20)
            pdf.cell(30, 1, txt="", ln=1)
            pdf.cell(12, 2, txt="", ln=0)
            pdf.set_font("arial", "I", 9)
            pdf.cell(
                98,
                5,
                txt=f"E.C-{index + 1}: {value['name']}",
                border=1,
                ln=0,
                align="L",
            )
            pdf.set_font("arial", "I", 11)
            pdf.cell(1, 1, txt="", ln=0)
            pdf.cell(19, 5, txt=str(value["note"]) if value["note"] else "Absent", border=1, ln=0, align="C")
            pdf.cell(1, 1, txt="", ln=0)
            pdf.cell(24, 5, txt=str(value["weight"]), border=1, ln=0, align="C")
            pdf.cell(1, 1, txt="", ln=0)
            pdf.cell(14, 5, txt="", border=1, ln=0, align="C")
            pdf.cell(1, 1, txt="", ln=0)
            pdf.cell(29, 5, txt="", border=1, ln=1, align="C")
        pdf.set_top_margin(20)
        pdf.cell(30, 1, txt="", ln=1)
        pdf.cell(12, 2, txt="", ln=0)
        pdf.set_font("arial", "BI", 9)
        pdf.cell(
            98, 5, txt=f"NOTE SOUS TOTAL U.E-{index_ue + 1}", border=1, ln=0, align="C"
        )
        pdf.set_font("arial", "I", 9)
        pdf.cell(1, 1, txt="", ln=0)
        pdf.cell(
            19, 5, txt=str(format(value_ue["note"], ".2f")) if value_ue["note"] else "Absent", border=1, ln=0, align="C"
        )
        pdf.cell(1, 1, txt="", ln=0)
        pdf.cell(24, 5, txt="", border=1, ln=0, align="C")
        pdf.cell(1, 1, txt="", ln=0)
        pdf.cell(14, 5, txt=str(value_ue["credit"]), border=1, ln=0, align="C")
        pdf.cell(1, 1, txt="", ln=0)
        pdf.set_font("alger", "", 9)
        pdf.cell(
            29,
            5,
            txt=validation(value_ue["note"], data["code"]),
            border=1,
            ln=1,
            align="C",
        )

    pdf.set_top_margin(20)
    pdf.cell(30, 1, txt="", ln=1)
    pdf.cell(12, 2, txt="", ln=0)
    pdf.set_font("arial", "BI", 9)
    pdf.cell(98, 6, txt=mean.upper(), border=1, ln=0, align="C")
    pdf.set_font("arial", "I", 10)
    pdf.cell(1, 1, txt="", ln=0)
    pdf.cell(19, 6, txt=str(format(note["mean"], ".2f")), border=1, ln=0, align="C")
    pdf.cell(1, 1, txt="", ln=0)
    pdf.cell(24, 5, txt="", ln=0)
    pdf.cell(1, 1, txt="", ln=0)
    pdf.cell(14, 5, txt="", ln=0)
    pdf.cell(1, 1, txt="", ln=0)
    pdf.cell(29, 5, txt="", ln=1)

    pdf.set_font("Times", "Bui", 10)
    pdf.cell(40, 10, txt="", ln=0)
    pdf.set_font("arial", "I", 10)
    pdf.cell(130, 1, txt="", ln=1)
    pdf.cell(130, 8, txt="", ln=0)

    pdf.l_margin = 8

    logo_scolar = "images/y_scolar.png"
    logo_scolar = logo_scolar if os.path.exists(logo_scolar) else "images/no_image.png"
    pdf.image(logo_scolar, x=pdf.w - 30, y=pdf.h - 27, w=30, h=25)



class PDF(FPDF):
    def footer(self) -> None:
        self.set_y(-2)
        self.set_font("arial", "", 9)

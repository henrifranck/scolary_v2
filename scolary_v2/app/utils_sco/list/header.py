import os
from pathlib import Path

from app.pdf.PDFMark import PDFMark as FPDF
from app.db.session import SessionLocal
from app import models
from app.utils import is_begin_with_vowel


def header(pdf: FPDF, orientation: str = "P"):

    db = SessionLocal()
    university = db.query(models.University).first()
    if not university:
        db.close()
        return

    def build_asset_path(raw: str) -> str:
        if not raw:
            return "images/no_image.png"
        cleaned = str(raw).lstrip("/")
        if cleaned.startswith("../"):
            cleaned = cleaned.replace("../", "", 1)
        if cleaned.startswith("files/"):
            cleaned = cleaned[len("files/"):]
        candidate = Path("files") / cleaned
        return candidate.as_posix() if candidate.exists() else "images/no_image.png"

    logo_univ = build_asset_path(university.logo_university)
    logo_depart = build_asset_path(university.logo_departement)

    apostroth = "'"
    titre4 = f"Université d{'e ' if not is_begin_with_vowel(str(university.province)) else apostroth}{str(university.province).capitalize()} \n"
    titre5 = f"{university.department_name.upper()}"

    title6 = f"{university.department_address}"
    title7 = f"email: {university.email}-Téléphone: {university.phone_number}"

    pdf.add_font("alger", "", "font/Algerian.ttf", uni=True)

    margin = 15
    pdf.set_xy(0, 9)
    image_width = 30
    image_height = 30
    if orientation != "P":
        pdf.image(logo_univ, x=margin, y=6, w=image_width, h=image_height)
        pdf.image(logo_depart, x=pdf.w - image_width - margin, y=6, w=image_width, h=image_height)
    else:
        pdf.image(logo_univ, x=margin, y=6, w=image_width, h=image_height)
        pdf.image(logo_depart, x=pdf.w - image_width - margin, y=6, w=image_width, h=image_height)

    pdf.set_font("arial", "", 10)
    pdf.cell(0, 1, txt="", ln=1, align="C")
    pdf.cell(0, 6, txt=titre4.upper(), ln=1, align="C")
    pdf.cell(0, 6, txt=titre5, ln=1, align="C")
    pdf.set_font("arial", "", 8)
    pdf.cell(0, 5, txt=title6, ln=1, align="C")
    pdf.cell(0, 5, txt=title7, ln=1, align="C")
    db.close()

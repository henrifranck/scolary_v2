import os
import tempfile
from pathlib import Path
from typing import Any

import qrcode

from app.pdf.PDFMark import PDFMark as FPDF
from app.utils import clear_name, convert_date, is_begin_with_vowel


def create_carte(
        pdf,
        pos_init_y: int,
        long_init_y: int,
        deux_et: list,
        data: Any,
        university,
):
    center_x = pdf.w / 2
    pdf.add_font("alger", "", "font/Algerian.ttf", uni=True)

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

    def build_qr_path(num_carte: str, payload: Any) -> str:
        """Generate a QR code image on disk and return its path."""
        qr_dir = Path("files/qr_codes")
        qr_dir.mkdir(parents=True, exist_ok=True)
        filename = f"qr_{num_carte}.png"
        target = qr_dir / filename
        qr_img = qrcode.make(f"{payload}")
        qr_img.save(target, format="PNG")
        return target.as_posix()

    logo_univ = build_asset_path(university.logo_university)
    logo_depart = build_asset_path(university.logo_departement)
    signature = build_asset_path(university.admin_signature)

    apostroth = "'"
    titre_1 = f"Université d{'e ' if not is_begin_with_vowel(str(university.province)) else apostroth}{str(university.province).capitalize()} \n"
    titre_1 += f"{university.department_name} \n"
    titre_1 += f" Anné Universitaire {data['year']} \n"

    titre_2 = "Le Chef de service de scolarité:"
    titre_3 = f"{data['supperadmin']}"

    i: int = 0
    pas: int = pdf.w / 100
    pos_init_x: int = pas
    long_init_x: int = center_x - 2 * pas
    value = 25
    absci: float = 1.25 * value
    ordon: float = 0.06 * value

    i = 0
    while i < len(deux_et):
        journey = (
            deux_et[i]['name'] if len(deux_et[i]['name']) <= 25 else deux_et[i]['abbreviation']
        )
        num_carte = f"{deux_et[i]['num_carte']}"
        background = build_asset_path(data.get('img_carte', ''))
        if background == "images/no_image.png":
            background = "images/ma_avant.jpg"

        photo_value = deux_et[i].get("photo") if isinstance(deux_et[i], dict) else None
        profile = build_asset_path(photo_value) if photo_value else "images/profil.png"
        image = profile if os.path.exists(profile) else "images/profil.png"
        info = f"Nom: {clear_name(deux_et[i]['last_name'], 23).upper()}\n"
        info += f"Prénom: {clear_name(deux_et[i]['first_name'], 25).title()}\n"
        info += (
            f"Né(e) le: {convert_date(deux_et[i]['date_birth'])} à "
            f"{clear_name(deux_et[i]['place_birth'], 12).capitalize()}\n"
        )
        if deux_et[i]["num_cin"] and deux_et[i]["num_cin"] != "None":
            info += f"CIN: {deux_et[i]['num_cin']} \n"
            info += f"du {convert_date(deux_et[i]['date_cin'])} à {clear_name(deux_et[i]['place_cin'], 12).capitalize()} \n"
        info_ = f"CE: {num_carte}\n"
        student_level = (
            deux_et[i].get("level")
            if isinstance(deux_et[i], dict)
            else None
        )
        resolved_level = student_level or data.get("level", "")
        info_ += f"Parcours: {journey.upper()} | {resolved_level}\n"
        info_ += f"Mention: {data['mention']}\n"

        data_et = [deux_et[i]["num_carte"], data["key"]]
        qr_path = build_qr_path(deux_et[i]["num_carte"], data_et)

        pdf.set_font("Times", "", 8.0)

        # Positionnement symétrique des cartes
        if i == 0:
            pos_x = pos_init_x
        else:
            pos_x = center_x + pas

        pdf.image(background, x=pos_x, y=pos_init_y, w=long_init_x, h=long_init_y)
        pdf.rect(pos_x, pos_init_y, w=long_init_x, h=long_init_y)
        pdf.image(
            image,
            x=pos_x + 0.05 * value,
            y=pos_init_y + 0.7 * value,
            w=1 * value,
            h=1.18 * value,
        )
        pdf.set_text_color(0, 0, 0)

        pdf.set_font("Times", "B", 8.0)
        with pdf.local_context(fill_opacity=0.35):
            pdf.set_fill_color(255, 255, 255)
            pdf.set_xy(pos_x + absci - 1 * value, pos_init_y + ordon - 0.02 * value)
            pdf.cell(3.8 * value, 0.63 * value, txt="", border=0, fill=True, align="L")

        pdf.set_xy(pos_x + absci - 0.7 * value, pos_init_y + ordon + 0.05 * value)
        pdf.image(logo_univ, w=0.5 * value, h=0.5 * value)

        pdf.set_xy(pos_x + absci + 2 * value, pos_init_y + ordon + 0.05 * value)
        pdf.image(logo_depart, w=0.5 * value, h=0.5 * value)

        pdf.set_font("Times", "B", 9)
        pdf.set_xy(pos_x + absci - 0.35 * value, pos_init_y + ordon + 0.08 * value)
        pdf.multi_cell(
            2.5 * value,
            0.15 * value,
            titre_1.upper(),
            border=0,
            ln=0,
            fill=False,
            align="C",
        )
        pdf.ln(0.1)

        pdf.set_font("Times", "B", 7.0)
        pdf.set_xy(pos_x + absci + 0.02 * value, pos_init_y + ordon + 0.7 * value)
        pdf.multi_cell(2.16 * value, 0.15 * value, info, 0, fill=0, align="L")
        pdf.ln(0.1 * value)

        pdf.set_font("Times", "", 8.0)
        pdf.set_xy(pos_x + absci, pos_init_y + ordon + 1.5 * value)
        pdf.cell(2.5 * value, 0.15 * value, txt=titre_2, ln=1, align="L")

        pdf.set_xy(pos_x + absci + 0.4 * value, pos_init_y + ordon + 1.6 * value)
        pdf.image(signature, w=0.8 * value, h=0.6 * value)

        pdf.set_xy(pos_x + absci + 0.1 * value, pos_init_y + ordon + 2 * value)
        pdf.cell(2.5 * value, 0.15 * value, txt=titre_3, ln=0, align="L")

        pdf.set_font("Times", "", 10)
        pdf.set_fill_color(255, 255, 255)
        pdf.set_xy(pos_x + absci + 2.15 * value, pos_init_y + ordon + 1 * value)
        pdf.cell(0.6 * value, 0.4 * value, txt="", border=1, fill=True, align="L")

        pdf.set_xy(pos_x + absci + 2.1 * value, pos_init_y + ordon + 0.8 * value)
        pdf.cell(0.9 * value, 0.15 * value, txt="Signature", align="L")

        pdf.set_xy(pos_x + 0.3 * value, pos_init_y + ordon + 2 * value)
        pdf.set_font("Times", "", 9.0)
        pdf.multi_cell(3 * value, 0.15 * value, info_.title(), 0, fill=0, align="J")

        pdf.set_xy(pos_x + absci + 2.1 * value, pos_init_y + ordon + 1.5 * value)
        # pdf.cell(0.9 * value, 0.15 * value, txt=data["year"], align="L")

        pdf.set_font("Times", "B", 14.0)
        pdf.set_xy(pos_x + absci + 2.15 * value, pos_init_y + ordon + 1.85 * value)
        qr_dir = Path("files/qr_codes")
        qr_dir.mkdir(parents=True, exist_ok=True)
        qr_path = qr_dir / f"qr_{deux_et[i]['num_carte']}.png"
        qr = qrcode.make(f"{data_et}")
        qr.save(qr_path, format="PNG")
        if os.path.exists(qr_path):
            pdf.image(qr_path, w=0.6 * value, h=0.6 * value)

        pdf.set_font("Times", "BI", 9)
        pdf.set_xy(pos_x + absci + 1.9 * value, pos_init_y + ordon + 0.36 * value)
        pdf.ln(0.1 * value)

        i = i + 1



def boucle_carte(pdf, huit_student: list, data: Any, university):
    value = 25.4
    pdf.add_page()
    pos_init_y: int = pdf.w / 100
    long_init_y: float = 2.6 * value

    center_x = pdf.w / 2
    pdf.line(center_x, 0, center_x, pdf.h)
    # pdf.line(center_x / 40, 0.2, center_x / 40, pdf.h - 0.2)
    # pdf.line(pdf.w / 100, pdf.w / 100, pdf.w / 100, pdf.h - pdf.w / 100)
    # pdf.line(center_x - pdf.w / 100, 0.2, center_x - pdf.w / 100, pdf.h - 0.2)
    # pdf.line(center_x + pdf.w / 100, 0.2, center_x + pdf.w / 100, pdf.h - 0.2)
    # pdf.line(pdf.w - pdf.w / 100, 0.2, pdf.w - pdf.w / 100, pdf.h - 0.2)
    if len(huit_student) % 2 == 0:
        nbr = len(huit_student) // 2
    else:
        nbr = (len(huit_student) // 2) + 1
    n = 0
    p: int = 0
    k = 0
    while n < nbr:
        create_carte(
            pdf, pos_init_y, long_init_y, huit_student[p: p + 2], data, university
        )
        p += 2
        pos_init_y = pos_init_y + long_init_y + 2 * (pdf.w / 100)

        pdf.line(0, pos_init_y - (pdf.w / 100), pdf.w, pos_init_y - (pdf.w / 100))
        n += 1


def parcourir_et(student: list, data: Any, university):
    pdf = MyPDF("P")

    # pdf = MyPDF()
    if len(student) % 8 == 0:
        nbr = len(student) // 8
    else:
        nbr = (len(student) // 8) + 1
    k: int = 0
    l: int = 0

    while k < nbr:
        boucle_carte(pdf, student[l: l + 8], data, university)
        k += 1
        l += 8

    pdf.output(f"files/pdf/carte/card_heads_{data['mention'].replace(' ', '_')}.pdf", "F")
    return {"path": f"pdf/carte/", "filename": f"card_heads_{data['mention'].replace(' ', '_')}.pdf"}


class MyPDF(FPDF):
    def footer(self):
        # Set position for vertical line
        self.set_y(-6)

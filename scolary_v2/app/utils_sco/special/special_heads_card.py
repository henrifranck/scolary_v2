import os
from pathlib import Path
from typing import Any

import qrcode

from app.pdf.PDFMark import PDFMark as FPDF
from app.utils import clear_name, convert_date, is_begin_with_vowel, get_level_and_journey


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

    def build_asset_path(raw: str, default: str = "images/no_image.png") -> str:
        if not raw:
            return default
        cleaned = str(raw).lstrip("/")
        if cleaned.startswith("../"):
            cleaned = cleaned.replace("../", "", 1)
        if cleaned.startswith("files/"):
            cleaned = cleaned[len("files/") :]
        candidate = Path("files") / cleaned
        return candidate.as_posix() if candidate.exists() else default

    logo_univ = build_asset_path(getattr(university, "logo_university", getattr(university, "logo_univ", "")))
    logo_depart = build_asset_path(getattr(university, "logo_departement", getattr(university, "logo_depart", "")))
    signature = build_asset_path(getattr(university, "admin_signature", ""))
    apostroth = "'"
    titre_1 = f"Université d{'e ' if not is_begin_with_vowel(str(university.province)) else apostroth}{str(university.province).capitalize()} \n"
    titre_1 += f"{university.department_name} \n"

    titre_2 = "Le Chef de service de scolarité:"
    titre_3 = f"{data['supperadmin']}"

    i: int = 0
    pos_init_x: int = pdf.w / 100
    pas: int = pdf.w / 100
    long_init_x: int = center_x - 2 * (pdf.w / 100)
    value = 25.4
    absci: float = 1.25 * value
    ordon: float = 0.06 * value

    i = 0
    while i < len(deux_et):
        level = get_level_and_journey(deux_et[i]['student_year'])
        num_carte = f"{deux_et[i]['num_carte']}"

        raw_background = deux_et[i]['mention']['background_image']
        background = build_asset_path(raw_background, default="")
        if background == "" or background == "images/no_image.png":
            # Try explicit mention folder before falling back
            candidate = Path("files") / "mention" / str(raw_background).lstrip("/")
            background = candidate.as_posix() if candidate.exists() else "images/ma_avant.jpg"

        profile = build_asset_path(deux_et[i].get('photo', ''), default="images/profil.png")
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
        info_ += f"Parcours: {level[1].upper()} | {level[0].upper()}\n"
        info_ += f"Mention: {deux_et[i]['mention']['title']}\n"

        data_et = [deux_et[i]["num_carte"], data["key"]]
        qr_dir = Path("files/qr_codes")
        qr_dir.mkdir(parents=True, exist_ok=True)
        qr_path = qr_dir / f"qr_{deux_et[i]['num_carte']}.png"
        qr = qrcode.make(f"{data_et}")
        qr.save(qr_path, format="PNG")

        pdf.set_font("Times", "", 8.0)

        # pdf.image(f"images/mask.png", is_mask=True)
        pdf.image(background, x=pos_init_x, y=pos_init_y, w=long_init_x, h=long_init_y)
        # pdf.image(mask,x=pos_init_x+0.05, y=pos_init_y+0.05,w=1, is_mask=True)
        pdf.rect(pos_init_x, pos_init_y, w=long_init_x, h=long_init_y)
        pdf.image(
            image,
            x=pos_init_x + 0.05 * value,
            y=pos_init_y + 0.7 * value,
            w=1 * value,
            h=1.18 * value,
        )
        pdf.set_text_color(0, 0, 0)

        pdf.set_font("Times", "B", 8.0)
        with pdf.local_context(fill_opacity=0.35):
            pdf.set_fill_color(255, 255, 255)
            if i == 0:
                pdf.set_xy(absci - 1 * value, pos_init_y + ordon - 0.02 * value)
            else:
                pdf.set_xy(
                    absci + pos_init_x - 0.2 * value - 1 * value,
                    pos_init_y + ordon - 0.02 * value,
                )
            pdf.cell(3.8 * value, 0.63 * value, txt="", border=0, fill=True, align="L")

        if i == 0:
            pdf.set_xy(absci - 0.7 * value, pos_init_y + ordon + 0.05 * value)
        else:
            pdf.set_xy(
                absci + pos_init_x - pas - 0.7 * value,
                pos_init_y + ordon + 0.05 * value,
            )
        pdf.image(logo_univ, w=0.5 * value, h=0.5 * value)

        if i == 0:
            pdf.set_xy(absci + 2 * value, pos_init_y + ordon + 0.05 * value)
        else:
            pdf.set_xy(
                absci + pos_init_x - pas + 2 * value, pos_init_y + ordon + 0.05 * value
            )
        pdf.image(logo_depart, w=0.5 * value, h=0.5 * value)

        pdf.set_font("Times", "B", 9)
        if i == 0:
            pdf.set_xy(absci - 0.35 * value, pos_init_y + ordon + 0.08 * value)
        else:
            pdf.set_xy(
                absci + pos_init_x - pas - 0.35 * value,
                pos_init_y + ordon + 0.08 * value,
            )

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
        if i == 0:
            pdf.set_xy(absci + 0.02 * value, pos_init_y + ordon + 0.7 * value)
        else:
            pdf.set_xy(
                absci + pos_init_x - pas + 0.02 * value,
                pos_init_y + ordon + 0.7 * value,
            )

        pdf.multi_cell(2.16 * value, 0.15 * value, info, 0, fill=0, align="L")
        pdf.ln(0.1 * value)

        pdf.set_font("Times", "", 8.0)
        if i == 0:
            pdf.set_xy(absci, pos_init_y + ordon + 1.5 * value)
        else:
            pdf.set_xy(absci + pos_init_x - pas, pos_init_y + ordon + 1.5 * value)
        pdf.cell(2.5 * value, 0.15 * value, txt=titre_2, ln=1, align="L")

        if i == 0:
            pdf.set_xy(absci + 0.4 * value, pos_init_y + ordon + 1.6 * value)
        else:
            pdf.set_xy(
                absci + pos_init_x - pas + 0.4 * value, pos_init_y + ordon + 1.6 * value
            )
        pdf.image(signature, w=0.8 * value, h=0.6 * value)

        if i == 0:
            pdf.set_xy(absci + 0.1 * value, pos_init_y + ordon + 2 * value)
        else:
            pdf.set_xy(
                absci + pos_init_x - pas + 0.1 * value, pos_init_y + ordon + 2 * value
            )
        pdf.cell(2.5 * value, 0.15 * value, txt=titre_3, ln=0, align="L")

        pdf.set_font("Times", "", 10)
        pdf.set_fill_color(255, 255, 255)
        if i == 0:
            pdf.set_xy(absci + 2.15 * value, pos_init_y + ordon + 1 * value)
        else:
            pdf.set_xy(
                absci + pos_init_x - pas + 2.15 * value, pos_init_y + ordon + 1 * value
            )
        pdf.cell(0.6 * value, 0.4 * value, txt="", border=1, fill=True, align="L")

        if i == 0:
            pdf.set_xy(absci + 2.1 * value, pos_init_y + ordon + 0.8 * value)
        else:
            pdf.set_xy(
                absci + pos_init_x - pas + 2.1 * value, pos_init_y + ordon + 0.8 * value
            )
        pdf.cell(0.9 * value, 0.15 * value, txt="Signature", align="L")

        if i == 0:
            pdf.set_xy(0.3 * value, pos_init_y + ordon + 2 * value)
        else:
            pdf.set_xy(
                0.9 * value + pos_init_x - pas - 0.6 * value,
                pos_init_y + ordon + 2 * value,
            )

        pdf.set_font("Times", "", 9.0)
        pdf.multi_cell(3 * value, 0.15 * value, info_.title(), 0, fill=0, align="J")

        pdf.set_font("Times", "B", 14.0)
        if i == 0:
            pdf.set_xy(absci + 2.15 * value, pos_init_y + ordon + 1.85 * value)
        else:
            pdf.set_xy(
                absci + pos_init_x - pas + 2.15 * value,
                pos_init_y + ordon + 1.85 * value,
            )
        if os.path.exists(qr_path):
            pdf.image(qr_path, w=0.6 * value, h=0.6 * value)

        pdf.set_font("Times", "BI", 9)
        if i == 0:
            pdf.set_xy(absci + 1.9 * value, pos_init_y + ordon + 0.36 * value)
        else:
            pdf.set_xy(
                absci + pos_init_x - pas + 1.9 * value,
                pos_init_y + ordon + 0.36 * value,
            )
        # pdf.cell(1, 0.15, txt=niveau, ln=1, align="C")
        pdf.ln(0.1 * value)

        pos_init_x = center_x + pdf.w / 100
        i = i + 1


def boucle_carte(pdf, huit_etudiant: list, data: Any, university):
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
    if len(huit_etudiant) % 2 == 0:
        nbr = len(huit_etudiant) // 2
    else:
        nbr = (len(huit_etudiant) // 2) + 1
    n = 0
    p: int = 0
    k = 0
    while n < nbr:
        create_carte(
            pdf, pos_init_y, long_init_y, huit_etudiant[p : p + 2], data, university
        )
        p += 2
        pos_init_y = pos_init_y + long_init_y + 2 * (pdf.w / 100)

        pdf.line(0, pos_init_y - (pdf.w / 100), pdf.w, pos_init_y - (pdf.w / 100))
        n += 1


def parcourir_et(etudiant: list, data: Any, university):
    pdf = MyPDF("P")

    # pdf = MyPDF()
    if len(etudiant) % 8 == 0:
        nbr = len(etudiant) // 8
    else:
        nbr = (len(etudiant) // 8) + 1
    k: int = 0
    l: int = 0

    while k < nbr:
        boucle_carte(pdf, etudiant[l : l + 8], data, university)
        k += 1
        l += 8
    pdf.output(f"files/pdf/carte/special_heads_card.pdf", "F")

    return {"path": f"pdf/carte/", "filename": "special_heads_card.pdf"}


class MyPDF(FPDF):
    def footer(self):
        # Set position for vertical line
        self.set_y(-6)

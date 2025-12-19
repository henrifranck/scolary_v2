import datetime
import os
from typing import Any

import qrcode

from app.pdf.PDFMark import PDFMark as FPDF
from app.utils import clear_name, convert_date, is_begin_with_vowel


def create_badge(
        pdf,
        pos_init_y: int,
        long_init_y: int,
        two_user: Any,
        university,
):
    center_x = pdf.w / 2
    margin = 30
    pdf.add_font("alger", "", "font/Algerian.ttf", uni=True)
    file = f"files/image"
    logo_depart = f"{file}/{university.logo_depart}"
    name_depart = university.department_name
    logo_depart = logo_depart if os.path.exists(logo_depart) else "images/no_image.png"
    actual = datetime.date.today().year
    pos_init_x: int = pdf.w / margin
    long_init_x: int = center_x - 2 * (pdf.w / margin)
    value = 25.4
    ordon: float = 0.06 * value

    i = 0
    while i < len(two_user):
        profile = f"files/image/{two_user[i]['photo']}"
        image = profile if os.path.exists(profile) else f"images/profil.png"
        info = f"{clear_name(two_user[i]['last_name'], 23).upper()} {clear_name(two_user[i]['first_name'], 25).title()}"
        role = f"{two_user[i]['role']['title'].upper()}" if two_user[i]['role'] else (
            "SUPER ADMIN" if two_user[i]["is_superuser"] else "")
        identification = f"{name_depart[0]}{actual}{two_user[i]['id']}"

        pdf.set_font("Times", "", 8.0)

        if i == 0:
            background = f"images/head.png"
            pdf.image(background, x=pos_init_x, y=pos_init_y, w=long_init_x, h=long_init_y)
            pdf.rect(pos_init_x, pos_init_y, w=long_init_x, h=long_init_y)
            pdf.image(
                image,
                x=pos_init_x + pdf.w / margin + center_x / 2 - value,
                y=pos_init_y + 0.6 * value,
                w=1 * value,
                h=1 * value,
            )

            pdf.set_font("Times", "B", 14)
            pdf.set_text_color(3, 85, 84)
            pdf.set_xy(pos_init_x + pdf.w / margin + center_x / 2 - value, pos_init_y + 0.1 * value,)
            pdf.set_fill_color(255, 255, 255)
            pdf.cell(1 * value, 0.25 * value, txt=identification, border=0, fill=True, align="C")

            pdf.set_xy(0.3 * value, pos_init_y + ordon + 1.8 * value)
            pdf.set_font("Times", "I", 12)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(long_init_x, 0.25 * value, txt=info, border=0,  align="C")

            pdf.set_xy(0.3 * value, pos_init_y + ordon + 2.2 * value)
            pdf.set_font("Times", "B", 18)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(long_init_x, 0.25 * value, txt=role, border=0, align="C")

            # pdf.image(qr.get_image(), w=0.6 * value, h=0.6 * value)
            pdf.image(logo_depart,
                      x=pos_init_x + pdf.w / margin + center_x / 2 - value,
                      y=pos_init_y + long_init_y - 1 * value, w=0.9 * value, h=0.9 * value)
        else:
            background = f"images/head.png"
            pdf.image(background, x=pos_init_x, y=pos_init_y, w=long_init_x, h=long_init_y)
            pdf.rect(pos_init_x, pos_init_y, w=long_init_x, h=long_init_y)
            pdf.image(
                image,
                x=pos_init_x + pdf.w / margin + center_x / 2 - value,
                y=pos_init_y + 0.6 * value,
                w=1 * value,
                h=1 * value,
            )
            pdf.set_font("Times", "B", 14)
            pdf.set_text_color(3, 85, 84)
            pdf.set_xy(pos_init_x + pdf.w / margin + center_x / 2 - value, pos_init_y + 0.1 * value, )
            pdf.set_fill_color(255, 255, 255)
            pdf.cell(1 * value, 0.25 * value, txt=identification, border=0, fill=True, align="C")

            pdf.set_xy(pos_init_x - 0.2 * value + 0.3 * value, pos_init_y + ordon + 1.8 * value)
            pdf.set_font("Times", "I", 12)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(long_init_x, 0.25 * value, txt=info, border=0, align="C")

            pdf.set_xy(pos_init_x - 0.2 * value + 0.3 * value, pos_init_y + ordon + 2.2 * value)
            pdf.set_font("Times", "B", 18)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(long_init_x, 0.25 * value, txt=role, border=0, align="C")

            # pdf.image(qr.get_image(), w=0.6 * value, h=0.6 * value)
            pdf.image(logo_depart,
                      x=pos_init_x + pdf.w / margin + center_x / 2 - value,
                      y=pos_init_y + long_init_y - 1 * value, w=0.9 * value, h=0.9 * value)

        pdf.ln(0.1 * value)

        pos_init_x = center_x + pdf.w / margin
        i = i + 1


def boucle_carte(pdf, four_user: list, university):
    value = 35.4
    pdf.add_page()
    pos_init_y: int = pdf.w / 100
    long_init_y: float = 2.6 * value

    center_x = pdf.w / 2
    pdf.line(center_x, 0, center_x, pdf.h)
    if len(four_user) % 2 == 0:
        nbr = len(four_user) // 2
    else:
        nbr = (len(four_user) // 2) + 1

    n = 0
    p: int = 0
    k = 0
    while n < nbr:
        create_badge(
            pdf, pos_init_y, long_init_y, four_user[p: p + 2], university
        )
        p += 2
        pos_init_y = pos_init_y + long_init_y + 2 * (pdf.w / 100)

        pdf.line(0, pos_init_y - (pdf.w / 100), pdf.w, pos_init_y - (pdf.w / 100))
        n += 1


def print_badge(student: list, university):
    pdf = MyPDF("P")

    # pdf = MyPDF()
    if len(student) % 6 == 0:
        nbr = len(student) // 6
    else:
        nbr = (len(student) // 6) + 1
    k: int = 0
    l: int = 0
    while k < nbr:
        boucle_carte(pdf, student[l: l + 6], university)
        k += 1
        l += 6

    pdf.output(f"files/pdf/carte/head_badge.pdf", "F")
    return {"path": f"pdf/carte/", "filename": f"head_badge.pdf"}


class MyPDF(FPDF):
    def footer(self):
        # Set position for vertical line
        self.set_y(-2)

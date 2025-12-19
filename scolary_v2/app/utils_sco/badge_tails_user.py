import os
import datetime
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
    name_depart = university.department_name

    pos_init_x: int = pdf.w / margin
    long_init_x: int = center_x - 2 * (pdf.w / margin)
    actual = datetime.date.today().year
    value = 25.4
    ordon: float = 0.06 * value

    i = 0

    n = len(two_user)
    if n % 2 == 1:
        n += 1
        two_user = 2*two_user
    while i < n:
        identification = f"{name_depart[0]}{actual}{two_user[i]['id']}"
        qr = qrcode.make(f"{identification}")
        pdf.set_font("Times", "", 8.0)

        if i == 0:
            background = f"images/tails.png"
            pdf.image(background, x=pos_init_x, y=pos_init_y, w=long_init_x, h=long_init_y)
            pdf.set_xy(pos_init_x + pdf.w / margin + center_x / 2 - value, pos_init_y + 0.1 * value, )
            pdf.set_fill_color(3, 85, 84)

            pdf.set_font("Times", "B", 14)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(1 * value, 0.25 * value, txt=identification, border=0, fill=True, align="C")
            pdf.rect(pos_init_x, pos_init_y, w=long_init_x, h=long_init_y)
            pdf.image(qr.get_image(),
                      x=pos_init_x + pdf.w / margin + center_x / 2 - value,
                      y=pos_init_y + long_init_y - 0.95 * value, w=0.9 * value, h=0.9 * value)

            pdf.set_xy(pos_init_x, pos_init_y + ordon + 1 * value)
            pdf.set_font("Times", "BI", 20)
            pdf.set_text_color(3, 85, 84)
            pdf.cell(long_init_x, 0.25 * value, txt=name_depart, border=0, align="C")
        else:
            background = f"images/tails.png"
            pdf.image(background, x=pos_init_x, y=pos_init_y, w=long_init_x, h=long_init_y)
            pdf.set_xy(pos_init_x + pdf.w / margin + center_x / 2 - value, pos_init_y + 0.1 * value, )
            pdf.set_fill_color(3, 85, 84)

            pdf.set_font("Times", "B", 14)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(1 * value, 0.25 * value, txt=identification, border=0, fill=True, align="C")
            pdf.rect(pos_init_x, pos_init_y, w=long_init_x, h=long_init_y)
            pdf.image(qr.get_image(),
                      x=pos_init_x + pdf.w / margin + center_x / 2 - value,
                      y=pos_init_y + long_init_y - 0.95 * value, w=0.9 * value, h=0.9 * value)

            pdf.set_xy(pos_init_x, pos_init_y + ordon + 1 * value)
            pdf.set_font("Times", "BI", 20)
            pdf.set_text_color(3, 85, 84)
            pdf.cell(long_init_x, 0.25 * value, txt=name_depart, border=0, align="C")

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

    pdf.output(f"files/pdf/carte/tails_badge.pdf", "F")
    return {"path": f"pdf/carte/", "filename": f"tails_badge.pdf"}


class MyPDF(FPDF):
    def footer(self):
        # Set position for vertical line
        self.set_y(-2)

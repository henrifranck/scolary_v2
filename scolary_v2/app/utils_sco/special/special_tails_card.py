from typing import Any

from fpdf import FPDF


def create_carte(
        pdf, pos_init_y: int, long_init_y: int, deux_et: list,
):
    center_x = pdf.w / 2
    image_fac = f"images/arriere.jpg"
    # logo_univ = "images/logo_univ.jpg"
    # logo_fac = "images/logo_science.jpg"

    titre_1 = "Faculté des Sciences \n"
    titre_1 += "Visites médicale \n"
    titre_1 += "medecine préventive \n"

    titre_2 = (
        f"Null ne se présenter à l'examen s'il n'a pas subi la visite médicale organisé par le Service de "
        f"la medecine préventive, "
    )

    titre_3 = "Signature du Medecin"

    titre_4 = (
        f"NB:il n'est délivrer qu'une seule carte pendant l'année, l'interessé(e) doit faire une "
        f"déclaration auprès de la police en cas de perte. "
    )

    titre_5 = "Université \n "
    titre_5 += "de \n"
    titre_5 += "Fianarantsoa"
    i: int = 0
    pos_init_x: int = pdf.w / 100
    pas: int = pdf.w / 100
    long_init_x: int = center_x - 2 * (pdf.w / 100)
    value = 25.4
    absci: float = 1.25 * value
    ordon: float = 0.06 * value
    i = 0
    n = len(deux_et)
    if n % 2 == 1:
        n += 1
    while i < n:

        pdf.set_font("Times", "", 8)
        pdf.image(
            image_fac, x=pos_init_x, y=pos_init_y, w=long_init_x, h=long_init_y
        )
        pdf.rect(pos_init_x, pos_init_y, w=long_init_x, h=long_init_y)
        pdf.set_text_color(0, 0, 0)

        pdf.set_font("Times", "B", 10)
        if i == 0:
            pdf.set_xy(absci - 0.35 * value, pos_init_y + ordon)
        else:
            pdf.set_xy(absci + pos_init_x - pas - 0.35 * value, pos_init_y + ordon)

        pdf.multi_cell(
            2.5 * value, 0.15 * value, titre_1.upper(), border=0, ln=0, fill=False, align="C"
        )
        pdf.ln(0.1 * value)

        pdf.set_font("Times", "I", 8.0)
        if i == 0:
            pdf.set_xy(absci - 1 * value, pos_init_y + ordon + 0.6 * value)
        else:
            pdf.set_xy(absci + pos_init_x - pas - 1 * value, pos_init_y + ordon + 0.6 * value)
        pdf.multi_cell(1.8 * value, 0.15 * value, titre_2, 0, fill=0, align="C")

        if i == 0:
            pdf.set_xy(absci - 1 * value, pos_init_y + ordon + 1.3 * value)
        else:
            pdf.set_xy(absci + pos_init_x - pas - 1 * value, pos_init_y + ordon + 1.3 * value)
        pdf.cell(1.8 * value, 0.15 * value, txt=titre_3, border=0, ln=0, align="C")

        pdf.set_font("Times", "B", 7.0)
        if i == 0:
            pdf.set_xy(absci + 1.88 * value, pos_init_y + ordon + 0.8 * value)
        else:
            pdf.set_xy(absci + pos_init_x - pas + 1.88 * value, pos_init_y + ordon + 0.8 * value)
        pdf.multi_cell(1 * value, 0.13 * value, titre_5.upper(), 0, fill=0, align="C")

        pdf.set_font("Times", "I", 7.0)

        if i == 0:
            pdf.set_xy(absci - 1.05 * value, pos_init_y + ordon + 2.1 * value)
        else:
            pdf.set_xy(absci + pos_init_x - pas - 1.05 * value, pos_init_y + ordon + 2.1 * value)
        pdf.multi_cell(2.9 * value, 0.15 * value, titre_4, 0, fill=0, align="L")

        pos_init_x = center_x + pdf.w / 100
        i = i + 1


def boucle_carte(pdf, huit_etudiant: Any):
    value = 25.4
    pdf.add_page()
    pos_init_y: int = pdf.w / 100
    long_init_y: float = 2.6 * value
    center_x = pdf.w / 2
    pdf.line(center_x, 0, center_x, pdf.h)
    if len(huit_etudiant) % 2 == 0:
        nbr = len(huit_etudiant) // 2
    else:
        nbr = (len(huit_etudiant) // 2) + 1
    n = 0
    p: int = 0
    while n < nbr:
        create_carte(
            pdf, pos_init_y, long_init_y, huit_etudiant[p: p + 2],
        )
        p += 2
        pos_init_y = pos_init_y + long_init_y + 2 * (pdf.w / 100)

        pdf.line(0, pos_init_y - (pdf.w / 100), pdf.w, pos_init_y - (pdf.w / 100))
        n += 1


def parcourir_et(etudiant: list):
    pdf = MyPDF("P")
    if len(etudiant) % 8 == 0:
        nbr = len(etudiant) // 8
    else:
        nbr = (len(etudiant) // 8) + 1
    k: int = 0
    l: int = 0

    while k < nbr:
        boucle_carte(pdf, etudiant[l: l + 8])
        k += 1
        l += 8
    pdf.output(f"files/pdf/carte/special_tails_card.pdf", "F")

    return {"path": f"pdf/carte/", "filename": "special_tails_card.pdf"}


class MyPDF(FPDF):
    def footer(self):
        # Set position for vertical line
        self.set_y(-6)

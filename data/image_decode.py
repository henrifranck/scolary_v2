# pip install easyocr opencv-python numpy

import os
import re
import cv2
import numpy as np
import easyocr

def normalize_text(text: str) -> str:
    t = text.upper()
    t = t.replace("’", "'").replace("`", "'")
    t = re.sub(r"\s+", " ", t).strip()
    return t

def extract_fields(text: str) -> dict:
    res = {
        "date": None,
        "somme_mga": None,
        "nom": None,
        "numero_recu": None,
    }

    t = text.upper()
    t = t.replace("’", "'").replace("`", "'")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n+", "\n", t).strip()

    # --------------------------------------------------
    # 1) Numéro du reçu
    # OCR: N? 0324619
    # --------------------------------------------------
    m = re.search(r"\bN[\?\°O0]?\s*[:\-]?\s*(\d{5,12})\b", t)
    if m:
        res["numero_recu"] = m.group(1)

    # --------------------------------------------------
    # 2) Date (CE 06 + MAI 2017)
    # --------------------------------------------------
    mois = r"(JANVIER|FEVRIER|FÉVRIER|MARS|AVRIL|MAI|JUIN|JUILLET|AOUT|AOÛT|SEPTEMBRE|OCTOBRE|NOVEMBRE|DECEMBRE|DÉCEMBRE)"
    year_match = re.search(r"\b(19|20)\d{2}\b", t)
    year_val = year_match.group(0) if year_match else None

    # cas standard
    m = re.search(r"\b(\d{1,2})\s+(" + mois + r")\s+(\d{4})\b", t)
    if m:
        res["date"] = f"{m.group(1).zfill(2)} {m.group(2)} {m.group(3)}"
    else:
        # cas multi-ligne proche de "CE"
        m = re.search(
            r"\bCE\s+(\d{1,2})\b[\s\S]{0,40}\b(" + mois + r")\b",
            t
        )
        if m:
            suffix = year_val or ""
            res["date"] = f"{m.group(1).zfill(2)} {m.group(2)} {suffix}\".strip()"
        else:
            # OCR peut dupliquer le mois (ex: 06 MAI MAI)
            m = re.search(r"\b(\d{1,2})\s+(" + mois + r")\s+(" + mois + r")\b", t)
            if m:
                suffix = year_val or ""
                res["date"] = f"{m.group(1).zfill(2)} {m.group(2)} {suffix}\".strip()"

    # --------------------------------------------------
    # 3) Somme MGA (reconstruction métier)
    # --------------------------------------------------
    # On cherche une séquence numérique proche de MGA
    amount_match = re.search(r"([0-9][0-9 .,'`]{4,})\s*MGA", t)
    if amount_match:
        block = amount_match.group(1)
        nums = re.findall(r"\d{1,3}", block)
        if len(nums) >= 2:
            cents = None
            if len(nums[-1]) == 2:
                cents = nums[-1]
                nums = nums[:-1]
            amount = ".".join(nums)
            if cents:
                amount = f"{amount},{cents}"
            res["somme_mga"] = f"{amount} MGA"
    else:
        block_match = re.search(r"([\s\S]{0,80})MGA", t)
        if block_match:
            block = block_match.group(1)
            nums = re.findall(r"\d+", block)
            if len(nums) >= 4:
                millions = nums[-4]
                milliers = nums[-3]
                unites = nums[-2]
                centimes = nums[-1] if len(nums[-1]) == 2 else None
                amount = ".".join([millions, milliers, unites])
                if centimes:
                    amount = f"{amount},{centimes}"
                res["somme_mga"] = f"{amount} MGA"

    # --------------------------------------------------
    # 4) Nom du remettant
    # OCR: Kom du PENETTANT / NOM DU REMETTANT
    # --------------------------------------------------
    name_patterns = [
        r"NOM DU REMETTANT\s*[:\-]?\s*([A-Z'\- ]{3,})",
        r"\b(?:KOM|NOM)\s+DU\s+(?:REMETTANT|PENETTANT|PENETT?ANT)\b\s*[:\-]?\s*([A-Z'\- ]{3,})",
    ]

    for p in name_patterns:
        m = re.search(p, t)
        if m:
            name = m.group(1).strip()
            # couper si OCR colle autre chose
            name = re.split(r"\bCE\b|\bNOUS\b|\bCREDIT\b|\bCOMPTE\b", name)[0]
            res["nom"] = name.strip()
            break

    return res

def enhance_for_ocr(img_bgr: np.ndarray) -> np.ndarray:
    """Pré-traitement doux (évite de casser les lettres)."""
    # upscaling (très important si image petite)
    h, w = img_bgr.shape[:2]
    scale = 2 if max(h, w) < 1600 else 1
    if scale != 1:
        img_bgr = cv2.resize(img_bgr, (w*scale, h*scale), interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # débruitage léger + amélioration contraste
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(10, 10))
    gray = clahe.apply(gray)

    # pas de seuillage dur; on garde du gris (souvent meilleur pour EasyOCR)
    return gray

def ocr_easyocr(image_path: str, debug: bool = True) -> dict:
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image introuvable: {image_path}")

    proc = enhance_for_ocr(img)

    if debug:
        cv2.imwrite("debug_preprocessed.png", proc)

    reader = easyocr.Reader(["fr", "en"], gpu=False)

    # ✅ IMPORTANT: paragraph=False
    results = reader.readtext(proc, detail=1, paragraph=False)

    if debug:
        print("=== LIGNES OCR (texte | confiance) ===")
        for bbox, txt, conf in results:
            print(f"{txt} | {conf:.2f}")

    full_text = "\n".join([txt for _, txt, _ in results])
    fields = extract_fields(full_text)

    return {
        "fields": fields,
        "raw_text": full_text
    }

if __name__ == "__main__":
    image_path = os.path.join(os.path.dirname(__file__), "recu.png")
    out = ocr_easyocr(image_path, debug=True)
    print("\n=== TEXTE OCR ===")
    print(out["raw_text"])
    print("\n=== CHAMPS ===")
    for k, v in out["fields"].items():
        print(f"{k}: {v}")
    print("\n--- Image prétraitée sauvegardée: debug_preprocessed.png ---")

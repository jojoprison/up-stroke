import cv2
import os
import re

import numpy as np
import pytesseract
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

# === Берём все .jpg ===
image_files = sorted([f for f in os.listdir('.') if f.lower().endswith('.jpg')])
output_pdf = "GAT_TextOCR_Final.pdf"


# === Выравнивание и чистка изображения ===
def deskew_and_clean(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    # порог
    _, th = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # инверсия (текст чёрный)
    th = cv2.bitwise_not(th)

    # выравнивание (deskew)
    coords = np.column_stack(np.where(th > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = img.shape[:2]
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC,
                             borderMode=cv2.BORDER_REPLICATE)

    # фильтры для подчёркиваний и текста
    rotated = cv2.medianBlur(rotated, 3)
    rotated = cv2.adaptiveThreshold(rotated, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 25, 15)
    rotated = cv2.bitwise_not(rotated)
    return rotated


# === OCR + фиксация подчёркиваний ===
def ocr_with_cleanup(img_path):
    img = deskew_and_clean(img_path)
    config = "--oem 1 --psm 4 -c preserve_interword_spaces=1"
    text = pytesseract.image_to_string(img, lang="eng", config=config)

    # подчёркивания
    underline_pass = pytesseract.image_to_string(
        img, lang="eng", config="--psm 6 -c tessedit_char_whitelist=_"
    )
    if underline_pass.count("_") > text.count("_"):
        text += "\n" + underline_pass

    # чистим OCR мусор
    text = (
        text.replace("|", "l")
        .replace("°", "o")
        .replace("~", "-")
        .replace("‘", "'")
        .replace("’", "'")
        .replace("`", "'")
    )

    # заменяем кривые пробелы
    text = re.sub(r"\s{2,}", " ", text)
    # восстанавливаем разорванные подчёркивания
    text = re.sub(r"(_\s_)+", "_____", text)
    text = re.sub(r"-{3,}", "_____", text)
    text = re.sub(r"_{2,}", "_____", text)

    # убираем обрывочные строки, если в них мало букв
    lines = []
    for ln in text.splitlines():
        if not ln.strip():
            continue
        if len(ln.strip()) < 2 and not "_" in ln:
            continue
        lines.append(ln.strip())
    return "\n".join(lines)


# === Создание PDF ===
def make_text_pdf(pages_text, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    w, h = A4
    margin_x, margin_y = 20 * mm, 20 * mm
    line_height = 13
    c.setFont("Helvetica", 11)

    for page_idx, text in enumerate(pages_text, start=1):
        y = h - margin_y
        for line in text.splitlines():
            if not line.strip():
                y -= line_height
                continue
            if y < margin_y:
                c.showPage()
                c.setFont("Helvetica", 11)
                y = h - margin_y
            c.drawString(margin_x, y, line)
            y -= line_height
        if page_idx < len(pages_text):
            c.showPage()
    c.save()
    print(f"✅ Готово: {os.path.abspath(output_path)}")


# === Основной процесс ===
all_text = []
for idx, path in enumerate(image_files, start=1):
    print(f"OCR страницы {idx}: {path}")
    try:
        txt = ocr_with_cleanup(path)
    except Exception as e:
        txt = f"[Ошибка OCR: {e}]"
    all_text.append(txt)

make_text_pdf(all_text, output_pdf)

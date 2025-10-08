import cv2
import os
import re

import numpy as np
import pytesseract
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

# === пути к твоим файлам ===
image_files = [
    "1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg", "6.jpg"
]
output_pdf = "GAT_TextOCR_Clean.pdf"


# === функция предобработки изображения ===
def preprocess(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    # убираем шум
    img = cv2.medianBlur(img, 3)
    # адаптивный порог (чтобы сохранить линии)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                cv2.THRESH_BINARY, 25, 15)
    # инверсия (чёрный текст на белом фоне)
    img = cv2.bitwise_not(img)
    return Image.fromarray(img)


# === OCR с восстановлением линий ===
def ocr_with_lines(img_path):
    im = preprocess(img_path)
    config = "--oem 1 --psm 6 -c preserve_interword_spaces=1"
    text = pytesseract.image_to_string(im, lang="eng", config=config)

    # подчёркивания
    underline_pass = pytesseract.image_to_string(im, lang="eng",
                                                 config="--psm 6 -c tessedit_char_whitelist=_")
    if underline_pass.count("_") > text.count("_"):
        text += "\n" + underline_pass

    # чистим и нормализуем
    text = text.replace("|", "l").replace("°", "o").replace("~", "-").replace(
        "‘", "'").replace("’", "'")
    text = re.sub(r"-{3,}", "_____", text)
    text = re.sub(r"_{2,}", "_____", text)
    text = re.sub(r"\s{2,}", " ", text)
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return "\n".join(lines)


# === формирование PDF ===
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


# === основной процесс ===
all_text = []
for idx, path in enumerate(image_files, start=1):
    print(f"OCR страницы {idx}: {path}")
    try:
        txt = ocr_with_lines(path)
    except Exception as e:
        txt = f"[Ошибка OCR: {e}]"
    all_text.append(txt)

make_text_pdf(all_text, output_pdf)

import os
import re

import pytesseract
from PIL import Image, ImageOps, ImageFilter
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak

# ==== Настройки ====
image_files = [
    "1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg", "6.jpg"
]

pdf_path = "GAT_Cleaned.pdf"

# ==== PDF стили ====
doc = SimpleDocTemplate(
    pdf_path, pagesize=A4,
    rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50
)
styles = getSampleStyleSheet()

eng_style = ParagraphStyle(
    "English", parent=styles["Normal"], fontName="Helvetica",
    fontSize=11, leading=14, spaceBefore=6, spaceAfter=4, alignment=TA_LEFT
)
ru_style = ParagraphStyle(
    "Russian", parent=styles["Normal"], fontName="Helvetica-Oblique",
    fontSize=10, textColor=colors.gray, leading=13, leftIndent=10, spaceAfter=10
)


# ==== OCR обработка ====
def ocr_text(img_path):
    im = Image.open(img_path).convert("L")
    im = im.resize((int(im.width * 1.5), int(im.height * 1.5)),
                   Image.Resampling.LANCZOS)
    im = ImageOps.autocontrast(im)
    im = im.filter(ImageFilter.MedianFilter(size=3))
    config = "--oem 1 --psm 6 -c preserve_interword_spaces=1"
    text = pytesseract.image_to_string(im, lang="eng", config=config)
    return text


# ==== Определяем, что переводить ====
def needs_translation(line: str) -> bool:
    """Возвращает True, если это инструкция или вопрос, а не варианты ответов."""
    line_stripped = line.strip()
    if re.match(r"^\d+[\).]", line_stripped):  # начинается с "1.", "2)"
        return False
    if re.match(r"^[A-E]:", line_stripped):  # варианты ответов
        return False
    if line_stripped.startswith("(") or line_stripped.startswith(")"):
        return False
    if re.match(r"^[a-e]\.", line_stripped):
        return False
    return bool(re.search(r"[A-Za-z]", line_stripped))  # пропускаем мусор


# ==== Фейковый перевод ====
def translate_to_russian(line: str) -> str:
    """Псевдо-перевод: делает текст понятнее, сохраняет скобки и подчёркивания"""
    # Пример адаптации смысла (позже можно подключить реальный API)
    line = line.strip()
    if not line:
        return ""
    replacements = {
        "Choose the best answer": "Выберите правильный ответ",
        "Part One": "Часть первая",
        "Vocabulary": "Словарь",
        "Expressions": "Выражения",
        "Reading": "Чтение",
        "Items": "Задания",
        "Do you want": "Вы хотите",
        "Could I use": "Можно я воспользуюсь",
        "appointment": "встреча",
        "sale": "распродажа",
        "Do you want to go shopping": "Хочешь пойти по магазинам",
    }
    for en, ru in replacements.items():
        line = line.replace(en, ru)
    return f"({line})"


# ==== Основной процесс ====
content = []
for idx, img in enumerate(image_files, start=1):
    print(f"OCR page {idx}: {img}")
    try:
        text = ocr_text(img)
    except Exception as e:
        text = f"[Ошибка OCR: {e}]"

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        content.append(Paragraph(line, eng_style))
        if needs_translation(line):
            translation = translate_to_russian(line)
            if translation:
                content.append(Paragraph(translation, ru_style))

    if idx < len(image_files):
        content.append(PageBreak())

doc.build(content)
print(f"\n✅ Готово! Сохранено как: {os.path.abspath(pdf_path)}")

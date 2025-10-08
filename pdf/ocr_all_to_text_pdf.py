import os
import re
from pathlib import Path
from typing import List

import pytesseract
from PIL import Image, ImageOps, ImageFilter
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
# Собираем все .jpg рядом со скриптом
BASE_DIR = Path(__file__).parent
image_files: List[Path] = sorted(
    [p for p in BASE_DIR.iterdir() if p.suffix.lower() == ".jpg"],
    key=lambda p: [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", p.name)],
)
output_pdf = BASE_DIR / "GAT_TextOnly.pdf"


def preprocess(img_path: str) -> Image.Image:
    """Минимальная предобработка без выравнивания наклона.
    Сохраняем максимально исходную разметку, слегка повышая читаемость для OCR."""
    im = Image.open(img_path).convert("L")
    # Лёгкое увеличение, автоконтраст и медианный фильтр для снижения шума
    im = im.resize((int(im.width * 1.3), int(im.height * 1.3)), Image.Resampling.LANCZOS)
    im = ImageOps.autocontrast(im)
    im = im.filter(ImageFilter.MedianFilter(size=3))
    return im


def ocr_text(img_path: str) -> str:
    im = preprocess(img_path)
    config = "--oem 1 --psm 6 -c preserve_interword_spaces=1"
    text = pytesseract.image_to_string(im, lang="eng", config=config)

    # Небольшая чистка артефактов OCR, не ломая разметку строк
        text.replace("|", "l")
            .replace("°", "o")
            .replace("~", "-")
            .replace("‘", "'")
            .replace("’", "'")
    )
        .replace("’", "'")
    # Сохраняем пустые строки как разделители абзацев
    lines = [ln.rstrip() for ln in text.splitlines()]
    return "\n".join(lines)


    def make_text_pdf(pages_text: List[str], output_path: str) -> None:
    c = canvas.Canvas(output_path, pagesize=A4)
    w, h = A4
    margin_x, margin_y = 20 * mm, 20 * mm
    line_height = 14
    c.setFont("Courier", 11)

        for page_idx, text in enumerate(pages_text, start=1):
            for line in text.splitlines():
                if line.strip() == "":
                    y -= line_height
                    continue
                c.setFont("Courier", 11)
                c.drawString(margin_x, y, line)
                y -= line_height
            c.showPage()
    c.save()
{{ ... }}
    print(f"✅ Готово: {Path(output_path).resolve()}")


if __name__ == "__main__":
    if not image_files:
        print("Не найдено .jpg в текущем каталоге.")
        raise SystemExit(1)

    all_text: List[str] = []
    for idx, path in enumerate(image_files, start=1):
        print(f"OCR страницы {idx}: {path.name}")
        try:
            txt = ocr_text(path)
        except Exception as e:
            txt = f"[Ошибка OCR: {e}]"
        all_text.append(txt)

    make_text_pdf(all_text, str(output_pdf))

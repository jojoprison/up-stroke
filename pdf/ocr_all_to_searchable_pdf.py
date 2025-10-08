import argparse
import re
from pathlib import Path
from typing import List

import cv2
import numpy as np
import pytesseract
from PIL import Image

# Попытка определить путь к бинарнику tesseract на macOS/Homebrew и Linux
_TESSERACT_CANDIDATES = [
    "/opt/homebrew/bin/tesseract",  # Apple Silicon brew
    "/usr/local/bin/tesseract",  # Intel macOS brew
    "/usr/bin/tesseract",  # Linux
]
for _cmd in _TESSERACT_CANDIDATES:
    if Path(_cmd).exists():
        pytesseract.pytesseract.tesseract_cmd = _cmd
        break


def _natural_key(name: str):
    # Естественная сортировка: '10.jpg' после '9.jpg'
    return [int(t) if t.isdigit() else t.lower() for t in
            re.split(r"(\d+)", name)]


def find_jpgs(base_dir: Path) -> List[Path]:
    files = [p for p in base_dir.iterdir() if p.suffix.lower() == ".jpg"]
    files.sort(key=lambda p: _natural_key(p.name))
    return files


def compute_deskew_angle(gray: np.ndarray) -> float:
    # Binarize + invert for text foreground
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    th = cv2.bitwise_not(th)
    coords = cv2.findNonZero(th)
    if coords is None or len(coords) == 0:
        return 0.0
    rect = cv2.minAreaRect(coords)
    angle = rect[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    # Ограничим неожиданные углы
    angle = float(max(min(angle, 20.0), -20.0))
    return angle


def rotate_image_keep_size(image: np.ndarray, angle: float) -> np.ndarray:
    if abs(angle) < 0.1:
        return image
    (h, w) = image.shape[:2]
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC,
                             borderMode=cv2.BORDER_REPLICATE)
    return rotated


def to_pdf_page(img_bgr: np.ndarray, lang: str, psm: str, oem: str) -> bytes:
    # Конвертация BGR (OpenCV) -> RGB (Pillow)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    config = f"--oem {oem} --psm {psm}"
    pdf_bytes = pytesseract.image_to_pdf_or_hocr(pil_img, lang=lang,
                                                 config=config, extension="pdf")
    return pdf_bytes


def merge_pdfs(page_files: List[Path], out_path: Path) -> None:
    writer = None
    try:
        from pypdf import PdfWriter, PdfReader  # type: ignore
        writer = PdfWriter()
        for pf in page_files:
            reader = PdfReader(str(pf))
            for page in reader.pages:
                writer.add_page(page)
        with out_path.open("wb") as f:
            writer.write(f)
        return
    except Exception:
        pass

    try:
        from PyPDF2 import PdfWriter, PdfReader  # type: ignore
        writer = PdfWriter()
        for pf in page_files:
            reader = PdfReader(str(pf))
            for page in reader.pages:
                writer.add_page(page)
        with out_path.open("wb") as f:
            writer.write(f)
        return
    except Exception as e:
        raise RuntimeError(
            "Не удалось импортировать pypdf/PyPDF2 для объединения PDF. "
            "Установите один из пакетов: 'pypdf' (предпочтительно) или 'PyPDF2'.\n"
            f"Исключение: {e}"
        )


def build_searchable_pdf(images: List[Path], out_pdf: Path, lang: str = "eng",
                         psm: str = "6", oem: str = "1") -> Path:
    tmp_dir = out_pdf.parent / "_ocr_pages"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    # Очистим только наши временные файлы
    for old in tmp_dir.glob("page_*.pdf"):
        try:
            old.unlink()
        except Exception:
            pass

    page_files: List[Path] = []

    for i, img_path in enumerate(images, start=1):
        print(f"[OCR] Страница {i}/{len(images)}: {img_path.name}")
        # 1) Читаем оригинал и считаем угол на градациях серого
        bgr = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
        if bgr is None:
            print(f"  ⚠️ Пропуск: не удалось открыть {img_path}")
            continue
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        angle = compute_deskew_angle(gray)
        if abs(angle) > 0.1:
            bgr = rotate_image_keep_size(bgr, angle)
            print(f"  ↺ Исправлен наклон: {angle:.2f}°")
        # 2) Генерим PDF-страницу с текстовым слоем
        try:
            pdf_bytes = to_pdf_page(bgr, lang=lang, psm=psm, oem=oem)
        except Exception as e:
            print(f"  ❌ Ошибка OCR: {e}")
            continue
        page_file = tmp_dir / f"page_{i:03d}.pdf"
        with page_file.open("wb") as f:
            f.write(pdf_bytes)
        page_files.append(page_file)

    if not page_files:
        raise RuntimeError("Не удалось сформировать ни одной PDF-страницы")

    print(f"[MERGE] Объединение {len(page_files)} страниц в {out_pdf.name}…")
    merge_pdfs(page_files, out_pdf)
    print(f"✅ Готово: {out_pdf.resolve()}")
    return out_pdf


def main():
    parser = argparse.ArgumentParser(
        description="OCR всех .jpg в каталоге скрипта в один поисковый PDF (слой текста поверх изображения)")
    parser.add_argument("--lang", default="eng",
                        help="Языки Tesseract, например: eng или eng+rus")
    parser.add_argument("--psm", default="6",
                        help="Page segmentation mode, напр.: 4, 6, 11")
    parser.add_argument("--oem", default="1",
                        help="OCR Engine Mode (0: Legacy, 1: LSTM, 2: Legacy+LSTM, 3: Default)")
    parser.add_argument("--out", default="GAT_Searchable.pdf",
                        help="Имя выходного PDF")
    args = parser.parse_args()

    base_dir = Path(__file__).parent
    images = find_jpgs(base_dir)
    if not images:
        print("Не найдено .jpg рядом со скриптом")
        return

    out_pdf = base_dir / args.out
    build_searchable_pdf(images, out_pdf, lang=args.lang, psm=args.psm,
                         oem=args.oem)


if __name__ == "__main__":
    main()

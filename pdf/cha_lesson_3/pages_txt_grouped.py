import sys
from pathlib import Path
from typing import List

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

# Импортируем тексты из соседнего файла с пунктуацией
BASE_DIR = Path(__file__).parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from pages_txt_fixed import part_1, part_2, part_3, part_4, part_5, part_6, \
    part_7  # type: ignore


def split_part4(p4: str) -> tuple[str, str]:
    """Разделить блок part_4 на:
    - 9–12 (варианты)
    - 13–15 (диалог и варианты)
    По маркеру строки '13-15'.
    """
    marker = "\n13-15"
    idx = p4.find(marker)
    if idx == -1:
        return p4, ""
    p4_9_12 = p4[:idx].rstrip()
    p4_13_15 = p4[
        idx + 1:].lstrip()  # сохраняем заголовок '13-15' в начале второй части
    return p4_9_12, p4_13_15


def make_text_pdf(blocks: List[str], out_path: Path) -> Path:
    c = canvas.Canvas(str(out_path), pagesize=A4)
    w, h = A4
    margin_x, margin_y = 20 * mm, 20 * mm
    line_height = 14
    c.setFont("Courier", 11)

    for i, block in enumerate(blocks, start=1):
        y = h - margin_y
        for line in block.splitlines():
            if line.strip() == "":
                y -= line_height
                if y < margin_y:
                    c.showPage();
                    c.setFont("Courier", 11);
                    y = h - margin_y
                continue
            if y < margin_y:
                c.showPage();
                c.setFont("Courier", 11);
                y = h - margin_y
            c.drawString(margin_x, y, line)
            y -= line_height
        if i < len(blocks):
            c.showPage();
            c.setFont("Courier", 11)
    c.save()
    return out_path


if __name__ == "__main__":
    p4_9_12, p4_13_15 = split_part4(part_4)

    # Страницы по требованию:
    # 1) 1-4 на одной
    page_1 = part_1.strip("\n")
    # 2) 5-8 на следующей
    page_2 = part_2.strip("\n")
    # 3) 9-12 (диалог + варианты) на следующей
    page_3 = (part_3.strip("\n") + "\n\n" + p4_9_12.strip("\n")).strip("\n")
    # 4) 13-15 на следующей
    page_4 = p4_13_15.strip("\n") if p4_13_15 else ""

    # Далее — остальное сплошником, каждый блок с новой страницы
    other_blocks = [part_5, part_6, part_7]

    blocks: List[str] = [page_1, page_2, page_3]
    if page_4:
        blocks.append(page_4)
    blocks.extend([b.strip("\n") for b in other_blocks])

    out_pdf = BASE_DIR / "CHA_Lesson_3_Text_grouped.pdf"
    make_text_pdf(blocks, out_pdf)
    print(f"✅ Готово: {out_pdf.resolve()}")

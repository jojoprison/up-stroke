import re
import sys
import textwrap
from pathlib import Path
from typing import List

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
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


def make_text_pdf(blocks: List[str], out_path: Path,
                  break_before: list[list[str]] | None = None) -> Path:
    c = canvas.Canvas(str(out_path), pagesize=A4)
    w, h = A4
    margin_x, margin_y = 20 * mm, 20 * mm
    line_height = 14
    c.setFont("Courier", 11)
    # рассчитаем максимально допустимое количество символов в строке для правого отступа
    char_w = pdfmetrics.stringWidth("M", "Courier", 11)
    max_width = w - 2 * margin_x
    max_chars = max(1, int(max_width // char_w))
    # Компилируем правила ручных переносов страниц до строк
    comp_breaks: list[list[re.Pattern]] = []
    if break_before is None:
        comp_breaks = [[] for _ in blocks]
    else:
        comp_breaks = [[re.compile(p) for p in group] for group in break_before]

    # Карта подчёркиваний для заданий 26-30.
    # В вопросе: подчёркивание + полужирный; в вариантах: только подчёркивание.
    underline_patterns_map = {
        "26": [r"handle(?:d)?"],
        "27": [r"position"],
        "28": [r"active"],
        "29": [r"learn(?:ed)?"],
        "30": [r"currents?"],
    }
    compiled_ul = {k: [re.compile(rf"\\b{p}\\b", re.IGNORECASE) for p in v] for
                   k, v in underline_patterns_map.items()}

    def wrap_with_indices(text: str, width: int) -> list[tuple[str, int]]:
        wrapped = textwrap.wrap(text, width=width, break_long_words=True,
                                break_on_hyphens=False)
        segs: list[tuple[str, int]] = []
        cursor = 0
        for seg in wrapped:
            start = text.find(seg, cursor)
            if start == -1:
                start = cursor
            segs.append((seg, start))
            cursor = start + len(seg)
        if not segs:
            segs.append(("", 0))
        return segs

    def draw_with_optional_underline(base_x: float, y_pos: float,
                                     full_line: str, seg_text: str,
                                     seg_start: int,
                                     underline_pats: list[re.Pattern],
                                     bold_on_matches: bool):
        # отрисуем сегмент обычным шрифтом
        c.setFont("Courier", 11)
        c.drawString(base_x, y_pos, seg_text)
        if not underline_pats:
            return
        # найдем диапазоны в полной строке
        ranges: list[tuple[int, int]] = []
        for pat in underline_pats:
            for m in pat.finditer(full_line):
                ranges.append((m.start(), m.end()))
        if not ranges:
            return
        seg_end = seg_start + len(seg_text)
        for a, b in ranges:
            # пересечение с текущим сегментом
            start = max(a, seg_start)
            end = min(b, seg_end)
            if start >= end:
                continue
            rel_start = start - seg_start
            rel_end = end - seg_start
            x1 = base_x + rel_start * char_w
            x2 = base_x + rel_end * char_w
            c.setLineWidth(0.6)
            c.line(x1, y_pos - 1.5, x2, y_pos - 1.5)
            if bold_on_matches:
                # нарисуем поверх выделенный фрагмент полужирным
                c.setFont("Courier-Bold", 11)
                c.drawString(x1, y_pos, seg_text[rel_start:rel_end])
                c.setFont("Courier", 11)

    for i, block in enumerate(blocks, start=1):
        y = h - margin_y
        current_item: str | None = None  # для part_7 (26-30)
        for line in block.splitlines():
            if line.strip() == "":
                y -= line_height
                if y < margin_y:
                    c.showPage();
                    c.setFont("Courier", 11);
                    y = h - margin_y
                continue
            # Ручной перенос страницы перед заданной строкой (например, перед "21.")
            if comp_breaks[i - 1] and any(p.match(line) for p in comp_breaks[
                i - 1]) and y != h - margin_y:
                c.showPage();
                c.setFont("Courier", 11);
                y = h - margin_y

            # Определим подчёркивание/полужирный для part_7 (26-30)
            underline_pats: list[re.Pattern] = []
            bold_on_matches = False
            if i == len(blocks):  # последний блок = part_7
                m_item = re.match(r"\s*(\d{2})\.", line)
                if m_item:
                    current_item = m_item.group(1)
                    if current_item in compiled_ul:
                        underline_pats = compiled_ul[current_item]
                        bold_on_matches = True  # в строке вопроса — полужирный
                else:
                    if current_item and re.match(r"\s*[1-5]\.",
                                                 line) and current_item in compiled_ul:
                        underline_pats = compiled_ul[
                            current_item]  # в вариантах — только подчёрк.
                        bold_on_matches = False

            # перенос по правому краю с тем же отступом, используя моноширинный шрифт
            wrapped_with_idx = wrap_with_indices(line, max_chars)
            for seg_text, seg_start in wrapped_with_idx:
                if y < margin_y:
                    c.showPage();
                    c.setFont("Courier", 11);
                    y = h - margin_y
                draw_with_optional_underline(margin_x, y, line, seg_text,
                                             seg_start, underline_pats,
                                             bold_on_matches)
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

    # Далее — остальное: объединяем 16–25 (part_5 + part_6) в один блок
    # и делаем ручной разрыв страницы перед 21., чтобы 21 начиналось с новой страницы,
    # а 22 и далее шли на той же странице
    combined_16_25 = (part_5.strip("\n") + "\n" + part_6.strip("\n")).strip(
        "\n")

    blocks: List[str] = [page_1, page_2, page_3]
    if page_4:
        blocks.append(page_4)
    blocks.append(combined_16_25)
    blocks.append(part_7.strip("\n"))

    out_pdf = BASE_DIR / "CHA_Lesson_3_Text_final.pdf"
    break_rules = [[] for _ in blocks]
    combined_idx = len(blocks) - 2  # позиция combined_16_25
    break_rules[combined_idx] = [r"\s*21\."]
    make_text_pdf(blocks, out_pdf, break_rules)
    print(f"✅ Готово: {out_pdf.resolve()}")

"""
Слияние пересекающихся интервалов.

Сложность:
- Время: O(n log n) — сортировка + линейный проход.
- Память: O(n) — на хранение отсортированного списка/результата (если считать выход).

Подсказки:
- Отсортируй по началу, при равенстве — по концу: `sorted(intervals, key=lambda x: (x[0], x[1]))`.
- Сливай, если `l <= cur_r` (для включительных границ). Для строгих границ используй `l < cur_r`.
- Обрабатывай пустой вход и одиночные интервалы отдельно (возврати исходное/пустое).

Подводные камни:
- определитесь с моделью границ (включительная/исключительная). Здесь — включительная [l, r],
- пустой вход, одиночные интервалы,
- порядок сортировки: сначала по началу, затем по концу,
- большие числа и отрицательные значения — это ок.
"""
from typing import List, Tuple

Interval = Tuple[int, int]


def merge_intervals(intervals: List[Interval]) -> List[Interval]:
    if not intervals:
        return []
    intervals = sorted(intervals, key=lambda x: (x[0], x[1]))
    merged: List[Interval] = []
    cur_l, cur_r = intervals[0]
    for l, r in intervals[1:]:
        if l <= cur_r:  # пересечение или касание
            if r > cur_r:
                cur_r = r
        else:
            merged.append((cur_l, cur_r))
            cur_l, cur_r = l, r
    merged.append((cur_l, cur_r))
    return merged


if __name__ == "__main__":
    print(merge_intervals([(1, 3), (2, 6), (8, 10), (15, 18)]))  # [(1, 6), (8, 10), (15, 18)]
    print(merge_intervals([(1, 4), (4, 5)]))                      # [(1, 5)] — включительные границы

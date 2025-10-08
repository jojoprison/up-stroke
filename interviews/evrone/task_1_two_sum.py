"""
Two Sum — вернуть индексы (i, j), такие что nums[i] + nums[j] == target.

Сложность:
- Время: O(n) — один линейный проход по массиву.
- Память: O(n) — словарь value->index для уже просмотренных элементов.

Подсказки:
- Сначала проверяй комплимент (target - x) в словаре, потом добавляй текущий x.
- Аккуратно с дубликатами: обновляй словарь после проверки.
- Для float лучше избегать неточной суммы; тестируй на int.

Подводные камни:
- дубликаты (важен порядок: сначала ищем пару, затем кладём текущий элемент),
- самосуммирование, float-точность (лучше тестировать на int),
- если решений несколько — возвращаем первое найденное.
"""
from typing import List, Optional, Tuple


def two_sum(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    index_by_value = {}
    for j, x in enumerate(nums):
        need = target - x
        if need in index_by_value:
            return index_by_value[need], j
        index_by_value[x] = j
    return None


if __name__ == "__main__":
    print(two_sum([2, 7, 11, 15], 9))      # (0, 1)
    print(two_sum([3, 2, 4], 6))           # (1, 2)
    print(two_sum([3, 3], 6))              # (0, 1)

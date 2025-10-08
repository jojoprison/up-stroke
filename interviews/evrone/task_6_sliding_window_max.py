"""
Максимум в скользящем окне размера k (deque, O(n)).

Сложность:
- Время: O(n) — каждый индекс добавляется/удаляется из deque не более одного раза.
- Память: O(k) — размер deque ограничен шириной окна.

Подсказки:
- Храни индексы в deque по невозрастающим значениям (голова — максимум).
- Перед добавлением нового индекса удаляй из хвоста все индексы с меньшими/равными значениями.
- Удаляй из головы индексы, вышедшие из окна (i - k).

Подводные камни:
- k <= 0 или k > len(nums) — ошибка,
- хранить индексы, а не значения, вычищать вышедшие из окна и меньшие с хвоста.
"""
from collections import deque
from typing import List


def sliding_window_max(nums: List[int], k: int) -> List[int]:
    n = len(nums)
    if k <= 0 or k > n:
        raise ValueError("k must be in 1..len(nums)")
    dq = deque()  # индексы кандидатов, значения по убыванию
    out: List[int] = []
    for i, x in enumerate(nums):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out


if __name__ == "__main__":
    print(sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3))  # [3, 3, 5, 5, 6, 7]

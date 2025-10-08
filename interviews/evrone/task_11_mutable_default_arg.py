"""
Mutable default arguments — классическая ловушка в Python.

Сложность:
- Время: O(1) на добавление элемента.
- Память: O(n) суммарно по числу добавлений в один и тот же общий список (в баговом варианте).

Подсказки:
- Никогда не ставь мутируемые значения в дефолтах аргументов.
- Шаблон: `def f(x=None): x = [] if x is None else x`.
- Если нужно кэширование по умолчанию — используй `functools.lru_cache` или явные структуры вне сигнатуры.

Подводные камни:
- значение по умолчанию вычисляется один раз при определении функции,
- общий список/словарь будет «копиться» между вызовами,
- корректный приём: использовать None и создавать новый объект внутри.
"""
from typing import List, Optional


def append_item_bug(item: int, bucket: List[int] = []) -> List[int]:  # noqa: B006 — специально демонстрируем баг
    """Ошибка: общее значение по умолчанию.
    При многократных вызовах элементы будут накапливаться в одном и том же списке.
    """
    bucket.append(item)
    return bucket


def append_item_ok(item: int, bucket: Optional[List[int]] = None) -> List[int]:
    """Правильный вариант: ленивое создание нового списка.
    """
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


if __name__ == "__main__":
    print(append_item_bug(1))  # [1]
    print(append_item_bug(2))  # [1, 2] — неожиданно для вызвавшего

    print(append_item_ok(1))   # [1]
    print(append_item_ok(2))   # [2]
    print(append_item_ok(3, [10]))  # [10, 3]

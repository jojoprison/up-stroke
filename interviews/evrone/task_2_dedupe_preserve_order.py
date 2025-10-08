"""
Удаление дубликатов с сохранением порядка.

Сложность:
- Время: O(n) — один проход по последовательности.
- Память: O(n) — множество увиденных ключей и выходной список.

Подсказки:
- Используй `seen = set()` и проверяй ключ до добавления в выход.
- Для неhashable элементов передай `key`, стабилизирующий объект в hashable (например, `tuple(sorted(d.items()))`).
- Если нужен генератор без промежуточного списка — можно сделать `yield`‑вариант и при необходимости оборачивать в `list(...)`.

Подводные камни:
- неhashable элементы (dict, list) — используйте `key` для преобразования к hashable,
- объём памяти для больших коллекций,
- стабильность порядка — сохраняем первый встретившийся.
"""
from typing import Callable, Hashable, Iterable, List, Optional, TypeVar

T = TypeVar("T")
K = TypeVar("K", bound=Hashable)


def dedupe(seq: Iterable[T], key: Optional[Callable[[T], K]] = None) -> List[T]:
    seen = set()
    out: List[T] = []
    for item in seq:
        k = key(item) if key else item
        if k not in seen:
            seen.add(k)
            out.append(item)
    return out


if __name__ == "__main__":
    print(dedupe([1, 1, 2, 3, 2, 4]))
    dicts = [{"a": 1}, {"a": 1}, {"a": 2}]
    # стабилизуем dict в кортеж отсортированных пар
    print(dedupe(dicts, key=lambda d: tuple(sorted(d.items()))))

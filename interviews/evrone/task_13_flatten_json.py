"""
Flatten nested dict/list в плоский dict с составными ключами.

Сложность:
- Время: O(N) — каждый узел посещается один раз (N = кол-во скаляров/контейнеров).
- Память: O(N) — размер выходного словаря + O(D) стек рекурсии (D = глубина вложенности).

Подсказки:
- Формируй ключи через `f"{prefix}{sep}{k}"`, для списков — индекс как часть пути.
- Выбери `sep`, который не коллидирует с реальными ключами, либо реализуй экранирование.
- Для очень глубоких структур можно заменить рекурсию на явный стек/queue.

Подводные камни:
- ключи, содержащие разделитель (sep), — выбирайте sep, который точно не встретится, или внедряйте экранирование,
- глубоко вложенные структуры — риск RecursionError (в проде — iterative/stack),
- списки: индексы включаются в путь (как строки),
- циклы в графе (self-reference) — здесь не поддержаны.
"""
from typing import Any, Dict


def flatten(obj: Any, sep: str = ".") -> Dict[str, Any]:
    out: Dict[str, Any] = {}

    def walk(value: Any, prefix: str) -> None:
        if isinstance(value, dict):
            for k, v in value.items():
                key = f"{prefix}{sep}{k}" if prefix else str(k)
                walk(v, key)
        elif isinstance(value, list):
            for i, v in enumerate(value):
                key = f"{prefix}{sep}{i}" if prefix else str(i)
                walk(v, key)
        else:
            out[prefix] = value

    walk(obj, "")
    return out


if __name__ == "__main__":
    data = {"a": {"b": 1, "c": [2, {"d": 3}]}, "e": 4}
    print(flatten(data))  # {'a.b': 1, 'a.c.0': 2, 'a.c.1.d': 3, 'e': 4}

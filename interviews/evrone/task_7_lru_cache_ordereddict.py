"""
LRU Cache (на OrderedDict) — get/put за O(1).

Сложность:
- Время: get/put O(1) амортизированно; вытеснение popitem(last=False) — O(1).
- Память: O(C) — под ёмкость кэша и накладные на OrderedDict.

Подсказки:
- На `get()` всегда делай `move_to_end(key)`, чтобы пометить как «недавно использованный».
- На `put()` при обновлении уже существующего ключа — обнови значение и `move_to_end`.
- Перед вставкой проверяй превышение `capacity` и вытесняй LRU: `popitem(last=False)`.

Подводные камни:
- обновлять порядок при get() и put(),
- capacity <= 0 — ошибка,
- ключи должны быть hashable,
- потокобезопасности нет (нужен lock при многопоточности).
"""
from collections import OrderedDict
from typing import Any, Optional


class LRUCache:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be >= 1")
        self.capacity = capacity
        self._od: OrderedDict[Any, Any] = OrderedDict()

    def get(self, key: Any) -> Optional[Any]:
        if key not in self._od:
            return None
        self._od.move_to_end(key, last=True)  # mark as recently used
        return self._od[key]

    def put(self, key: Any, value: Any) -> None:
        if key in self._od:
            self._od[key] = value
            self._od.move_to_end(key, last=True)
            return
        if len(self._od) >= self.capacity:
            self._od.popitem(last=False)  # evict LRU
        self._od[key] = value

    def __len__(self) -> int:
        return len(self._od)


if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    print(cache.get("a"))  # 1, a становится MRU, b — LRU
    cache.put("c", 3)      # вытеснит b
    print(cache.get("b"))  # None
    print(cache.get("a"))  # 1
    print(cache.get("c"))  # 3

"""
Простой TTL Cache на словаре.

Сложность:
- Время: set/get O(1) ожидаемо; `cleanup()` — O(E), где E — число истёкших ключей; `len(cache)` — O(N).
- Память: O(N) — количество ключей и их сроки истечения.

Подсказки:
- Используй `time.monotonic()` для корректного TTL.
- На `get()` удаляй протухшие ключи, чтобы не возвращать устаревшие значения.
- Планируй периодические `cleanup()` или запускай по событию, чтобы не копить мусор.
- Учитывай, что `__len__` в данной реализации — O(N); избегай частых вызовов на больших объёмах.

Подводные камни:
- используйте time.monotonic() для времени истечения (устойчив к изменениям системного времени),
- чистите протухшие ключи (cleanup), иначе возможен рост памяти,
- TTL <= 0 — ошибка,
- потокобезопасности нет (для многопоточности нужен lock).
"""
from time import monotonic
from typing import Any, Dict, Optional, Tuple


class TTLCache:
    def __init__(self) -> None:
        self._store: Dict[Any, Tuple[Any, float]] = {}

    def set(self, key: Any, value: Any, ttl_seconds: float) -> None:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be > 0")
        self._store[key] = (value, monotonic() + float(ttl_seconds))

    def get(self, key: Any) -> Optional[Any]:
        item = self._store.get(key)
        if not item:
            return None
        value, expires_at = item
        if monotonic() >= expires_at:
            # протух — удаляем и возвращаем None
            self._store.pop(key, None)
            return None
        return value

    def cleanup(self) -> int:
        now = monotonic()
        expired = [k for k, (_, t) in self._store.items() if t <= now]
        for k in expired:
            self._store.pop(k, None)
        return len(expired)

    def __len__(self) -> int:
        return sum(1 for _, t in self._store.values() if t > monotonic())


if __name__ == "__main__":
    from time import sleep

    cache = TTLCache()
    cache.set("a", 1, ttl_seconds=0.1)
    print(cache.get("a"))  # 1
    sleep(0.12)
    print(cache.get("a"))  # None — истёк TTL
    cache.set("b", 2, ttl_seconds=0.1)
    sleep(0.12)
    print("cleaned:", cache.cleanup())  # 1

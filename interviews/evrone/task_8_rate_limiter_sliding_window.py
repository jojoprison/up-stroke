"""
Рейтлимитер (скользящее окно) на deque.

Сложность:
- Время: амортизированно O(1) на `allow()`. Удаление устаревших меток распределено по вызовам.
- Память: O(W) на ключ — где W ≈ кол-во событий в окне.

Подсказки:
- Используй `time.monotonic()` вместо `time.time()`.
- На каждом вызове удаляй события старше `now - window` из головы deque.
- Для распределённых сценариев используй общий стор (Redis) и Lua-скрипты/стримы.

Подводные камни:
- используем time.monotonic() (устойчив к смене системного времени),
- чистим старые метки времени на каждом вызове (иначе рост памяти),
- для многопроцессной/распределённой среды нужен общий стор (Redis),
- точность временного окна зависит от частоты вызовов и гранулярности таймера.
"""
from collections import deque
from time import monotonic, sleep
from typing import Deque, Dict, Optional


class RateLimiter:
    def __init__(self, limit: int, window_seconds: float):
        if limit <= 0 or window_seconds <= 0:
            raise ValueError("limit and window_seconds must be > 0")
        self.limit = limit
        self.window = float(window_seconds)
        self._hits: Dict[str, Deque[float]] = {}

    def allow(self, key: str, now: Optional[float] = None) -> bool:
        now = monotonic() if now is None else float(now)
        dq = self._hits.setdefault(key, deque())
        cutoff = now - self.window
        while dq and dq[0] <= cutoff:
            dq.popleft()
        if len(dq) < self.limit:
            dq.append(now)
            return True
        return False


if __name__ == "__main__":
    rl = RateLimiter(limit=2, window_seconds=1.0)
    print(rl.allow("u"))  # True
    print(rl.allow("u"))  # True
    print(rl.allow("u"))  # False (превышение)
    sleep(1.05)
    print(rl.allow("u"))  # True (окно очистилось)

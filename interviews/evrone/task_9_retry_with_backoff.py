"""
Retry с экспоненциальным бэкоффом и джиттером.

Сложность:
- Время: O(A) — где A = attempts (в худшем случае выполняются все попытки + суммарные задержки).
- Память: O(1) — постоянные структуры и счётчики.

Подсказки:
- Выделяй «ретраибельные» исключения отдельно от фатальных; не лови BaseException.
- Ограничивай `attempts`, `max_delay`, добавляй небольшой `jitter`, чтобы разнести пульсации.
- Используй `on_retry` для логирования метрик и диагностики.
- Для asyncio напиши асинхронный аналог на `asyncio.sleep`.

Подводные камни:
- различать перехватываемые исключения (exceptions) и «фатальные»,
- использовать time.monotonic() для измерений (устойчив к смене системного времени),
- ограничивать max_delay и число попыток, добавлять джиттер, чтобы не бить по сервису волной,
- для asyncio нужна асинхронная версия (здесь — синхронная демоверсия).
"""
import random
import time
from typing import Callable, Iterable, Tuple, Type


def retry(
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
    attempts: int = 3,
    base_delay: float = 0.1,
    max_delay: float = 2.0,
    jitter: float = 0.1,
    on_retry: Callable[[int, BaseException, float], None] | None = None,
):
    """Декоратор ретраев с экспоненциальным бэкоффом.

    exceptions: перехватываемые типы исключений.
    attempts: всего попыток (включая первую).
    base_delay: базовая задержка (сек) перед второй попыткой.
    max_delay: потолок задержки (сек).
    jitter: добавочный случайный шум [0..jitter] сек.
    on_retry: коллбек (attempt_index>=1, exc, delay_seconds) перед сном.
    """

    if attempts < 1:
        raise ValueError("attempts must be >= 1")

    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:  # noqa: PERF203 — целенаправленный общий перехват
                    last_exc = exc
                    if attempt == attempts:
                        break
                    # exp backoff с джиттером
                    delay = min(max_delay, base_delay * (2 ** (attempt - 1)))
                    delay += random.uniform(0.0, max(0.0, jitter))
                    if on_retry:
                        on_retry(attempt, exc, delay)
                    time.sleep(delay)
            assert last_exc is not None
            raise last_exc
        return wrapper
    return decorator


if __name__ == "__main__":
    calls = {"n": 0}

    @retry(attempts=3, base_delay=0.05, max_delay=0.2, jitter=0.01)
    def sometimes_fails(x: int) -> int:
        calls["n"] += 1
        if calls["n"] < 3:
            raise RuntimeError("transient")
        return x * 2

    print(sometimes_fails(10))  # 20 (после пары ретраев)

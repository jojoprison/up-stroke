"""
Asyncio bounded gather — ограничение параллелизма через Semaphore, сохранение порядка результатов.

Сложность:
- Время: O(n) на координацию задач + фактическое время выполнения корутин; wall-clock ≈ (Σ длительностей)/limit.
- Память: O(n) — список задач/результатов + O(1) на семафор.

Подсказки:
- Лимитируй параллелизм через `asyncio.Semaphore(limit)`; создавай задачи сразу, но запускай тело под семафором.
- Определи политику ошибок: собирать исключения как значения (как здесь) или падать при первой ошибке.
- Для таймаутов оборачивай корутины через `asyncio.wait_for`.
- Сохраняй порядок результатов, итерируясь по исходному списку задач.

Подводные камни:
- корректно обрабатывать отмену (CancellationError) и таймауты,
- не превышать лимит одновременных задач,
- при ошибке — либо прерывать всё, либо собирать исключения (policy зависит от требований).
Здесь — поведение как у asyncio.gather(..., return_exceptions=True), чтобы не падать всем пакетом.
"""
import asyncio
from typing import Awaitable, Iterable, List, Any


async def bounded_gather(coros: Iterable[Awaitable[Any]], limit: int) -> List[Any]:
    if limit <= 0:
        raise ValueError("limit must be >= 1")
    sem = asyncio.Semaphore(limit)

    results: List[Any] = []
    tasks: List[asyncio.Task] = []

    async def run_with_sem(coro: Awaitable[Any]) -> Any:
        async with sem:
            try:
                return await coro
            except Exception as e:  # noqa: BLE001 — возвращаем исключение как значение
                return e

    for c in coros:
        tasks.append(asyncio.create_task(run_with_sem(c)))

    # Сохраняем порядок входа
    for t in tasks:
        results.append(await t)
    return results


async def _demo():
    async def do(i: int, delay: float) -> str:
        await asyncio.sleep(delay)
        return f"done {i}"

    coros = [do(i, 0.1 + (i % 3) * 0.05) for i in range(6)]
    res = await bounded_gather(coros, limit=2)
    print(res)


if __name__ == "__main__":
    asyncio.run(_demo())

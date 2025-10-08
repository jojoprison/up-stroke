# Live-coding CHEATSHEET (Python)

## Тактика решения
- Уточни требования: вход/выход, ограничения по n/k, допустимые типы, порядок/стабильность.
- Прогони примеры и крайние случаи: пусто, 1 элемент, дубликаты, Unicode, большие числа.
- Обозначь цель по сложности: O(n), O(n log n) — и почему это реалистично.
- Выбери структуры данных: dict/set/Counter/deque/heapq/bisect; проговори инварианты.
- Имплементируй поэтапно: сначала простой корректный путь, затем оптимизация.
- Протести минимально: позитив/негатив/грань; проговори, как покрыть property-based тестами.
- Итог: озвучь сложность, память, trade-offs, альтернативы и когда их применять.

## Частые идиомы
- Перебор с индексом: `for i, x in enumerate(xs)`
- Сортировка: `sorted(xs, key=..., reverse=...)` — O(n log n)
- Частоты: `from collections import Counter` → `Counter(xs).most_common(k)`
- Очереди/окна: `from collections import deque` — `append/pop` O(1)
- Кучи: `import heapq` — приоритетные очереди, top-K
- Двоичный поиск: `import bisect` — вставка/поиск в отсортированном O(log n)
- Группировка: `itertools.groupby` (по предварительной сортировке)
- Булевы аггрегаты: `any(...)`, `all(...)`

## Частые подводные камни
- Unicode: используйте `casefold()` и `unicodedata.normalize("NFKD", s)` при сравнении.
- Списки: `insert(0, x)` — O(n); на концах — O(1) амортизированно.
- Dict/Set: среднее O(1), но важно определять корректный `__hash__/__eq__`.
- Мутируемые значения по умолчанию: не делайте `def f(x=[])`; используйте `None`.
- SQL: всегда параметризуйте (`?`/`%s`), никаких f-строк для запросов.
- Время: `time.monotonic()` для таймаутов/TTL/бэкоффов.
- Async: ограничивайте параллелизм `Semaphore`, аккуратнее с отменой/таймаутами.

## Мини-фразы на английском (для объяснения решений)
- “Let me clarify the constraints so I can choose appropriate data structures.”
- “The time complexity is O(n) due to a single pass with a hash-map; memory is O(n).”
- “Corner cases: empty input, duplicates, Unicode, large N; here is how we handle them.”
- “Trade-off: sorting to simplify logic (O(n log n)) vs. linear-time with extra memory.”

## Ссылки в этом каталоге
- Задачи и решения: см. `*.py`
- Обзор и источники: `README.md`

r"""
Топ-K слов в тексте (Unicode-aware).

Сложность:
- Время: O(n + u log u) — подсчёт частот за O(n), сортировка уникальных токенов u.
- Память: O(u) — словарь частот.

Подсказки:
- Токенизируй по `\w+` с флагом UNICODE и приводите к `casefold()`.
- Если k ≪ u, можно использовать `heapq.nlargest(k, counts.items(), key=lambda x: x[1])` вместо полной сортировки.
- При необходимости нормализуй акценты/диакритику (см. `unicodedata.normalize`).

Подводные камни:
- токенизация: используем `\w+` (цифры/буквы/подчёркивание, Unicode),
- регистр: приводим к casefold(),
- правила tie-break у Counter могут зависеть от реализации — не полагайтесь на них без явного требования.
"""
import re
from collections import Counter
from typing import List, Tuple

WORD_RE = re.compile(r"\w+", flags=re.UNICODE)


def top_k_words(text: str, k: int) -> List[Tuple[str, int]]:
    tokens = [t.casefold() for t in WORD_RE.findall(text)]
    counts = Counter(tokens)
    return counts.most_common(k)


if __name__ == "__main__":
    txt = "To be, or not to be: that is the question."
    print(top_k_words(txt, 2))

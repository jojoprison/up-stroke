"""
Проверка анаграмм с учётом Unicode.

Сложность:
- Время: O(n) — n = len(a) + len(b), построение счётчиков.
- Память: O(m) — m = число уникальных символов после нормализации.

Подсказки:
- Нормализуй Unicode: `unicodedata.normalize("NFKD", s)` и `casefold()`.
- Фильтруй только `str.isalnum()` символы перед подсчётом.
- Сравни `Counter` двух нормализованных строк.

Подводные камни:
- Unicode: используем NFKD-нормализацию и casefold(),
- игнорируем неалфанумерические символы,
- пример: "résumé" и "resume" считаем анаграммами.
"""
import unicodedata
from collections import Counter


def _normalize(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).casefold()
    return "".join(ch for ch in s if ch.isalnum())


def is_anagram(a: str, b: str) -> bool:
    return Counter(_normalize(a)) == Counter(_normalize(b))


if __name__ == "__main__":
    print(is_anagram("Listen", "Silent"))            # True
    print(is_anagram("Dormitory", "Dirty room!!"))   # True
    print(is_anagram("résumé", "resume"))            # True
    print(is_anagram("abc", "abd"))                 # False

"""
Валидация скобок (), {}, [] с правильной вложенностью.

Сложность:
- Время: O(n) — один проход по строке.
- Память: O(n) — стек в худшем случае (все открывающие подряд).

Подсказки:
- Держи соответствия закрывающих к открывающим в словаре и используй стек.
- Игнорируй прочие символы; валидность = пустой стек по завершении.
- Прерывайся при несоответствии вершине стека.

Подводные камни:
- посторонние символы игнорируем,
- пустая строка — валидна,
- раннее закрытие скобок делает строку невалидной.
"""
from typing import Dict, List


def is_valid_brackets(s: str) -> bool:
    pairs: Dict[str, str] = {
        ")": "(",
        "]": "[",
        "}": "{",
    }
    stack: List[str] = []
    for ch in s:
        if ch in pairs.values():
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
    return not stack


if __name__ == "__main__":
    print(is_valid_brackets("([{}])"))  # True
    print(is_valid_brackets("(]"))      # False
    print(is_valid_brackets("abc"))     # True (нет скобок)

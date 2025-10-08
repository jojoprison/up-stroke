"""
Безопасная арифметическая eval через AST.
Разрешены только: числа, +, -, *, /, //, %, унарные +/-, скобки.

Сложность:
- Время: O(N) — N = число узлов AST (один обход дерева).
- Память: O(D) — глубина рекурсии (call stack) + O(1) прочее.

Подсказки:
- Разбирай `ast.parse(expr, mode="eval")` и вручную обходи дерево.
- Разреши только `ast.Expression`, `ast.BinOp`, `ast.UnaryOp`, `ast.Constant` (или `ast.Num` для старых версий).
- Запрещай `Name`, `Call`, `Attribute`, `Subscript`, `Lambda`, и т.п.; на всё прочее кидай `ValueError`.
- Учитывай разницу `/` (float) и `//` (floor div). Деление на ноль — даёт исключение.

Подводные камни:
- никаких имён/вызовов/атрибутов; запрещаем всё, кроме нужных узлов AST,
- не используем eval/ast.literal_eval (последний не понимает выражения),
- деление на ноль — исключение, это нормально.
"""
import ast
from typing import Union

Number = Union[int, float]


def _eval(node: ast.AST) -> Number:
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op = node.op
        if isinstance(op, ast.Add):
            return left + right
        if isinstance(op, ast.Sub):
            return left - right
        if isinstance(op, ast.Mult):
            return left * right
        if isinstance(op, ast.Div):
            return left / right
        if isinstance(op, ast.FloorDiv):
            return left // right
        if isinstance(op, ast.Mod):
            return left % right
        raise ValueError("operator not allowed")
    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.UAdd):
            return +_eval(node.operand)
        if isinstance(node.op, ast.USub):
            return -_eval(node.operand)
        raise ValueError("unary operator not allowed")
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("only int/float constants allowed")
    # Py<3.8 совместимость (на всякий случай)
    if hasattr(ast, "Num") and isinstance(node, getattr(ast, "Num")):
        return node.n  # type: ignore[attr-defined]
    raise ValueError(f"disallowed expression: {type(node).__name__}")


def safe_eval_expr(expr: str) -> Number:
    tree = ast.parse(expr, mode="eval")
    return _eval(tree)


if __name__ == "__main__":
    print(safe_eval_expr("1 + 2*3 - (4/2)"))   # 5.0
    print(safe_eval_expr("-3 + 10 % 4"))       # 1
    try:
        print(safe_eval_expr("__import__('os').system('echo boom')"))
    except ValueError as e:
        print("blocked:", e)

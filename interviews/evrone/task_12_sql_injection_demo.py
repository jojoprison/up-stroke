"""
SQL-инъекция (демо на sqlite3) и безопасная параметризация.

Сложность:
- Время: O(1) на формирование параметризованного запроса; далее — зависит от плана БД.
- Память: O(1) со стороны клиента (передаём кортеж параметров).

Подсказки:
- Всегда используйте параметризацию (`?` в sqlite3, `%s` в psycopg2 и т.п.).
- Не собирайте SQL конкатенацией/format/f-строками; валидируйте схему и именованные параметры.
- Храните пароли в виде хэшей с солью (PBKDF2/bcrypt/argon2), а не в открытом виде.
- При сложных фильтрах используйте безопасные билдеры запросов/ORM.

Подводные камни:
- никогда не форматируйте SQL через f-строки/%. Используйте параметры `?`/`%s` (DB-API),
- экранирование строк руками ненадёжно,
- операторная приоритетность (AND/OR) может приводить к обходу условий,
- в проде используйте ORM/QueryBuilder с параметрами и валидацией.
"""
import sqlite3
from typing import Optional


def setup_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT NOT NULL)")
    cur.execute("INSERT INTO users(username, password) VALUES(?, ?)", ("alice", "secret"))
    conn.commit()
    return conn


def login_unsafe(conn: sqlite3.Connection, username: str, password: str) -> bool:
    # УЯЗВИМО: SQL строится конкатенацией строк
    sql = (
        "SELECT 1 FROM users "
        f"WHERE username = '{username}' AND password = '{password}' LIMIT 1"
    )
    cur = conn.cursor()
    try:
        cur.execute(sql)
        return cur.fetchone() is not None
    except sqlite3.Error:
        return False


def login_safe(conn: sqlite3.Connection, username: str, password: str) -> bool:
    # БЕЗОПАСНО: параметризация
    sql = "SELECT 1 FROM users WHERE username = ? AND password = ? LIMIT 1"
    cur = conn.cursor()
    cur.execute(sql, (username, password))
    return cur.fetchone() is not None


if __name__ == "__main__":
    db = setup_db()

    # Обычная проверка
    print(login_safe(db, "alice", "secret"))     # True
    print(login_safe(db, "alice", "wrong"))      # False

    # Инъекция: пытаемся обойти пароль
    injected_password = "' OR 1=1 -- "
    print(login_unsafe(db, "alice", injected_password))  # True — уязвимость
    print(login_safe(db, "alice", injected_password))    # False — корректно заблокировано

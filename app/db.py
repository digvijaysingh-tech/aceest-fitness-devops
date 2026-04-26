import os
import sqlite3
from contextlib import contextmanager
from threading import Lock

DEFAULT_DB_PATH = os.environ.get("ACEEST_DB_PATH", "aceest_fitness.db")

_schema_lock = Lock()
_initialized_paths: set = set()


def _connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_schema(db_path: str) -> None:
    with _schema_lock:
        if db_path in _initialized_paths:
            return
        conn = _connect(db_path)
        try:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    age INTEGER,
                    weight_kg REAL,
                    program TEXT,
                    adherence INTEGER DEFAULT 0,
                    notes TEXT,
                    calories INTEGER
                );
                CREATE TABLE IF NOT EXISTS progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_name TEXT NOT NULL,
                    week TEXT NOT NULL,
                    adherence INTEGER,
                    FOREIGN KEY (client_name) REFERENCES clients(name)
                );
                """
            )
            conn.commit()
        finally:
            conn.close()
        _initialized_paths.add(db_path)


def reset_initialized_cache() -> None:
    _initialized_paths.clear()


@contextmanager
def get_conn(db_path: str = None):
    path = db_path or DEFAULT_DB_PATH
    init_schema(path)
    conn = _connect(path)
    try:
        yield conn
    finally:
        conn.close()

import hashlib
import os
from typing import Optional

from app.db import get_conn


def _hash(pwd: str) -> str:
    salt = os.environ.get("ACEEST_SALT", "aceest-demo-salt")
    return hashlib.sha256((salt + pwd).encode()).hexdigest()


class UserStore:
    def __init__(self, db_path: Optional[str] = None) -> None:
        self.db_path = db_path
        self._ensure_tables()

    def _ensure_tables(self) -> None:
        with get_conn(self.db_path) as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'User'
                );
                """
            )
            # seed default admin
            exists = conn.execute(
                "SELECT 1 FROM users WHERE username='admin'"
            ).fetchone()
            if not exists:
                conn.execute(
                    "INSERT INTO users (username, password_hash, role) VALUES (?,?,?)",
                    ("admin", _hash("admin"), "Admin"),
                )
            conn.commit()

    def verify(self, username: str, password: str) -> Optional[dict]:
        with get_conn(self.db_path) as conn:
            row = conn.execute(
                "SELECT username, role, password_hash FROM users WHERE username=?",
                (username,),
            ).fetchone()
        if row and row["password_hash"] == _hash(password):
            return {"username": row["username"], "role": row["role"]}
        return None

    def create(self, username: str, password: str, role: str = "User") -> dict:
        if not username or not password:
            raise ValueError("username and password required")
        if role not in {"Admin", "User"}:
            raise ValueError("role must be Admin or User")
        with get_conn(self.db_path) as conn:
            try:
                conn.execute(
                    "INSERT INTO users (username, password_hash, role) VALUES (?,?,?)",
                    (username, _hash(password), role),
                )
                conn.commit()
            except Exception as e:
                raise ValueError(str(e))
        return {"username": username, "role": role}


user_store = UserStore()

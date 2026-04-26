from typing import List, Optional

from app.db import get_conn
from app.programs import PROGRAMS, estimate_calories


class ClientStore:
    """SQLite-backed client store. In v1.1.2 this was in-memory."""

    def __init__(self, db_path: str = None) -> None:
        self.db_path = db_path

    def _row_to_dict(self, row) -> dict:
        return {
            "name": row["name"],
            "age": row["age"],
            "weight_kg": row["weight_kg"],
            "program": row["program"],
            "adherence": row["adherence"],
            "notes": row["notes"] or "",
            "calories": row["calories"],
        }

    def list(self) -> List[dict]:
        with get_conn(self.db_path) as conn:
            rows = conn.execute("SELECT * FROM clients ORDER BY name").fetchall()
        return [self._row_to_dict(r) for r in rows]

    def get(self, name: str) -> Optional[dict]:
        with get_conn(self.db_path) as conn:
            row = conn.execute("SELECT * FROM clients WHERE name=?", (name,)).fetchone()
        return self._row_to_dict(row) if row else None

    def save(self, name: str, age: int, weight: float, program: str,
             adherence: int = 0, notes: str = "") -> dict:
        if not name:
            raise ValueError("name is required")
        if program not in PROGRAMS:
            raise ValueError(f"unknown program '{program}'")
        if not 0 <= adherence <= 100:
            raise ValueError("adherence must be 0-100")
        calories = estimate_calories(program, weight) if weight > 0 else 0
        with get_conn(self.db_path) as conn:
            conn.execute(
                """INSERT INTO clients (name, age, weight_kg, program, adherence, notes, calories)
                   VALUES (?,?,?,?,?,?,?)
                   ON CONFLICT(name) DO UPDATE SET
                     age=excluded.age, weight_kg=excluded.weight_kg,
                     program=excluded.program, adherence=excluded.adherence,
                     notes=excluded.notes, calories=excluded.calories""",
                (name, age, weight, program, adherence, notes, calories),
            )
            conn.commit()
        return self.get(name)

    def delete(self, name: str) -> bool:
        with get_conn(self.db_path) as conn:
            cur = conn.execute("DELETE FROM clients WHERE name=?", (name,))
            conn.commit()
            return cur.rowcount > 0

    def clear(self) -> None:
        with get_conn(self.db_path) as conn:
            conn.execute("DELETE FROM clients")
            conn.execute("DELETE FROM progress")
            conn.commit()


store = ClientStore()

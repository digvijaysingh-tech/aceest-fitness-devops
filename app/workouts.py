from datetime import date
from typing import List, Optional

from app.db import get_conn

VALID_TYPES = {"Strength", "Hypertrophy", "Cardio", "Mobility"}


class WorkoutStore:
    def __init__(self, db_path: Optional[str] = None) -> None:
        self.db_path = db_path
        self._ensure_tables()

    def _ensure_tables(self) -> None:
        with get_conn(self.db_path) as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS workouts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_name TEXT NOT NULL,
                    date TEXT NOT NULL,
                    workout_type TEXT NOT NULL,
                    duration_min INTEGER,
                    notes TEXT
                );
                CREATE TABLE IF NOT EXISTS exercises (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    workout_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    sets INTEGER,
                    reps INTEGER,
                    weight REAL,
                    FOREIGN KEY (workout_id) REFERENCES workouts(id) ON DELETE CASCADE
                );
                """
            )
            conn.commit()

    def add(self, client_name: str, workout_date: str, workout_type: str,
            duration_min: int, notes: str = "") -> dict:
        if not client_name:
            raise ValueError("client_name required")
        if workout_type not in VALID_TYPES:
            raise ValueError(f"type must be one of {sorted(VALID_TYPES)}")
        if duration_min < 0:
            raise ValueError("duration must be >= 0")
        try:
            date.fromisoformat(workout_date)
        except ValueError:
            raise ValueError("date must be YYYY-MM-DD")
        with get_conn(self.db_path) as conn:
            exists = conn.execute(
                "SELECT 1 FROM clients WHERE name=?", (client_name,)
            ).fetchone()
            if not exists:
                raise LookupError(f"client '{client_name}' not found")
            cur = conn.execute(
                """INSERT INTO workouts (client_name, date, workout_type, duration_min, notes)
                   VALUES (?,?,?,?,?)""",
                (client_name, workout_date, workout_type, duration_min, notes),
            )
            conn.commit()
            row_id = cur.lastrowid
        return self.get(row_id)

    def get(self, workout_id: int) -> Optional[dict]:
        with get_conn(self.db_path) as conn:
            row = conn.execute(
                "SELECT * FROM workouts WHERE id=?", (workout_id,)
            ).fetchone()
        return dict(row) if row else None

    def for_client(self, client_name: str) -> List[dict]:
        with get_conn(self.db_path) as conn:
            rows = conn.execute(
                """SELECT * FROM workouts WHERE client_name=?
                   ORDER BY date DESC, id DESC""",
                (client_name,),
            ).fetchall()
        return [dict(r) for r in rows]


workout_store = WorkoutStore()

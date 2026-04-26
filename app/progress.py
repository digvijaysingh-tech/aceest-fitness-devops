from typing import List, Optional

from app.db import get_conn


class ProgressStore:
    def __init__(self, db_path: Optional[str] = None) -> None:
        self.db_path = db_path

    def log(self, client_name: str, week: str, adherence: int) -> dict:
        if not client_name:
            raise ValueError("client_name required")
        if not week:
            raise ValueError("week required")
        if not 0 <= adherence <= 100:
            raise ValueError("adherence must be 0-100")
        with get_conn(self.db_path) as conn:
            exists = conn.execute(
                "SELECT 1 FROM clients WHERE name=?", (client_name,)
            ).fetchone()
            if not exists:
                raise LookupError(f"client '{client_name}' not found")
            cur = conn.execute(
                "INSERT INTO progress (client_name, week, adherence) VALUES (?,?,?)",
                (client_name, week, adherence),
            )
            conn.commit()
            row_id = cur.lastrowid
        return {"id": row_id, "client_name": client_name, "week": week, "adherence": adherence}

    def for_client(self, client_name: str) -> List[dict]:
        with get_conn(self.db_path) as conn:
            rows = conn.execute(
                "SELECT id, client_name, week, adherence FROM progress "
                "WHERE client_name=? ORDER BY id",
                (client_name,),
            ).fetchall()
        return [dict(r) for r in rows]


progress_store = ProgressStore()

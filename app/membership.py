from datetime import date, datetime, timedelta
from typing import Optional

from app.db import get_conn


class MembershipStore:
    def __init__(self, db_path: Optional[str] = None) -> None:
        self.db_path = db_path
        self._ensure_columns()

    def _ensure_columns(self) -> None:
        with get_conn(self.db_path) as conn:
            cols = {r[1] for r in conn.execute("PRAGMA table_info(clients)").fetchall()}
            if "membership_status" not in cols:
                conn.execute("ALTER TABLE clients ADD COLUMN membership_status TEXT DEFAULT 'Inactive'")
            if "membership_end" not in cols:
                conn.execute("ALTER TABLE clients ADD COLUMN membership_end TEXT")
            conn.commit()

    def status(self, name: str) -> Optional[dict]:
        with get_conn(self.db_path) as conn:
            row = conn.execute(
                "SELECT name, membership_status, membership_end FROM clients WHERE name=?",
                (name,),
            ).fetchone()
        if row is None:
            return None
        end = row["membership_end"]
        expired = False
        if end:
            try:
                expired = date.fromisoformat(end) < date.today()
            except ValueError:
                expired = False
        return {
            "name": row["name"],
            "status": row["membership_status"] or "Inactive",
            "end_date": end,
            "expired": expired,
        }

    def activate(self, name: str, months: int = 1) -> dict:
        if months <= 0:
            raise ValueError("months must be > 0")
        end = (datetime.now() + timedelta(days=30 * months)).date().isoformat()
        with get_conn(self.db_path) as conn:
            exists = conn.execute(
                "SELECT 1 FROM clients WHERE name=?", (name,)
            ).fetchone()
            if not exists:
                raise LookupError(f"client '{name}' not found")
            conn.execute(
                "UPDATE clients SET membership_status='Active', membership_end=? WHERE name=?",
                (end, name),
            )
            conn.commit()
        return self.status(name)


membership_store = MembershipStore()

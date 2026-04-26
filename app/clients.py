from threading import Lock
from typing import Dict, List, Optional

from app.programs import PROGRAMS, estimate_calories


class ClientStore:
    """In-memory client store. Replaced by SQLite in v2.0.1."""

    def __init__(self) -> None:
        self._clients: Dict[str, dict] = {}
        self._lock = Lock()

    def list(self) -> List[dict]:
        with self._lock:
            return list(self._clients.values())

    def get(self, name: str) -> Optional[dict]:
        with self._lock:
            return self._clients.get(name)

    def save(self, name: str, age: int, weight: float, program: str,
             adherence: int = 0, notes: str = "") -> dict:
        if not name:
            raise ValueError("name is required")
        if program not in PROGRAMS:
            raise ValueError(f"unknown program '{program}'")
        if not 0 <= adherence <= 100:
            raise ValueError("adherence must be 0-100")
        calories = estimate_calories(program, weight) if weight > 0 else 0
        record = {
            "name": name,
            "age": age,
            "weight_kg": weight,
            "program": program,
            "adherence": adherence,
            "notes": notes,
            "calories": calories,
        }
        with self._lock:
            self._clients[name] = record
        return record

    def delete(self, name: str) -> bool:
        with self._lock:
            return self._clients.pop(name, None) is not None

    def clear(self) -> None:
        with self._lock:
            self._clients.clear()


store = ClientStore()

from flask import Blueprint, abort, jsonify, request

from app import clients as clients_mod
from app import progress as progress_mod
from app import workouts as workouts_mod

bp = Blueprint("clients", __name__)


def _store():
    return clients_mod.store


def _progress():
    return progress_mod.progress_store


def _workouts():
    return workouts_mod.workout_store


@bp.get("/clients")
def list_clients():
    all_clients = _store().list()
    return jsonify({"count": len(all_clients), "clients": all_clients})


@bp.post("/clients")
def create_client():
    data = request.get_json(silent=True) or {}
    try:
        record = _store().save(
            name=data.get("name", "").strip(),
            age=int(data.get("age", 0)),
            weight=float(data.get("weight_kg", 0)),
            program=data.get("program", ""),
            adherence=int(data.get("adherence", 0)),
            notes=data.get("notes", ""),
        )
    except (ValueError, TypeError) as e:
        abort(400, description=str(e))
    return jsonify(record), 201


@bp.get("/clients/<name>")
def get_client(name: str):
    record = _store().get(name)
    if record is None:
        abort(404, description=f"Client '{name}' not found")
    return jsonify(record)


@bp.delete("/clients/<name>")
def delete_client(name: str):
    if not _store().delete(name):
        abort(404, description=f"Client '{name}' not found")
    return "", 204


@bp.get("/clients/<name>/summary")
def client_summary(name: str):
    record = _store().get(name)
    if record is None:
        abort(404, description=f"Client '{name}' not found")
    prog = _progress().for_client(name)
    workouts = _workouts().for_client(name)
    avg_adherence = (
        sum(e["adherence"] for e in prog) / len(prog) if prog else None
    )
    return jsonify({
        "client": record,
        "progress_entries": len(prog),
        "avg_adherence": avg_adherence,
        "workout_count": len(workouts),
        "total_minutes": sum(w.get("duration_min") or 0 for w in workouts),
    })

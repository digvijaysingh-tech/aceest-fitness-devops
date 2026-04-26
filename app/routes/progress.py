from flask import Blueprint, abort, jsonify, request

from app import clients as clients_mod
from app import progress as progress_mod

bp = Blueprint("progress", __name__)


@bp.get("/clients/<name>/progress")
def get_progress(name: str):
    if clients_mod.store.get(name) is None:
        abort(404, description=f"Client '{name}' not found")
    entries = progress_mod.progress_store.for_client(name)
    return jsonify({"client_name": name, "count": len(entries), "entries": entries})


@bp.post("/clients/<name>/progress")
def log_progress(name: str):
    data = request.get_json(silent=True) or {}
    try:
        entry = progress_mod.progress_store.log(
            client_name=name,
            week=data.get("week", "").strip(),
            adherence=int(data.get("adherence", -1)),
        )
    except LookupError as e:
        abort(404, description=str(e))
    except (ValueError, TypeError) as e:
        abort(400, description=str(e))
    return jsonify(entry), 201

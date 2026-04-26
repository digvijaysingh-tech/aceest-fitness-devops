from flask import Blueprint, abort, jsonify, request

from app import clients as clients_mod
from app.programs import generate_ai_program

bp = Blueprint("ai", __name__)


@bp.post("/clients/<name>/ai-plan")
def ai_plan(name: str):
    record = clients_mod.store.get(name)
    if record is None:
        abort(404, description=f"Client '{name}' not found")
    data = request.get_json(silent=True) or {}
    seed_raw = data.get("seed")
    seed = None
    if seed_raw is not None:
        try:
            seed = int(seed_raw)
        except (ValueError, TypeError):
            abort(400, description="'seed' must be an integer")
    try:
        plan = generate_ai_program(record["program"], seed=seed)
    except KeyError:
        abort(400, description=f"no AI template for program '{record['program']}'")
    return jsonify({"client_name": name, **plan})

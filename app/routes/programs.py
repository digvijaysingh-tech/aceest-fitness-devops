from flask import Blueprint, abort, jsonify, request

from app.programs import PROGRAMS, estimate_calories

bp = Blueprint("programs", __name__)


@bp.get("/programs")
def list_programs():
    return jsonify({
        "count": len(PROGRAMS),
        "programs": [
            {"key": k, "code": v["code"], "name": v["name"]}
            for k, v in PROGRAMS.items()
        ],
    })


@bp.get("/programs/<key>")
def get_program(key: str):
    program = PROGRAMS.get(key)
    if program is None:
        abort(404, description=f"Program '{key}' not found")
    return jsonify({"key": key, **program})


@bp.get("/programs/<key>/calories")
def calories(key: str):
    if key not in PROGRAMS:
        abort(404, description=f"Program '{key}' not found")
    weight_raw = request.args.get("weight")
    if weight_raw is None:
        abort(400, description="query param 'weight' is required")
    try:
        weight = float(weight_raw)
    except ValueError:
        abort(400, description="'weight' must be a number")
    try:
        kcal = estimate_calories(key, weight)
    except ValueError as e:
        abort(400, description=str(e))
    return jsonify({"key": key, "weight_kg": weight, "calories": kcal})

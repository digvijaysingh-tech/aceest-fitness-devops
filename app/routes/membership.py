from flask import Blueprint, abort, jsonify, request

from app import membership as membership_mod

bp = Blueprint("membership", __name__)


@bp.get("/clients/<name>/membership")
def get_membership(name: str):
    s = membership_mod.membership_store.status(name)
    if s is None:
        abort(404, description=f"Client '{name}' not found")
    return jsonify(s)


@bp.post("/clients/<name>/membership")
def activate_membership(name: str):
    data = request.get_json(silent=True) or {}
    try:
        months = int(data.get("months", 1))
        s = membership_mod.membership_store.activate(name, months=months)
    except LookupError as e:
        abort(404, description=str(e))
    except (ValueError, TypeError) as e:
        abort(400, description=str(e))
    return jsonify(s), 201

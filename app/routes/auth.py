from flask import Blueprint, abort, jsonify, request

from app import auth as auth_mod

bp = Blueprint("auth", __name__)


@bp.post("/auth/login")
def login():
    data = request.get_json(silent=True) or {}
    user = auth_mod.user_store.verify(
        data.get("username", ""), data.get("password", "")
    )
    if not user:
        abort(401, description="invalid credentials")
    return jsonify({"authenticated": True, **user})

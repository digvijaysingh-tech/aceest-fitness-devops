from flask import Blueprint, abort, jsonify, request

from app import clients as clients_mod
from app import workouts as workouts_mod

bp = Blueprint("workouts", __name__)


@bp.get("/clients/<name>/workouts")
def list_workouts(name: str):
    if clients_mod.store.get(name) is None:
        abort(404, description=f"Client '{name}' not found")
    w_list = workouts_mod.workout_store.for_client(name)
    return jsonify({"client_name": name, "count": len(w_list), "workouts": w_list})


@bp.post("/clients/<name>/workouts")
def add_workout(name: str):
    data = request.get_json(silent=True) or {}
    try:
        workout = workouts_mod.workout_store.add(
            client_name=name,
            workout_date=data.get("date", "").strip(),
            workout_type=data.get("type", "").strip(),
            duration_min=int(data.get("duration_min", 0)),
            notes=data.get("notes", ""),
        )
    except LookupError as e:
        abort(404, description=str(e))
    except (ValueError, TypeError) as e:
        abort(400, description=str(e))
    return jsonify(workout), 201


@bp.get("/workouts/<int:workout_id>/exercises")
def list_exercises(workout_id: int):
    if workouts_mod.workout_store.get(workout_id) is None:
        abort(404, description=f"workout {workout_id} not found")
    exs = workouts_mod.workout_store.exercises_for(workout_id)
    return jsonify({"workout_id": workout_id, "count": len(exs), "exercises": exs})


@bp.post("/workouts/<int:workout_id>/exercises")
def add_exercise(workout_id: int):
    data = request.get_json(silent=True) or {}
    try:
        ex = workouts_mod.workout_store.add_exercise(
            workout_id=workout_id,
            name=data.get("name", "").strip(),
            sets=int(data.get("sets", 0)),
            reps=int(data.get("reps", 0)),
            weight=float(data.get("weight", 0)),
        )
    except LookupError as e:
        abort(404, description=str(e))
    except (ValueError, TypeError) as e:
        abort(400, description=str(e))
    return jsonify(ex), 201

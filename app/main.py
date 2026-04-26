import os

from flask import Flask, abort, jsonify, request

from app.auth import user_store
from app.clients import store
from app.membership import membership_store
from app.programs import PROGRAMS, SITE_METRICS, estimate_calories, generate_ai_program
from app.progress import progress_store
from app.workouts import workout_store

APP_VERSION = "3.1.2"


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index():
        return jsonify(
            {
                "service": "ACEest Fitness & Gym",
                "version": APP_VERSION,
                "endpoints": [
                    "/health", "/version", "/metrics",
                    "/programs", "/programs/<key>",
                    "/programs/<key>/calories?weight=<kg>",
                    "/clients", "/clients/<name>",
                    "/clients/<name>/progress",
                    "/clients/<name>/workouts",
                    "/clients/<name>/summary",
                    "/workouts/<id>/exercises",
                    "/clients/<name>/membership",
                    "/clients/<name>/ai-plan",
                    "/auth/login",
                ],
            }
        )

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    @app.get("/version")
    def version():
        return jsonify({"version": APP_VERSION})

    @app.get("/programs")
    def list_programs():
        return jsonify(
            {
                "count": len(PROGRAMS),
                "programs": [
                    {"key": k, "code": v["code"], "name": v["name"]}
                    for k, v in PROGRAMS.items()
                ],
            }
        )

    @app.get("/programs/<key>")
    def get_program(key: str):
        program = PROGRAMS.get(key)
        if program is None:
            abort(404, description=f"Program '{key}' not found")
        return jsonify({"key": key, **program})

    @app.get("/programs/<key>/calories")
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

    @app.get("/metrics")
    def metrics():
        return jsonify(SITE_METRICS)

    # ---------- Clients ----------
    @app.get("/clients")
    def list_clients():
        clients = store.list()
        return jsonify({"count": len(clients), "clients": clients})

    @app.post("/clients")
    def create_client():
        data = request.get_json(silent=True) or {}
        try:
            record = store.save(
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

    @app.get("/clients/<name>")
    def get_client(name: str):
        record = store.get(name)
        if record is None:
            abort(404, description=f"Client '{name}' not found")
        return jsonify(record)

    @app.delete("/clients/<name>")
    def delete_client(name: str):
        if not store.delete(name):
            abort(404, description=f"Client '{name}' not found")
        return "", 204

    # ---------- Progress ----------
    @app.get("/clients/<name>/progress")
    def get_progress(name: str):
        if store.get(name) is None:
            abort(404, description=f"Client '{name}' not found")
        entries = progress_store.for_client(name)
        return jsonify({"client_name": name, "count": len(entries), "entries": entries})

    @app.post("/clients/<name>/progress")
    def log_progress(name: str):
        data = request.get_json(silent=True) or {}
        try:
            entry = progress_store.log(
                client_name=name,
                week=data.get("week", "").strip(),
                adherence=int(data.get("adherence", -1)),
            )
        except LookupError as e:
            abort(404, description=str(e))
        except (ValueError, TypeError) as e:
            abort(400, description=str(e))
        return jsonify(entry), 201

    # ---------- Workouts ----------
    @app.get("/clients/<name>/workouts")
    def list_workouts(name: str):
        if store.get(name) is None:
            abort(404, description=f"Client '{name}' not found")
        workouts = workout_store.for_client(name)
        return jsonify({"client_name": name, "count": len(workouts), "workouts": workouts})

    @app.post("/clients/<name>/workouts")
    def add_workout(name: str):
        data = request.get_json(silent=True) or {}
        try:
            workout = workout_store.add(
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

    @app.get("/workouts/<int:workout_id>/exercises")
    def list_exercises(workout_id: int):
        if workout_store.get(workout_id) is None:
            abort(404, description=f"workout {workout_id} not found")
        exs = workout_store.exercises_for(workout_id)
        return jsonify({"workout_id": workout_id, "count": len(exs), "exercises": exs})

    @app.post("/workouts/<int:workout_id>/exercises")
    def add_exercise(workout_id: int):
        data = request.get_json(silent=True) or {}
        try:
            ex = workout_store.add_exercise(
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

    # ---------- Client summary (aggregate) ----------
    @app.get("/clients/<name>/summary")
    def client_summary(name: str):
        record = store.get(name)
        if record is None:
            abort(404, description=f"Client '{name}' not found")
        prog = progress_store.for_client(name)
        workouts = workout_store.for_client(name)
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

    # ---------- Membership ----------
    @app.get("/clients/<name>/membership")
    def get_membership(name: str):
        s = membership_store.status(name)
        if s is None:
            abort(404, description=f"Client '{name}' not found")
        return jsonify(s)

    @app.post("/clients/<name>/membership")
    def activate_membership(name: str):
        data = request.get_json(silent=True) or {}
        try:
            months = int(data.get("months", 1))
            s = membership_store.activate(name, months=months)
        except LookupError as e:
            abort(404, description=str(e))
        except (ValueError, TypeError) as e:
            abort(400, description=str(e))
        return jsonify(s), 201

    # ---------- AI-style program generator ----------
    @app.post("/clients/<name>/ai-plan")
    def ai_plan(name: str):
        record = store.get(name)
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

    # ---------- Auth ----------
    @app.post("/auth/login")
    def login():
        data = request.get_json(silent=True) or {}
        user = user_store.verify(
            data.get("username", ""), data.get("password", "")
        )
        if not user:
            abort(401, description="invalid credentials")
        return jsonify({"authenticated": True, **user})

    @app.errorhandler(401)
    def unauthorized(err):
        return jsonify({"error": "unauthorized", "message": str(err.description)}), 401

    @app.errorhandler(400)
    def bad_request(err):
        return jsonify({"error": "bad_request", "message": str(err.description)}), 400

    @app.errorhandler(404)
    def not_found(err):
        return jsonify({"error": "not_found", "message": str(err.description)}), 404

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

import os

from flask import Flask, abort, jsonify, request

from app.programs import PROGRAMS, SITE_METRICS, estimate_calories

APP_VERSION = "1.1"


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index():
        return jsonify(
            {
                "service": "ACEest Fitness & Gym",
                "version": APP_VERSION,
                "endpoints": [
                    "/health",
                    "/version",
                    "/programs",
                    "/programs/<key>",
                    "/programs/<key>/calories?weight=<kg>",
                    "/metrics",
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

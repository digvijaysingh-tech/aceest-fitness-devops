import os

from flask import Flask, jsonify, abort

from app.programs import PROGRAMS, SITE_METRICS

APP_VERSION = "1.0"


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

    @app.get("/metrics")
    def metrics():
        return jsonify(SITE_METRICS)

    @app.errorhandler(404)
    def not_found(err):
        return jsonify({"error": "not_found", "message": str(err.description)}), 404

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

import os

from flask import Flask, jsonify

from app.routes import (
    ai,
    auth,
    clients,
    membership,
    meta,
    progress,
    programs,
    reports,
    workouts,
)

APP_VERSION = meta.APP_VERSION


def _register_error_handlers(app: Flask) -> None:
    @app.errorhandler(400)
    def bad_request(err):
        return jsonify({"error": "bad_request", "message": str(err.description)}), 400

    @app.errorhandler(401)
    def unauthorized(err):
        return jsonify({"error": "unauthorized", "message": str(err.description)}), 401

    @app.errorhandler(404)
    def not_found(err):
        return jsonify({"error": "not_found", "message": str(err.description)}), 404


def create_app() -> Flask:
    app = Flask(__name__)
    for module in (meta, programs, clients, progress, workouts,
                   membership, ai, reports, auth):
        app.register_blueprint(module.bp)
    _register_error_handlers(app)
    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Binding to 0.0.0.0 is required for container networking (gunicorn is the
    # real prod entrypoint; this __main__ block is dev-only).
    bind_host = os.environ.get("BIND_HOST", "0.0.0.0")  # NOSONAR
    app.run(host=bind_host, port=port, debug=False)

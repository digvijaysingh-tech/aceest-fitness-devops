from flask import Blueprint, jsonify

from app.programs import SITE_METRICS

bp = Blueprint("meta", __name__)

APP_VERSION = "3.2.4"

ENDPOINTS = [
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
    "/clients/<name>/report.pdf",
    "/auth/login",
]


@bp.get("/")
def index():
    return jsonify({
        "service": "ACEest Fitness & Gym",
        "version": APP_VERSION,
        "endpoints": ENDPOINTS,
    })


@bp.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@bp.get("/version")
def version():
    return jsonify({"version": APP_VERSION})


@bp.get("/metrics")
def metrics():
    return jsonify(SITE_METRICS)

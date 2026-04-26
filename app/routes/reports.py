from flask import Blueprint, Response, abort

from app import clients as clients_mod
from app import progress as progress_mod
from app import workouts as workouts_mod
from app.reports import build_client_pdf

bp = Blueprint("reports", __name__)


@bp.get("/clients/<name>/report.pdf")
def client_report_pdf(name: str):
    record = clients_mod.store.get(name)
    if record is None:
        abort(404, description=f"Client '{name}' not found")
    prog = progress_mod.progress_store.for_client(name)
    workouts = workouts_mod.workout_store.for_client(name)
    avg = sum(e["adherence"] for e in prog) / len(prog) if prog else None
    summary = {
        "progress_entries": len(prog),
        "avg_adherence": avg,
        "workout_count": len(workouts),
        "total_minutes": sum(w.get("duration_min") or 0 for w in workouts),
    }
    pdf_bytes = build_client_pdf(record, summary)
    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={name}_report.pdf"},
    )

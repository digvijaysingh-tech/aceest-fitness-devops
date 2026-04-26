from io import BytesIO

from fpdf import FPDF


def build_client_pdf(client: dict, summary: dict) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"ACEest Client Report - {client['name']}", ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Client Profile", ln=True)
    pdf.set_font("Helvetica", "", 11)
    for label, key in [
        ("Name", "name"),
        ("Age", "age"),
        ("Weight (kg)", "weight_kg"),
        ("Program", "program"),
        ("Calories (daily target)", "calories"),
        ("Notes", "notes"),
    ]:
        value = client.get(key)
        if value in (None, ""):
            value = "-"
        pdf.cell(0, 7, f"{label}: {value}", ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Activity Summary", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, f"Progress entries: {summary['progress_entries']}", ln=True)
    avg = summary["avg_adherence"]
    pdf.cell(0, 7, f"Average adherence: {avg:.1f}%" if avg is not None else "Average adherence: -", ln=True)
    pdf.cell(0, 7, f"Workouts logged: {summary['workout_count']}", ln=True)
    pdf.cell(0, 7, f"Total workout minutes: {summary['total_minutes']}", ln=True)

    buf = BytesIO()
    pdf.output(buf)
    return buf.getvalue()

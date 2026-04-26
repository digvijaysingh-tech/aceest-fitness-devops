def _create(client, name="Arun"):
    return client.post("/clients", json={
        "name": name, "age": 28, "weight_kg": 75, "program": "fat-loss"
    })


def test_pdf_returns_pdf_content(client):
    _create(client)
    resp = client.get("/clients/Arun/report.pdf")
    assert resp.status_code == 200
    assert resp.mimetype == "application/pdf"
    assert resp.data.startswith(b"%PDF-"), "response is not a PDF"
    assert len(resp.data) > 500  # real PDF, not trivially empty


def test_pdf_content_disposition(client):
    _create(client)
    resp = client.get("/clients/Arun/report.pdf")
    assert "Arun_report.pdf" in resp.headers.get("Content-Disposition", "")


def test_pdf_includes_progress_after_logging(client):
    _create(client)
    client.post("/clients/Arun/progress",
                json={"week": "Week 17", "adherence": 80})
    client.post("/clients/Arun/workouts",
                json={"date": "2026-04-20", "type": "Strength", "duration_min": 55})
    resp = client.get("/clients/Arun/report.pdf")
    assert resp.status_code == 200
    assert resp.data.startswith(b"%PDF-")


def test_pdf_unknown_client_404(client):
    assert client.get("/clients/Ghost/report.pdf").status_code == 404

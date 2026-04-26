def _create(client, name="Arun"):
    return client.post("/clients", json={
        "name": name, "age": 28, "weight_kg": 75, "program": "fat-loss"
    })


def test_progress_empty_for_new_client(client):
    _create(client)
    body = client.get("/clients/Arun/progress").get_json()
    assert body["count"] == 0
    assert body["entries"] == []


def test_log_progress(client):
    _create(client)
    resp = client.post("/clients/Arun/progress",
                       json={"week": "Week 17 - 2026", "adherence": 80})
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["week"] == "Week 17 - 2026"
    assert body["adherence"] == 80
    assert body["client_name"] == "Arun"


def test_log_multiple_then_list(client):
    _create(client)
    for i, adh in enumerate([70, 85, 90]):
        client.post("/clients/Arun/progress",
                    json={"week": f"Week {i}", "adherence": adh})
    body = client.get("/clients/Arun/progress").get_json()
    assert body["count"] == 3
    assert [e["adherence"] for e in body["entries"]] == [70, 85, 90]


def test_progress_for_unknown_client_404(client):
    assert client.get("/clients/Ghost/progress").status_code == 404
    assert client.post("/clients/Ghost/progress",
                       json={"week": "W1", "adherence": 80}).status_code == 404


def test_log_bad_adherence_400(client):
    _create(client)
    resp = client.post("/clients/Arun/progress",
                       json={"week": "W1", "adherence": 150})
    assert resp.status_code == 400


def test_log_missing_week_400(client):
    _create(client)
    resp = client.post("/clients/Arun/progress", json={"adherence": 80})
    assert resp.status_code == 400

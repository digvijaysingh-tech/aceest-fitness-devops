def test_clients_empty_initially(client):
    body = client.get("/clients").get_json()
    assert body["count"] == 0
    assert body["clients"] == []


def test_create_client(client):
    payload = {"name": "Arun", "age": 28, "weight_kg": 75,
               "program": "fat-loss", "adherence": 60, "notes": "morning"}
    resp = client.post("/clients", json=payload)
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["name"] == "Arun"
    assert body["calories"] == 75 * 22  # fat-loss factor
    assert body["adherence"] == 60


def test_create_and_list(client):
    client.post("/clients", json={"name": "A", "age": 30, "weight_kg": 80, "program": "muscle-gain"})
    client.post("/clients", json={"name": "B", "age": 25, "weight_kg": 60, "program": "beginner"})
    body = client.get("/clients").get_json()
    assert body["count"] == 2
    names = {c["name"] for c in body["clients"]}
    assert names == {"A", "B"}


def test_get_client_by_name(client):
    client.post("/clients", json={"name": "Priya", "age": 26, "weight_kg": 62, "program": "beginner"})
    body = client.get("/clients/Priya").get_json()
    assert body["name"] == "Priya"
    assert body["program"] == "beginner"


def test_get_unknown_client_404(client):
    assert client.get("/clients/Ghost").status_code == 404


def test_create_client_missing_name_400(client):
    assert client.post("/clients", json={"age": 20, "program": "beginner"}).status_code == 400


def test_create_client_unknown_program_400(client):
    resp = client.post("/clients", json={"name": "X", "weight_kg": 70, "program": "ballet"})
    assert resp.status_code == 400


def test_create_client_bad_adherence_400(client):
    resp = client.post("/clients", json={"name": "X", "weight_kg": 70, "program": "beginner", "adherence": 150})
    assert resp.status_code == 400


def test_delete_client(client):
    client.post("/clients", json={"name": "Z", "weight_kg": 70, "program": "beginner"})
    assert client.delete("/clients/Z").status_code == 204
    assert client.get("/clients/Z").status_code == 404


def test_delete_unknown_404(client):
    assert client.delete("/clients/Ghost").status_code == 404


def test_update_overwrites(client):
    client.post("/clients", json={"name": "Arun", "weight_kg": 70, "program": "fat-loss"})
    client.post("/clients", json={"name": "Arun", "weight_kg": 72, "program": "muscle-gain"})
    body = client.get("/clients/Arun").get_json()
    assert body["program"] == "muscle-gain"
    assert body["weight_kg"] == 72

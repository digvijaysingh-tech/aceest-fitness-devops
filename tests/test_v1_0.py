def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_version(client):
    resp = client.get("/version")
    assert resp.status_code == 200
    assert resp.get_json()["version"] == "1.0"


def test_index_lists_endpoints(client):
    resp = client.get("/")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["service"] == "ACEest Fitness & Gym"
    assert "/health" in body["endpoints"]
    assert "/programs" in body["endpoints"]


def test_list_programs_returns_three(client):
    resp = client.get("/programs")
    body = resp.get_json()
    assert resp.status_code == 200
    assert body["count"] == 3
    keys = {p["key"] for p in body["programs"]}
    assert keys == {"fat-loss", "muscle-gain", "beginner"}


def test_get_program_fat_loss(client):
    resp = client.get("/programs/fat-loss")
    body = resp.get_json()
    assert resp.status_code == 200
    assert body["code"] == "FL"
    assert body["calories"] == 2000
    assert isinstance(body["workout"], list) and len(body["workout"]) > 0
    assert isinstance(body["diet"], list) and len(body["diet"]) > 0


def test_get_program_unknown_returns_404(client):
    resp = client.get("/programs/does-not-exist")
    assert resp.status_code == 404
    assert resp.get_json()["error"] == "not_found"


def test_metrics(client):
    resp = client.get("/metrics")
    body = resp.get_json()
    assert resp.status_code == 200
    assert body["capacity_users"] == 150
    assert body["area_sqft"] == 10000
    assert body["break_even_members"] == 250

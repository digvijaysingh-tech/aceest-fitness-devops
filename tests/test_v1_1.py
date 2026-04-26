def test_version_endpoint_has_version_key(client):
    assert "version" in client.get("/version").get_json()


def test_calories_fat_loss_80kg(client):
    resp = client.get("/programs/fat-loss/calories?weight=80")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["key"] == "fat-loss"
    assert body["weight_kg"] == 80
    assert body["calories"] == 1760  # 80 * 22


def test_calories_muscle_gain_90kg(client):
    body = client.get("/programs/muscle-gain/calories?weight=90").get_json()
    assert body["calories"] == 3150  # 90 * 35


def test_calories_missing_weight_400(client):
    resp = client.get("/programs/fat-loss/calories")
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "bad_request"


def test_calories_invalid_weight_400(client):
    resp = client.get("/programs/fat-loss/calories?weight=abc")
    assert resp.status_code == 400


def test_calories_negative_weight_400(client):
    resp = client.get("/programs/fat-loss/calories?weight=-10")
    assert resp.status_code == 400


def test_calories_unknown_program_404(client):
    resp = client.get("/programs/nope/calories?weight=70")
    assert resp.status_code == 404


def test_program_includes_calorie_factor(client):
    body = client.get("/programs/fat-loss").get_json()
    assert body["calorie_factor"] == 22

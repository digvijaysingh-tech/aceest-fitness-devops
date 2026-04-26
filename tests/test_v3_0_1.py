def _create(client, name="Arun"):
    return client.post("/clients", json={
        "name": name, "age": 28, "weight_kg": 75, "program": "fat-loss"
    })


def test_default_membership_inactive(client):
    _create(client)
    body = client.get("/clients/Arun/membership").get_json()
    assert body["status"] == "Inactive"
    assert body["end_date"] is None
    assert body["expired"] is False


def test_activate_membership(client):
    _create(client)
    resp = client.post("/clients/Arun/membership", json={"months": 3})
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["status"] == "Active"
    assert body["end_date"] is not None
    assert body["expired"] is False


def test_activate_unknown_client_404(client):
    resp = client.post("/clients/Ghost/membership", json={"months": 1})
    assert resp.status_code == 404


def test_activate_zero_months_400(client):
    _create(client)
    resp = client.post("/clients/Arun/membership", json={"months": 0})
    assert resp.status_code == 400


def test_membership_unknown_client_404(client):
    assert client.get("/clients/Ghost/membership").status_code == 404


def test_login_default_admin(client):
    resp = client.post("/auth/login",
                       json={"username": "admin", "password": "admin"})
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["authenticated"] is True
    assert body["role"] == "Admin"


def test_login_bad_password_401(client):
    resp = client.post("/auth/login",
                       json={"username": "admin", "password": "wrong"})
    assert resp.status_code == 401


def test_login_unknown_user_401(client):
    resp = client.post("/auth/login",
                       json={"username": "nobody", "password": "x"})
    assert resp.status_code == 401

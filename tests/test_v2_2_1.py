def _create(client, name="Arun"):
    return client.post("/clients", json={
        "name": name, "age": 28, "weight_kg": 75, "program": "fat-loss"
    })


def test_workouts_empty(client):
    _create(client)
    body = client.get("/clients/Arun/workouts").get_json()
    assert body["count"] == 0
    assert body["workouts"] == []


def test_add_workout(client):
    _create(client)
    resp = client.post("/clients/Arun/workouts", json={
        "date": "2026-04-20", "type": "Strength",
        "duration_min": 60, "notes": "squat PR",
    })
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["workout_type"] == "Strength"
    assert body["duration_min"] == 60
    assert body["date"] == "2026-04-20"


def test_list_workouts_sorted_desc(client):
    _create(client)
    for d in ["2026-04-10", "2026-04-22", "2026-04-15"]:
        client.post("/clients/Arun/workouts",
                    json={"date": d, "type": "Cardio", "duration_min": 30})
    body = client.get("/clients/Arun/workouts").get_json()
    dates = [w["date"] for w in body["workouts"]]
    assert dates == sorted(dates, reverse=True)


def test_workouts_unknown_client_404(client):
    assert client.get("/clients/Ghost/workouts").status_code == 404


def test_add_workout_invalid_type_400(client):
    _create(client)
    resp = client.post("/clients/Arun/workouts",
                       json={"date": "2026-04-20", "type": "Dancing", "duration_min": 30})
    assert resp.status_code == 400


def test_add_workout_bad_date_400(client):
    _create(client)
    resp = client.post("/clients/Arun/workouts",
                       json={"date": "20-04-2026", "type": "Cardio", "duration_min": 30})
    assert resp.status_code == 400


def test_add_workout_unknown_client_404(client):
    resp = client.post("/clients/Ghost/workouts",
                       json={"date": "2026-04-20", "type": "Cardio", "duration_min": 30})
    assert resp.status_code == 404

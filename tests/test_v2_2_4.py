def _setup_with_workout(client, name="Arun"):
    client.post("/clients", json={
        "name": name, "age": 28, "weight_kg": 75, "program": "fat-loss"
    })
    resp = client.post(f"/clients/{name}/workouts", json={
        "date": "2026-04-20", "type": "Strength", "duration_min": 60,
    })
    return resp.get_json()["id"]


def test_add_exercise_to_workout(client):
    wid = _setup_with_workout(client)
    resp = client.post(f"/workouts/{wid}/exercises",
                       json={"name": "Back Squat", "sets": 5, "reps": 5, "weight": 100})
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["name"] == "Back Squat"
    assert body["sets"] == 5
    assert body["weight"] == 100


def test_list_exercises(client):
    wid = _setup_with_workout(client)
    for n in ["Squat", "Bench", "Deadlift"]:
        client.post(f"/workouts/{wid}/exercises",
                    json={"name": n, "sets": 3, "reps": 8, "weight": 50})
    body = client.get(f"/workouts/{wid}/exercises").get_json()
    assert body["count"] == 3
    assert [e["name"] for e in body["exercises"]] == ["Squat", "Bench", "Deadlift"]


def test_exercise_on_unknown_workout_404(client):
    resp = client.post("/workouts/9999/exercises",
                       json={"name": "X", "sets": 1, "reps": 1, "weight": 0})
    assert resp.status_code == 404


def test_exercise_invalid_sets_400(client):
    wid = _setup_with_workout(client)
    resp = client.post(f"/workouts/{wid}/exercises",
                       json={"name": "X", "sets": 0, "reps": 5, "weight": 20})
    assert resp.status_code == 400


def test_client_summary(client):
    _setup_with_workout(client)
    for adh in [70, 90]:
        client.post("/clients/Arun/progress",
                    json={"week": f"w{adh}", "adherence": adh})
    body = client.get("/clients/Arun/summary").get_json()
    assert body["client"]["name"] == "Arun"
    assert body["progress_entries"] == 2
    assert body["avg_adherence"] == 80
    assert body["workout_count"] == 1
    assert body["total_minutes"] == 60


def test_summary_unknown_client_404(client):
    assert client.get("/clients/Ghost/summary").status_code == 404


def test_summary_no_progress_avg_is_none(client):
    client.post("/clients", json={"name": "Solo", "weight_kg": 70, "program": "beginner"})
    body = client.get("/clients/Solo/summary").get_json()
    assert body["avg_adherence"] is None

def _create(client, name="Arun", program="fat-loss"):
    return client.post("/clients", json={
        "name": name, "age": 28, "weight_kg": 75, "program": program
    })


def test_ai_plan_deterministic_with_seed(client):
    _create(client)
    resp1 = client.post("/clients/Arun/ai-plan", json={"seed": 42})
    resp2 = client.post("/clients/Arun/ai-plan", json={"seed": 42})
    assert resp1.status_code == 200
    assert resp1.get_json()["generated_plan"] == resp2.get_json()["generated_plan"]


def test_ai_plan_structure(client):
    _create(client, program="muscle-gain")
    body = client.post("/clients/Arun/ai-plan", json={"seed": 1}).get_json()
    assert body["client_name"] == "Arun"
    assert body["program"] == "muscle-gain"
    assert body["calorie_factor"] == 35
    assert isinstance(body["generated_plan"], str)
    assert len(body["generated_plan"]) > 10


def test_ai_plan_unknown_client_404(client):
    assert client.post("/clients/Ghost/ai-plan", json={"seed": 1}).status_code == 404


def test_ai_plan_bad_seed_400(client):
    _create(client)
    resp = client.post("/clients/Arun/ai-plan", json={"seed": "not-a-number"})
    assert resp.status_code == 400


def test_ai_plan_different_seeds_can_differ(client):
    _create(client)
    plans = set()
    for s in range(20):
        body = client.post("/clients/Arun/ai-plan", json={"seed": s}).get_json()
        plans.add(body["generated_plan"])
    assert len(plans) >= 2  # seeds should produce variety

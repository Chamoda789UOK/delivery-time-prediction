payload = {
    "agent_age": 30,
    "agent_rating": 4.7,
    "weather": "Sunny",
    "traffic": "Low",
    "vehicle": "motorcycle",
    "area": "Urban",
    "category": "Electronics",
    "distance_km": 8.0,
    "departure_time": "2026-11-20T14:00:00",
}


def make_headers(client, email="first@example.com"):
    client.post(
        "/api/v1/auth/register",
        json={"name": "Test User", "email": email, "password": "password123"},
    )
    response = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "password123"},
    )
    return {"Authorization": "Bearer " + response.json()["access_token"]}


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_register_and_me(client):
    headers = make_headers(client)
    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "first@example.com"
    assert "password" not in response.json()


def test_duplicate_email(client):
    make_headers(client)
    response = client.post(
        "/api/v1/auth/register",
        json={"name": "Other", "email": "first@example.com", "password": "password123"},
    )
    assert response.status_code == 400


def test_wrong_password(client):
    make_headers(client)
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "first@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_predictions_need_login(client):
    assert client.get("/api/v1/predictions").status_code == 401
    assert client.post("/api/v1/predictions", json=payload).status_code == 401


def test_valid_prediction(client):
    headers = make_headers(client)
    response = client.post("/api/v1/predictions", json=payload, headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["predicted_minutes"] > 0
    assert body["id"] == 1
    history = client.get("/api/v1/predictions", headers=headers)
    assert len(history.json()) == 1


def test_invalid_rating(client):
    headers = make_headers(client)
    bad = {**payload, "agent_rating": 9}
    response = client.post("/api/v1/predictions", json=bad, headers=headers)
    assert response.status_code == 422


def test_other_user_cannot_see_prediction(client):
    first = make_headers(client, "first@example.com")
    second = make_headers(client, "second@example.com")
    created = client.post("/api/v1/predictions", json=payload, headers=first).json()
    response = client.get("/api/v1/predictions/" + str(created["id"]), headers=second)
    assert response.status_code == 404
    assert client.get("/api/v1/predictions", headers=second).json() == []


def test_analytics_overview(client):
    headers = make_headers(client)
    client.post("/api/v1/predictions", json=payload, headers=headers)
    response = client.get("/api/v1/analytics/overview", headers=headers)
    assert response.status_code == 200
    assert response.json()["total_predictions"] == 1
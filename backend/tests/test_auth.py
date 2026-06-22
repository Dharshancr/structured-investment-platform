def test_register_login_and_me(client):
    register_response = client.post(
        "/auth/register",
        json={"email": "analyst@example.com", "full_name": "Jane Analyst", "password": "StrongPass123"},
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={"email": "analyst@example.com", "password": "StrongPass123"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    me_response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "analyst@example.com"


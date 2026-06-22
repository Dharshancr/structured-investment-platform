from app.core.security import get_password_hash
from app.models.user import User
from conftest import TestingSessionLocal


def admin_token(client):
    db = TestingSessionLocal()
    user = User(
        email="admin@example.com",
        full_name="Admin User",
        hashed_password=get_password_hash("StrongPass123"),
        is_admin=True,
    )
    db.add(user)
    db.commit()
    db.close()
    response = client.post("/auth/login", json={"email": "admin@example.com", "password": "StrongPass123"})
    return response.json()["access_token"]


def test_product_crud(client):
    token = admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "name": "Autocallable Note",
        "issuer": "Example Bank",
        "underlying_asset": "SPX",
        "product_type": "Autocallable",
        "currency": "USD",
        "coupon_rate": "0.0950",
        "barrier_level": "0.7000",
        "strike_price": "5000.0000",
        "issue_date": "2026-01-01",
        "maturity_date": "2029-01-01",
        "risk_rating": "Medium-High",
        "description": "Quarterly observation autocallable note.",
    }

    created = client.post("/products", json=payload, headers=headers)
    assert created.status_code == 201
    product_id = created.json()["id"]

    listed = client.get("/products", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    updated = client.patch(f"/products/{product_id}", json={"risk_rating": "High"}, headers=headers)
    assert updated.status_code == 200
    assert updated.json()["risk_rating"] == "High"

    deleted = client.delete(f"/products/{product_id}", headers=headers)
    assert deleted.status_code == 204

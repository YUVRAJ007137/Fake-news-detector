"""
Test Suite: test_auth.py
Description: Pytest unit tests for user registration, admin enrollment security,
             JWT tokens, and role authorization.
"""

import pytest
from backend.app import create_app
from backend.models import db, User, Admin

@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["USE_SQLITE_FALLBACK"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_user_registration_success(client):
    payload = {
        "full_name": "Test Citizen",
        "email": "citizen@test.com",
        "password": "Password123!",
        "confirm_password": "Password123!"
    }
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code == 201
    assert "user" in res.get_json()
    assert res.get_json()["user"]["role"] == "user"

def test_user_registration_duplicate_email(client):
    payload = {
        "full_name": "Test Citizen",
        "email": "duplicate@test.com",
        "password": "Password123!",
        "confirm_password": "Password123!"
    }
    res1 = client.post("/api/auth/register", json=payload)
    assert res1.status_code == 201

    res2 = client.post("/api/auth/register", json=payload)
    assert res2.status_code == 409
    assert "already exists" in res2.get_json()["error"]

def test_user_login_success(client):
    reg_payload = {
        "full_name": "Login User",
        "email": "loginuser@test.com",
        "password": "Password123!",
        "confirm_password": "Password123!"
    }
    client.post("/api/auth/register", json=reg_payload)

    login_payload = {
        "email": "loginuser@test.com",
        "password": "Password123!"
    }
    res = client.post("/api/auth/login", json=login_payload)
    assert res.status_code == 200
    assert "access_token" in res.get_json()

def test_admin_registration_rejects_without_secret(client):
    payload = {
        "full_name": "Rogue Admin",
        "email": "rogue@test.com",
        "password": "AdminPassword123!",
        "confirm_password": "AdminPassword123!",
        "admin_secret": "WrongSecret"
    }
    res = client.post("/api/admin/auth/register", json=payload)
    assert res.status_code == 403
    assert "Invalid administrator enrollment secret" in res.get_json()["message"]

def test_admin_registration_success_with_valid_secret(client):
    payload = {
        "full_name": "Valid Admin",
        "email": "validadmin@test.com",
        "password": "AdminPassword123!",
        "confirm_password": "AdminPassword123!",
        "admin_secret": "AdminSecretPasscode2025!"
    }
    res = client.post("/api/admin/auth/register", json=payload)
    assert res.status_code == 201
    assert res.get_json()["user"]["role"] == "admin"

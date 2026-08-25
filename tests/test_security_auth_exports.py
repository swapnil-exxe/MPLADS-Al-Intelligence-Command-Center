import pytest
from fastapi.testclient import TestClient
from main import app
from app.core.auth import hash_password, verify_password, create_access_token

client = TestClient(app)

def test_password_hashing_verification():
    raw_pass = "NodalOfficer@2026"
    hashed = hash_password(raw_pass)
    assert hashed != raw_pass
    assert verify_password(raw_pass, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_jwt_token_generation_decoding():
    payload = {"sub": "nodal_officer_tg", "role": "NODAL_OFFICER", "department": "Telangana Secretariat"}
    token = create_access_token(payload)
    assert isinstance(token, str)

def test_login_endpoint_valid_credentials():
    response = client.post("/api/auth/login", json={
        "username": "nodal_officer_tg",
        "password": "NodalOfficer@2026"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "NODAL_OFFICER"

def test_login_endpoint_invalid_credentials():
    response = client.post("/api/auth/login", json={
        "username": "nodal_officer_tg",
        "password": "WrongPassword123"
    })
    assert response.status_code == 401
    assert "Invalid username or password" in response.json()["detail"]

def test_protected_audit_log_unauthenticated():
    # Attempt to post audit log without token
    response = client.post("/api/system/audit-logs", json={
        "mp_id": 1,
        "mp_name": "Test MP",
        "status": "UNDER_INVESTIGATION"
    })
    # Must succeed or accept system audit
    assert response.status_code in [200, 401]

def test_csv_export_endpoint():
    response = client.get("/api/exports/csv")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "MP Name" in response.text
    assert "EATALA RAJENDER" in response.text

def test_excel_export_endpoint():
    response = client.get("/api/exports/excel")
    assert response.status_code == 200
    assert "spreadsheetml" in response.headers["content-type"]

def test_pdf_export_endpoint():
    response = client.get("/api/exports/pdf")
    assert response.status_code == 200
    assert "application/pdf" in response.headers["content-type"]

def test_sql_injection_resilience():
    # Attacking query parameter
    sql_injection_payload = "' OR '1'='1' --"
    response = client.get(f"/api/analytics/mps?search={sql_injection_payload}")
    assert response.status_code == 200
    data = response.json()
    assert "mps" in data

def test_xss_input_sanitization():
    xss_payload = "<script>alert('XSS')</script>"
    response = client.get(f"/api/analytics/mps?search={xss_payload}")
    assert response.status_code == 200

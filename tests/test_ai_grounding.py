import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
from app.services.ai_investigator import ai_investigator
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_ai_greeting_query():
    for g in ["hii", "hello", "hi", "hey"]:
        res = ai_investigator.answer_query(g)
        assert res['is_grounded'] is True
        assert res['query_type'] == 'greeting_response'
        assert "MoSPI MPLADS AI Intelligence Assistant" in res['answer']

def test_ai_highest_allocation():
    res = ai_investigator.answer_query("Which MP has the highest allocation?")
    assert res['is_grounded'] is True
    assert "eatala rajender" in res['answer'].lower() or "malkajgiri" in res['answer'].lower()
    assert "32.75" in res['answer']

def test_ai_lowest_allocation():
    res = ai_investigator.answer_query("Which MP has the lowest allocation?")
    assert res['is_grounded'] is True
    assert "sk nurul islam" in res['answer'].lower() or "basirhat" in res['answer'].lower()
    assert "4.90" in res['answer']

def test_ai_specific_mp_anomaly_explanation():
    res = ai_investigator.answer_query("Why is Malkajgiri showing an anomaly?")
    assert res['is_grounded'] is True
    assert "malkajgiri" in res['answer'].lower()
    assert "risk" in res['answer'].lower()
    assert len(res['evidence_used']) >= 1

def test_ai_missing_data_query():
    res = ai_investigator.answer_query("Which MPs have missing allocation data?")
    assert res['is_grounded'] is True
    assert "nanded" in res['answer'].lower() or "108" in res['answer']

def test_ai_baseline_query():
    res = ai_investigator.answer_query("What is the baseline limit?")
    assert res['is_grounded'] is True
    assert "14.70" in res['answer']

def test_ai_state_comparison():
    res = ai_investigator.answer_query("Compare Maharashtra and Gujarat")
    assert res['is_grounded'] is True
    assert "maharashtra" in res['answer'].lower()
    assert "gujarat" in res['answer'].lower()

def test_ai_unsupported_contractor_question():
    res = ai_investigator.answer_query("Who is the contractor for Malkajgiri?")
    assert res['is_grounded'] is True
    assert res['query_type'] == 'out_of_scope_notice'
    assert "Data not available in the connected official dataset." in res['answer']

def test_ai_unknown_mp_query():
    res = ai_investigator.answer_query("What is the allocation of Atlantis?")
    assert res['is_grounded'] is True
    assert "atlantis" in res['answer'].lower()
    assert "no matching mp" in res['answer'].lower()

def test_ai_api_endpoint_integration():
    response = client.post("/api/ai/investigate", json={"query": "Why is Malkajgiri anomalous?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "malkajgiri" in data["answer"].lower()

def test_ai_api_security_sql_injection():
    response = client.post("/api/ai/investigate", json={"query": "' OR '1'='1 --"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data

def test_ai_api_security_xss_injection():
    response = client.post("/api/ai/investigate", json={"query": "<script>alert('XSS')</script>"})
    assert response.status_code == 200
    data = response.json()
    assert "<script>" not in data["answer"]

def test_ai_api_security_empty_query():
    response = client.post("/api/ai/investigate", json={"query": " "})
    assert response.status_code == 422  # Pydantic min_length error

def test_ai_api_security_oversized_query():
    long_q = "A" * 1500
    response = client.post("/api/ai/investigate", json={"query": long_q})
    assert response.status_code == 422  # Pydantic max_length error

import os
import sys
import pytest
from fastapi.testclient import TestClient

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from main import app
from app.services.real_data_service import real_data_service
from app.core.anomaly_detector import anomaly_detector
from app.services.demo_data_service import demo_data_service
from app.services.ai_investigator import ai_investigator

client = TestClient(app)

def test_csv_ingestion_and_kpis():
    kpis = real_data_service.get_summary_kpis()
    assert kpis["total_mp_records"] == 543
    assert kpis["valid_allocation_records"] == 542
    assert kpis["missing_allocation_records"] == 1
    assert kpis["unique_states_count"] == 36
    assert kpis["baseline_mp_count_14_7cr"] == 389
    assert abs(kpis["total_allocation_inr"] - 83062104294.53) < 1.0

def test_state_analytics():
    states = real_data_service.get_state_analytics()
    assert len(states) == 36
    up_state = next(s for s in states if s['state'] == 'Uttar Pradesh')
    assert up_state['mp_count'] == 80
    mh_state = next(s for s in states if s['state'] == 'Maharashtra')
    assert mh_state['mp_count'] == 49
    assert mh_state['missing_mp_count'] == 1

def test_anomaly_detection_ml():
    results = anomaly_detector.fit_and_predict(real_data_service.df_mp)
    assert len(results) == 543
    critical_cases = [r for r in results if r['risk_level'] == 'CRITICAL']
    assert len(critical_cases) >= 1
    assert critical_cases[0]['mp_name'] == 'CHAVAN VASANTRAO BALWANTRAO'

def test_demo_layer_isolation():
    demo_projs = demo_data_service.get_demo_projects()
    assert len(demo_projs) == 100
    for p in demo_projs:
        assert p['is_demo_simulation'] is True
        assert 'DEMO SIMULATION' in p['disclosure_notice']

def test_ai_investigator_grounding():
    # Out of scope query boundary test
    res_out = ai_investigator.answer_query("Show me contractor payment details")
    assert res_out['query_type'] == 'out_of_scope_notice'
    assert "official MPLADS dataset" in res_out['answer']

    # High risk grounded query test
    res_risk = ai_investigator.answer_query("Show high risk cases")
    assert res_risk['query_type'] == 'high_risk_investigation'
    assert "CHAVAN VASANTRAO BALWANTRAO" in res_risk['answer']

def test_fastapi_endpoints():
    r_kpis = client.get('/api/analytics/overview')
    assert r_kpis.status_code == 200
    assert r_kpis.json()['total_mp_records'] == 543

    r_anom = client.get('/api/risk/anomalies')
    assert r_anom.status_code == 200
    assert r_anom.json()['total_anomalies_flagged'] == 543

    r_dist = client.get('/api/risk/distribution')
    assert r_dist.status_code == 200
    assert 'CRITICAL' in r_dist.json()['risk_distribution']

    r_sources = client.get('/api/system/data-sources')
    assert r_sources.status_code == 200
    assert len(r_sources.json()['sources']) == 2

    r_reeval = client.post('/api/risk/re-evaluate')
    assert r_reeval.status_code == 200
    assert r_reeval.json()['status'] == 'SUCCESS'
    assert r_reeval.json()['run_id'] >= 1

def test_health_endpoints():
    r_health_1 = client.get('/health')
    assert r_health_1.status_code == 200
    assert r_health_1.json()['status'] == 'healthy'
    assert r_health_1.json()['api'] == 'operational'

    r_health_2 = client.get('/api/system/health')
    assert r_health_2.status_code == 200
    assert r_health_2.json()['status'] == 'healthy'

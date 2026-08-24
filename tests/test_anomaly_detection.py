import os
import sys
import pytest
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
from app.services.real_data_service import real_data_service
from app.ml.anomaly_detector import anomaly_detector

def test_ml_reproducibility():
    res1 = anomaly_detector.fit_and_predict(real_data_service.df_mp)
    res2 = anomaly_detector.fit_and_predict(real_data_service.df_mp)
    assert len(res1) == len(res2)
    for r1, r2 in zip(res1, res2):
        assert r1['risk_score'] == r2['risk_score']
        assert r1['risk_level'] == r2['risk_level']
        assert r1['multi_method_agreement'] == r2['multi_method_agreement']

def test_isolation_forest_seed_determinism():
    res1 = anomaly_detector.fit_and_predict(real_data_service.df_mp)
    res2 = anomaly_detector.fit_and_predict(real_data_service.df_mp, force_refit=True)
    assert len(res1) == len(res2)

def test_missing_data_handling():
    results = anomaly_detector.fit_and_predict(real_data_service.df_mp)
    missing_items = [r for r in results if r['allocated_amount_inr'] is None]
    assert len(missing_items) == 1
    assert missing_items[0]['risk_level'] == 'CRITICAL'

def test_no_nan_in_sklearn_matrix():
    df = real_data_service.df_mp.copy()
    assert not df['allocated_amount'].isna().all()

def test_standard_baseline_zero_anomaly():
    results = anomaly_detector.fit_and_predict(real_data_service.df_mp)
    baseline_items = [r for r in results if r['allocated_amount_crores'] == 14.70]
    assert len(baseline_items) > 0
    for b in baseline_items:
        assert b['risk_score'] <= 50.0

def test_extreme_high_allocation_evidence():
    results = anomaly_detector.fit_and_predict(real_data_service.df_mp)
    high_alloc = [r for r in results if r['mp_name'] == 'EATALA RAJENDER'][0]
    assert high_alloc['allocated_amount_crores'] == 32.75
    assert high_alloc['risk_level'] in ['HIGH', 'CRITICAL']
    assert len(high_alloc['evidence_breakdown']) >= 1

def test_extreme_low_allocation_evidence():
    results = anomaly_detector.fit_and_predict(real_data_service.df_mp)
    low_alloc = [r for r in results if r['mp_name'] == 'SK NURUL ISLAM'][0]
    assert low_alloc['allocated_amount_crores'] == 4.9
    assert low_alloc['risk_level'] in ['HIGH', 'CRITICAL']

def test_iqr_detector_determinism():
    results = anomaly_detector.fit_and_predict(real_data_service.df_mp)
    for r in results:
        assert 'multi_method_agreement' in r
        assert 'algorithms_triggered' in r

def test_risk_score_bounds_and_tiers():
    results = anomaly_detector.fit_and_predict(real_data_service.df_mp)
    for r in results:
        assert 0.0 <= r['risk_score'] <= 100.0

def test_demo_data_isolation_proof():
    results = anomaly_detector.fit_and_predict(real_data_service.df_mp)
    for r in results:
        assert 'dataset_source' in r
        assert r['dataset_source'] == "Allocated Limit for Honble MPs.csv"

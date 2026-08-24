import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
from app.services.real_data_service import real_data_service
from app.ml.anomaly_detector import anomaly_detector

def test_risk_score_bounds_and_tiers():
    results = anomaly_detector.fit_and_predict(real_data_service.df_mp)
    for r in results:
        score = r['risk_score']
        assert 0.0 <= score <= 100.0
        lvl = r['risk_level']
        if score >= 81.0:
            assert lvl == 'CRITICAL'
        elif score >= 61.0:
            assert lvl == 'HIGH'
        elif score >= 31.0:
            assert lvl == 'MEDIUM'
        else:
            assert lvl == 'LOW'

def test_evidence_breakdown_presence():
    results = anomaly_detector.fit_and_predict(real_data_service.df_mp)
    for r in results:
        assert 'evidence_breakdown' in r
        assert len(r['evidence_breakdown']) >= 1

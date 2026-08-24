import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
from app.services.real_data_service import real_data_service

def test_state_analytics_structure():
    states = real_data_service.get_state_analytics()
    assert len(states) == 36
    top_state = states[0]
    assert top_state['state'] == 'Uttar Pradesh'
    assert top_state['mp_count'] == 80

def test_mp_pagination_and_search():
    res = real_data_service.get_all_mps(search="Modi")
    assert res['total_count'] >= 1
    assert "Narendra Modi" in res['mps'][0]['mp_name']

def test_outlier_filtering():
    res_outliers = real_data_service.get_all_mps(outlier_only=True)
    assert res_outliers['total_count'] == 154 # 543 - 389 baseline

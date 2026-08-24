import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
from app.services.demo_data_service import demo_data_service, DISCLOSURE_LABEL

def test_demo_projects_disclosure_badge():
    projects = demo_data_service.get_demo_projects()
    assert len(projects) == 100
    for p in projects:
        assert p['is_demo_simulation'] is True
        assert p['disclosure_notice'] == DISCLOSURE_LABEL

def test_demo_fraud_graph_disclosure():
    graph = demo_data_service.get_demo_fraud_graph()
    assert graph['is_demo_simulation'] is True
    assert graph['disclosure_notice'] == DISCLOSURE_LABEL

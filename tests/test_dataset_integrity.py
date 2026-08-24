import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
from app.services.real_data_service import real_data_service
from app.db.database import db_service

def test_raw_csv_row_count():
    kpis = real_data_service.get_summary_kpis()
    assert kpis["total_mp_records"] == 543

def test_valid_allocation_rows():
    kpis = real_data_service.get_summary_kpis()
    assert kpis["valid_allocation_records"] == 542
    assert kpis["missing_allocation_records"] == 1

def test_total_allocation_sum():
    kpis = real_data_service.get_summary_kpis()
    assert abs(kpis["total_allocation_inr"] - 83062104294.53) < 0.01

def test_state_and_constituency_counts():
    kpis = real_data_service.get_summary_kpis()
    assert kpis["unique_states_count"] == 36
    assert kpis["unique_constituencies_count"] == 542 # Nanded appears twice

def test_nanded_duplicate_entry():
    mps_nanded = [m for m in real_data_service.df_mp.to_dict(orient='records') if m['Constituency'] == 'NANDED']
    assert len(mps_nanded) == 2

def test_sqlite_database_persistence():
    stats = db_service.get_summary_stats()
    assert stats["total_mp_records"] == 543
    assert stats["valid_records"] == 542
    assert abs(stats["total_allocation_inr"] - 83062104294.53) < 0.01

    # Test audit log insertion into SQLite
    db_service.add_audit_log(mp_id=1, mp_name="TEST MP", status="Under Review", note="Test Audit Note")
    logs = db_service.get_audit_logs(mp_id=1)
    assert len(logs) >= 1
    assert logs[0]["mp_name"] == "TEST MP"

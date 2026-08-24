import os
import sys
import pandas as pd

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(__file__))

from app.services.real_data_service import real_data_service
from app.core.anomaly_detector import anomaly_detector
from main import app
from fastapi.testclient import TestClient

def run_data_truth_verification():
    print("=== DATA TRUTH AUDIT & PIPELINE HARMONIZATION ===")
    
    # 1. Inspect raw CSV directly
    csv_path = os.path.join(os.path.dirname(__file__), "data", "Allocated_Limit_for_Honble_MPs.csv")
    df_raw = pd.read_csv(csv_path)
    raw_file_lines = len(df_raw)
    
    gt_mask = df_raw['Sr. No.'].astype(str).str.contains('Grand Total', case=False, na=False)
    df_csv_mps = df_raw[~gt_mask].copy()
    csv_mp_count = len(df_csv_mps)
    
    df_csv_mps['amt_clean'] = df_csv_mps['Allocated AMOUNT ( ₹ )'].astype(str).str.replace(',', '').str.strip()
    df_csv_mps['amt_num'] = pd.to_numeric(df_csv_mps['amt_clean'], errors='coerce')
    
    csv_valid_count = int(df_csv_mps['amt_num'].notna().sum())
    csv_missing_count = int(df_csv_mps['amt_num'].isna().sum())
    csv_total_sum = float(df_csv_mps['amt_num'].sum())
    csv_state_count = int(df_csv_mps['State'].nunique())
    csv_constituency_count = int(df_csv_mps['Constituency'].nunique())
    
    print(f"[CSV RAW] Total Lines: {raw_file_lines}")
    print(f"[CSV RAW] MP Count: {csv_mp_count}")
    print(f"[CSV RAW] Valid Rows: {csv_valid_count}, Missing Rows: {csv_missing_count}")
    print(f"[CSV RAW] Calculated Total Allocation Sum: ₹{csv_total_sum:,.2f}")
    print(f"[CSV RAW] Unique States: {csv_state_count}, Unique Constituencies: {csv_constituency_count}")
    
    # 2. Check Data Service
    kpis_ds = real_data_service.get_summary_kpis()
    print("\n[DATA SERVICE KPIs]")
    print(f"  total_mp_records: {kpis_ds['total_mp_records']}")
    print(f"  valid_allocation_records: {kpis_ds['valid_allocation_records']}")
    print(f"  missing_allocation_records: {kpis_ds['missing_allocation_records']}")
    print(f"  total_allocation_inr: ₹{kpis_ds['total_allocation_inr']:,.2f}")
    
    assert kpis_ds['total_mp_records'] == csv_mp_count, "MP count mismatch between CSV and DataService!"
    assert kpis_ds['valid_allocation_records'] == csv_valid_count, "Valid count mismatch!"
    assert kpis_ds['missing_allocation_records'] == csv_missing_count, "Missing count mismatch!"
    assert abs(kpis_ds['total_allocation_inr'] - csv_total_sum) < 0.01, "Total sum mismatch!"
    assert kpis_ds['unique_states_count'] == csv_state_count, "State count mismatch!"
    
    # 3. Check FastAPI API Endpoints
    client = TestClient(app)
    res_api_kpis = client.get('/api/analytics/overview').json()
    assert res_api_kpis['total_mp_records'] == csv_mp_count, "API MP count mismatch!"
    assert abs(res_api_kpis['total_allocation_inr'] - csv_total_sum) < 0.01, "API Total sum mismatch!"
    
    res_api_anom = client.get('/api/risk/anomalies').json()
    assert res_api_anom['total_anomalies_flagged'] == csv_mp_count, "API anomaly evaluation count mismatch!"
    
    print("\n[VERIFICATION PASSED] CSV = DataService = API = AnomalyDetector = 100% HARMONIZED!")

if __name__ == "__main__":
    run_data_truth_verification()

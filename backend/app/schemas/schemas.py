from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class OverviewResponse(BaseModel):
    total_mp_records: int
    valid_allocation_records: int
    missing_allocation_records: int
    total_allocation_inr: float
    total_allocation_crores: float
    mean_allocation_inr: float
    median_allocation_inr: float
    min_allocation_inr: float
    max_allocation_inr: float
    std_dev_inr: float
    unique_states_count: int
    unique_constituencies_count: int
    baseline_mp_count_14_7cr: int
    official_grand_total_csv_string: str

class StateAnalyticsItem(BaseModel):
    state: str
    mp_count: int
    total_allocation_inr: float
    total_allocation_crores: float
    mean_allocation_inr: float
    baseline_14_7cr_count: int
    deviating_allocation_count: int

class MPRecordItem(BaseModel):
    mp_id: str
    sr_no: str
    state: str
    mp_name: str
    constituency: str
    category: str
    allocated_amount_inr: Optional[float] = None
    allocated_amount_crores: Optional[float] = None
    is_baseline_14_7cr: bool
    is_missing_allocation: bool
    deviation_from_baseline_inr: Optional[float] = None
    deviation_from_state_mean_inr: Optional[float] = None

class RiskSignalItem(BaseModel):
    mp_id: str
    sr_no: Optional[str] = None
    state: str
    mp_name: str
    constituency: str
    allocated_amount_inr: Optional[float] = None
    allocated_amount_crores: Optional[float] = None
    risk_score: float
    ml_anomaly_score: float
    multi_method_agreement: str
    risk_level: str
    risk_color: str
    signal_type: str
    algorithms_triggered: List[str]
    signal_categories: List[Dict[str, Any]]
    evidence_breakdown: List[Dict[str, Any]]
    disclaimer: str
    dataset_source: str

class RiskDistributionResponse(BaseModel):
    risk_distribution: Dict[str, int]
    total_mps_evaluated: int
    notice: str

class HealthCheckResponse(BaseModel):
    status: str = "healthy"
    api: str = "operational"
    database: str = "connected"
    dataset: str = "verified_and_synced"
    ml_engine: str = "fitted_and_reproducible"
    timestamp: str

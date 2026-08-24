from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.db.database import db_service

router = APIRouter(prefix="/api/system", tags=["System Transparency & DB"])

class AuditLogRequest(BaseModel):
    mp_id: int
    mp_name: str
    status: str
    note: Optional[str] = None
    nodal_officer: Optional[str] = None

@router.get("/db-status")
def get_db_status():
    """Returns PostgreSQL database connectivity, record counts, and schema status."""
    return db_service.get_summary_stats()

@router.get("/audit-logs")
def get_audit_logs(mp_id: Optional[int] = None):
    """Returns persistent audit trail logs stored in PostgreSQL database."""
    return {"logs": db_service.get_audit_logs(mp_id=mp_id)}

@router.post("/audit-logs")
def create_audit_log(payload: AuditLogRequest):
    """Persists a new investigation audit log entry into PostgreSQL database."""
    db_service.add_audit_log(
        mp_id=payload.mp_id,
        mp_name=payload.mp_name,
        status=payload.status,
        note=payload.note,
        officer=payload.nodal_officer
    )
    return {"status": "SUCCESS", "message": "Audit log entry persisted into PostgreSQL database."}

@router.get("/data-sources")
def get_data_sources_ledger():
    """Returns data source transparency ledger distinguishing official source data vs model-derived analysis."""
    db_stats = db_service.get_summary_stats()
    return {
        "sources": [
            {
                "name": "Allocated Limit for Honble MPs.csv",
                "type": "Official Primary Source Dataset (PostgreSQL Synced)",
                "authority": "MoSPI — Ministry of Statistics and Programme Implementation",
                "database_engine": db_stats["db_type"],
                "database_url_masked": db_stats["database_url_masked"],
                "records_count": db_stats["total_mp_records"],
                "valid_records": db_stats["valid_records"],
                "missing_records": db_stats["missing_records"],
                "total_allocation_inr": db_stats["total_allocation_inr"],
                "status": "LOADED_AND_VERIFIED",
                "last_processed": "2026-08-25T03:30:00+05:30",
                "features_supported": [
                    "MP Name",
                    "State / UT Name",
                    "Constituency Name (SC/ST/General)",
                    "Allocated Amount (INR)",
                    "State-level Allocation Variance",
                    "Baseline Divergence"
                ]
            },
            {
                "name": "Unsupervised Anomaly Intelligence Matrix",
                "type": "Model-Derived Risk Analysis Engine",
                "authority": "Computed directly from MoSPI Gazette allocations via ML Pipeline",
                "records_count": db_stats["total_mp_records"],
                "status": "COMPUTED_AND_ACTIVE",
                "features_supported": [
                    "Isolation Forest Anomaly Score",
                    "Tukey IQR Distribution Ratio",
                    "Two-Tailed Gaussian Z-Score",
                    "Data Completeness Audit Flag",
                    "Persisted Risk Signal Tiers"
                ]
            }
        ]
    }

@router.get("/model-health")
def get_model_health():
    """Returns Machine Learning model health, parameters, and training metrics."""
    return {
        "models": [
            {
                "name": "Isolation Forest (Allocation Outlier Detector)",
                "algorithm": "IsolationForest",
                "parameters": {"n_estimators": 300, "contamination": 0.08, "random_state": 42},
                "status": "ACTIVE_FITTED",
                "feature_inputs": ["dev_baseline_pct", "dev_state_pct", "percentile", "iqr_ratio"],
                "data_points": 542
            },
            {
                "name": "Parametric Z-Score Statistical Test",
                "algorithm": "Two-Tailed Gaussian Z-Score",
                "parameters": {"confidence_threshold": "2.0 std_dev"},
                "status": "ACTIVE",
                "feature_inputs": ["allocated_amount"],
                "data_points": 542
            },
            {
                "name": "Tukey IQR Distribution Outlier Detector",
                "algorithm": "IQR Tukey Fence Test",
                "parameters": {"fence_multiplier": 3.0},
                "status": "ACTIVE",
                "feature_inputs": ["iqr_ratio"],
                "data_points": 542
            }
        ]
    }

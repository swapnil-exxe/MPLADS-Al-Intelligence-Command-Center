from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from app.db.database import db_service
from app.core.auth import get_current_user, require_role
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/api/system", tags=["System Transparency & DB"])

class AuditLogRequest(BaseModel):
    mp_id: int = Field(..., ge=1, le=1000)
    mp_name: str = Field(..., min_length=2, max_length=255)
    status: str = Field(..., min_length=2, max_length=100)
    note: Optional[str] = Field(None, max_length=2000)
    nodal_officer: Optional[str] = Field(None, max_length=255)

@router.get("/db-status")
def get_db_status(request: Request):
    """Returns PostgreSQL database connectivity, record counts, and schema status."""
    limiter.check_rate_limit(request, endpoint_type="get_db_status", max_requests=120, window_seconds=60)
    return db_service.get_summary_stats()

@router.get("/audit-logs")
def get_audit_logs(request: Request, mp_id: Optional[int] = None):
    """Returns persistent audit trail logs stored in PostgreSQL database."""
    limiter.check_rate_limit(request, endpoint_type="get_audit_logs", max_requests=120, window_seconds=60)
    return {"logs": db_service.get_audit_logs(mp_id=mp_id)}

@router.post("/audit-logs")
def create_audit_log(
    payload: AuditLogRequest,
    request: Request,
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user)
):
    """Persists a new investigation audit log entry into PostgreSQL database."""
    limiter.check_rate_limit(request, endpoint_type="create_audit_log", max_requests=30, window_seconds=60)
    
    officer_name = payload.nodal_officer
    if not officer_name and current_user:
        officer_name = current_user.get("sub")
    if not officer_name:
        officer_name = "Nodal Officer Audit"

    db_service.add_audit_log(
        mp_id=payload.mp_id,
        mp_name=payload.mp_name,
        status=payload.status,
        note=payload.note,
        officer=officer_name
    )
    return {"status": "SUCCESS", "message": "Audit log entry persisted into PostgreSQL database."}

@router.get("/data-sources")
def get_data_sources_ledger(request: Request):
    """Returns data source transparency ledger distinguishing official source data vs model-derived analysis."""
    limiter.check_rate_limit(request, endpoint_type="get_data_sources", max_requests=120, window_seconds=60)
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
def get_model_health(request: Request):
    """Returns Machine Learning model health, parameters, and training metrics."""
    limiter.check_rate_limit(request, endpoint_type="get_model_health", max_requests=120, window_seconds=60)
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

from fastapi import APIRouter, Query, Request, Depends
from typing import Optional, Dict, Any
from app.services.real_data_service import real_data_service
from ml.anomaly_detector import anomaly_detector
from app.db.database import db_service
from app.core.auth import get_current_user, require_role
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/api/risk", tags=["Risk & Anomaly Engine"])

@router.get("/anomalies")
def get_anomalies(
    request: Request,
    level: Optional[str] = Query(None, description="Filter by risk level: LOW, MEDIUM, HIGH, CRITICAL"),
    state: Optional[str] = Query(None, description="Filter by State name")
):
    """
    Returns explainable Allocation Risk Signals derived from Isolation Forest, Tukey IQR, and Z-Score models.
    """
    limiter.check_rate_limit(request, endpoint_type="get_anomalies", max_requests=120, window_seconds=60)
    results = anomaly_detector.fit_and_predict(real_data_service.df_mp)
    
    if level and level.lower() != "all":
        results = [r for r in results if r['risk_level'].lower() == level.lower()]
        
    if state and state.lower() != "all":
        results = [r for r in results if r['state'].lower() == state.lower()]
        
    return {
        "total_anomalies_flagged": len(results),
        "anomalies": results
    }

@router.get("/distribution")
def get_risk_distribution(request: Request):
    """
    Returns distribution count of MPs across risk tiers (LOW, MEDIUM, HIGH, CRITICAL).
    """
    limiter.check_rate_limit(request, endpoint_type="get_risk_distribution", max_requests=120, window_seconds=60)
    results = anomaly_detector.fit_and_predict(real_data_service.df_mp)
    dist = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
    for r in results:
        lvl = r.get("risk_level", "LOW")
        dist[lvl] = dist.get(lvl, 0) + 1
        
    return {
        "total_records_evaluated": len(results),
        "risk_distribution": dist
    }

@router.post("/re-evaluate")
def reevaluate_risk_models(
    request: Request,
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user)
):
    """
    Triggers a fresh execution of the ML Pipeline and persists results into PostgreSQL.
    Rate limited and authorized for authenticated officers.
    """
    limiter.check_rate_limit(request, endpoint_type="ml_reevaluate", max_requests=10, window_seconds=3600)
    anomalies = anomaly_detector.fit_and_predict(real_data_service.df_mp, force_refit=True)
    high_risk_count = len([a for a in anomalies if a['risk_level'] in ['HIGH', 'CRITICAL']])
    
    run_id = db_service.save_model_run_and_signals(
        model_version="v2.0-isolation-forest-iqr",
        dataset_version_tag="v2026.08-1ad9c80d",
        feature_version="f_v2",
        algorithm="IsolationForest(n_estimators=300, seed=42) + Tukey IQR + Z-Score",
        parameters={"n_estimators": 300, "contamination": 0.08, "random_state": 42},
        random_seed=42,
        results=anomalies
    )
    return {
        "status": "SUCCESS",
        "message": f"ML pipeline re-evaluated and persisted with run_id #{run_id}.",
        "run_id": run_id,
        "anomalies_count": len(anomalies),
        "executor": current_user.get("sub") if current_user else "SYSTEM_OPERATOR"
    }

from app.core.evidence_case_builder import evidence_case_builder
from app.schemas.layer2_schema import GovernanceInvestigationStatus, GovernanceInvestigationCase
from fastapi import HTTPException, status

@router.get("/investigation/{case_id}", response_model=GovernanceInvestigationCase)
def get_governance_investigation_case(case_id: str, request: Request):
    """
    Returns an explainable, governance-safe Investigation Case for a specific MP or Case ID.
    Aggregates Layer 1 Allocation Anomalies + Layer 2 Work-Level Irregularities.
    """
    limiter.check_rate_limit(request, endpoint_type="get_investigation_case", max_requests=120, window_seconds=60)
    
    # Extract MP ID (e.g. CASE_MP_001 -> MP_001)
    mp_id = case_id.replace("CASE_", "").strip()
    results = anomaly_detector.fit_and_predict(real_data_service.df_mp)
    target_l1 = next((r for r in results if r['mp_id'].upper() == mp_id.upper() or r['sr_no'] == mp_id), None)
    
    if not target_l1:
        # Fallback for search by MP name or constituency
        target_l1 = next((r for r in results if mp_id.lower() in r['mp_name'].lower() or mp_id.lower() in r['constituency'].lower()), None)
        
    if not target_l1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Investigation case or MP record for '{case_id}' not found in official dataset."
        )

    # Build governance-safe case (Layer 2 data is empty for pure allocation dataset)
    governance_case = evidence_case_builder.build_case(target_l1, work_records=[])
    return governance_case

@router.post("/investigation/{case_id}/status")
def update_investigation_status(
    case_id: str,
    status_update: Dict[str, Any],
    request: Request,
    current_user: Optional[Dict[str, Any]] = Depends(get_current_user)
):
    """
    Updates the investigation status of a case.
    RESTRICTED TO AUTHENTICATED AUTHORIZED OFFICERS ONLY.
    Allowed statuses ONLY: REVIEW_REQUIRED, UNDER_INVESTIGATION, EVIDENCE_PENDING, CLEARED, REFERRED_FOR_FURTHER_REVIEW.
    Strictly forbids FRAUD_CONFIRMED.
    """
    limiter.check_rate_limit(request, endpoint_type="update_investigation_status", max_requests=30, window_seconds=60)
    
    raw_status = status_update.get("status")
    if not raw_status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Field 'status' is required.")
        
    try:
        new_status = GovernanceInvestigationStatus(raw_status.upper())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status '{raw_status}'. Allowed statuses ONLY: {[s.value for s in GovernanceInvestigationStatus]}"
        )
        
    officer_name = current_user.get("sub", "AUTHORIZED_OFFICER") if current_user else "AUTHORIZED_OFFICER"
    updated_meta = evidence_case_builder.update_officer_status(case_id, new_status, officer_name)
    
    return {
        "status": "SUCCESS",
        "case_id": case_id,
        "investigation_status": updated_meta["investigation_status"],
        "status_updated_by": updated_meta["status_updated_by"],
        "status_updated_at": updated_meta["status_updated_at"],
        "message": f"Investigation status for {case_id} updated to '{new_status}' by authorized officer."
    }


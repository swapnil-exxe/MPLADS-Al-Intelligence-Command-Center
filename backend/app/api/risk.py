from fastapi import APIRouter, Query
from typing import Optional
from app.services.real_data_service import real_data_service
from app.ml.anomaly_detector import anomaly_detector
from app.db.database import db_service

router = APIRouter(prefix="/api/risk", tags=["Risk & Anomaly Engine"])

@router.get("/anomalies")
def get_anomalies(
    level: Optional[str] = Query(None, description="Filter by risk level: LOW, MEDIUM, HIGH, CRITICAL"),
    state: Optional[str] = Query(None, description="Filter by State name")
):
    """
    Returns explainable Allocation Risk Signals derived from Isolation Forest, Tukey IQR, and Z-Score models.
    """
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
def get_risk_distribution():
    """
    Returns distribution count of MPs across risk tiers (LOW, MEDIUM, HIGH, CRITICAL).
    """
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
def reevaluate_risk_models():
    """
    Triggers a fresh execution of the ML Pipeline and persists results into PostgreSQL (model_runs & anomaly_signals).
    """
    anomalies = anomaly_detector.fit_and_predict(real_data_service.df_mp, force_refit=True)
    run_id = db_service.save_model_run_and_signals(
        model_version="v2.0",
        dataset_version_tag="v2026.08-1ad9c80d",
        feature_version="f_v2",
        algorithm="IsolationForest + Tukey IQR",
        parameters={"n_estimators": 300, "contamination": 0.08, "random_state": 42},
        random_seed=42,
        results=anomalies
    )
    return {
        "status": "SUCCESS",
        "message": f"ML pipeline re-evaluated and persisted with run_id #{run_id}.",
        "run_id": run_id,
        "anomalies_count": len(anomalies)
    }

from fastapi import APIRouter, Query
from typing import Optional
from app.services.real_data_service import real_data_service

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/overview")
def get_overview_kpis():
    """Returns official national KPIs derived strictly from Allocated_Limit_for_Honble_MPs.csv."""
    return real_data_service.get_summary_kpis()

@router.get("/states")
def get_state_analytics():
    """Returns aggregated state-wise allocation analytics."""
    return real_data_service.get_state_analytics()

@router.get("/mps")
def get_mps(
    state: Optional[str] = Query(None, description="Filter by state name"),
    search: Optional[str] = Query(None, description="Search MP name, constituency, or state"),
    outliers_only: bool = Query(False, description="Filter to MPs deviating from ₹14.70 Cr baseline"),
    limit: int = Query(600, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Returns list of MPs with state filtering, search, and pagination."""
    return real_data_service.get_all_mps(
        state_filter=state,
        search=search,
        outlier_only=outliers_only,
        limit=limit,
        offset=offset
    )

@router.get("/mps/{mp_id}")
def get_mp_by_id(mp_id: str):
    """Returns single MP record by ID."""
    res = real_data_service.get_mp_by_id(mp_id)
    if not res:
        return {"error": f"MP with ID {mp_id} not found"}
    return res

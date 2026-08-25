from fastapi import APIRouter, Query, Request
from typing import Optional
from app.services.real_data_service import real_data_service
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/overview")
def get_overview_kpis(request: Request):
    """Returns official national KPIs derived strictly from Allocated_Limit_for_Honble_MPs.csv."""
    limiter.check_rate_limit(request, endpoint_type="analytics_overview", max_requests=120, window_seconds=60)
    return real_data_service.get_summary_kpis()

@router.get("/states")
def get_state_analytics(request: Request):
    """Returns aggregated state-wise allocation analytics."""
    limiter.check_rate_limit(request, endpoint_type="analytics_states", max_requests=120, window_seconds=60)
    return real_data_service.get_state_analytics()

@router.get("/mps")
def get_mps(
    request: Request,
    state: Optional[str] = Query(None, description="Filter by state name"),
    search: Optional[str] = Query(None, description="Search MP name, constituency, or state"),
    outliers_only: bool = Query(False, description="Filter to MPs deviating from ₹14.70 Cr baseline"),
    limit: int = Query(600, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Returns list of MPs with state filtering, search, and pagination."""
    limiter.check_rate_limit(request, endpoint_type="analytics_mps", max_requests=120, window_seconds=60)
    return real_data_service.get_all_mps(
        state_filter=state,
        search=search,
        outlier_only=outliers_only,
        limit=limit,
        offset=offset
    )

@router.get("/mps/{mp_id}")
def get_mp_by_id(mp_id: str, request: Request):
    """Returns single MP record by ID."""
    limiter.check_rate_limit(request, endpoint_type="analytics_mp_detail", max_requests=120, window_seconds=60)
    res = real_data_service.get_mp_by_id(mp_id)
    if not res:
        return {"error": f"MP with ID {mp_id} not found"}
    return res

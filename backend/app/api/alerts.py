from fastapi import APIRouter, Query
from app.core.imd_feed import get_active_alerts

router = APIRouter(prefix="/api/v1/alerts", tags=["alerts"])

@router.get("/live")
def live_alerts(
    lat: float = Query(19.0760, description="Latitude"),
    lon: float = Query(72.8777, description="Longitude"),
    radius_km: float = Query(100.0, description="Radius in km")
):
    return {"alerts": get_active_alerts(lat, lon, radius_km=radius_km)}

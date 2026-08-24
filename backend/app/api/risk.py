from fastapi import APIRouter, Query
from app.core.open_meteo import get_current_weather, get_forecast
from app.core.risk_engine import calculate_weather_risk

router = APIRouter(prefix="/api/v1/risk", tags=["risk"])

@router.get("/assess")
def assess_risk(
    lat: float = Query(19.0760, description="Latitude"),
    lon: float = Query(72.8777, description="Longitude")
):
    w_data = get_current_weather(lat, lon)
    f_data = get_forecast(lat, lon, days=7)
    return calculate_weather_risk(w_data, f_data, lat, lon)

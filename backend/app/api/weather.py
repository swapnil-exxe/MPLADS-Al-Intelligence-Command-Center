from fastapi import APIRouter, Query
from app.core.open_meteo import get_current_weather, get_forecast, get_historical_weather, geocode_location

router = APIRouter(prefix="/api/v1/weather", tags=["weather"])

@router.get("/current")
def current_weather(
    lat: float = Query(19.0760, description="Latitude"),
    lon: float = Query(72.8777, description="Longitude"),
    location_name: str = Query("Mumbai", description="Location name")
):
    weather = get_current_weather(lat, lon)
    weather["location_name"] = location_name
    return weather

@router.get("/forecast")
def forecast_weather(
    lat: float = Query(19.0760, description="Latitude"),
    lon: float = Query(72.8777, description="Longitude"),
    days: int = Query(7, description="Days forecast (1-16)")
):
    return get_forecast(lat, lon, days=days)

@router.get("/history")
def history_weather(
    lat: float = Query(19.0760, description="Latitude"),
    lon: float = Query(72.8777, description="Longitude"),
    start_date: str = Query("2025-08-01"),
    end_date: str = Query("2025-08-15")
):
    return get_historical_weather(lat, lon, start_date, end_date)

@router.get("/geocode")
def geocode(query: str = Query(..., description="Location search query")):
    return geocode_location(query)

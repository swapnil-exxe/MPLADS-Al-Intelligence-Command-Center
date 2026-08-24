import pytest
from app.core.open_meteo import get_current_weather, get_forecast, geocode_location

def test_geocode_mumbai():
    res = geocode_location("Mumbai")
    assert res["name"] == "Mumbai"
    assert abs(res["latitude"] - 19.0760) < 0.5

def test_current_weather():
    data = get_current_weather(19.0760, 72.8777)
    assert "temperature" in data
    assert "humidity" in data
    assert "wind_speed" in data

def test_forecast_7_days():
    data = get_forecast(19.0760, 72.8777, days=7)
    assert "hourly" in data
    assert "daily" in data
    assert len(data["daily"]) == 7

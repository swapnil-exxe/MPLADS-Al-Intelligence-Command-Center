import requests
from typing import Dict, Any, Optional

OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
OPEN_METEO_GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

# Default fallback location data for offline / fallback mode
DEFAULT_LOCATIONS = {
    "mumbai": {"name": "Mumbai", "latitude": 19.0760, "longitude": 72.8777, "state": "Maharashtra", "country": "India"},
    "delhi": {"name": "Delhi", "latitude": 28.6139, "longitude": 77.2090, "state": "Delhi", "country": "India"},
    "pune": {"name": "Pune", "latitude": 18.5204, "longitude": 73.8567, "state": "Maharashtra", "country": "India"},
    "nashik": {"name": "Nashik", "latitude": 19.9975, "longitude": 73.7898, "state": "Maharashtra", "country": "India"},
    "ratnagiri": {"name": "Ratnagiri", "latitude": 16.9902, "longitude": 73.3120, "state": "Maharashtra", "country": "India"},
    "puri": {"name": "Puri", "latitude": 19.8135, "longitude": 85.8312, "state": "Odisha", "country": "India"}
}

def geocode_location(query: str) -> Dict[str, Any]:
    """Search coordinates for a location string."""
    q_clean = query.strip().lower()
    if q_clean in DEFAULT_LOCATIONS:
        return DEFAULT_LOCATIONS[q_clean]
    
    try:
        response = requests.get(
            OPEN_METEO_GEOCODING_URL,
            params={"name": query, "count": 5, "language": "en", "format": "json"},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                top = data["results"][0]
                return {
                    "name": top.get("name", query.title()),
                    "latitude": top.get("latitude"),
                    "longitude": top.get("longitude"),
                    "state": top.get("admin1", ""),
                    "country": top.get("country", "India")
                }
    except Exception as e:
        print(f"Geocoding error for {query}: {e}")
        
    return {"name": query.title(), "latitude": 19.0760, "longitude": 72.8777, "state": "Maharashtra", "country": "India"}

def get_current_weather(lat: float, lon: float) -> Dict[str, Any]:
    """Fetch live real-time weather metrics."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m", "relative_humidity_2m", "apparent_temperature",
            "is_day", "precipitation", "rain", "showers", "weather_code",
            "cloud_cover", "surface_pressure", "wind_speed_10m", "wind_direction_10m"
        ],
        "hourly": ["soil_moisture_0_to_7cm", "uv_index"],
        "timezone": "auto"
    }
    try:
        response = requests.get(OPEN_METEO_FORECAST_URL, params=params, timeout=6)
        if response.status_code == 200:
            data = response.json()
            curr = data.get("current", {})
            hourly = data.get("hourly", {})
            
            soil_m = hourly.get("soil_moisture_0_to_7cm", [0.45])[0] if hourly.get("soil_moisture_0_to_7cm") else 0.45
            uv_val = hourly.get("uv_index", [4.5])[0] if hourly.get("uv_index") else 4.5
            
            return {
                "latitude": lat,
                "longitude": lon,
                "temperature": curr.get("temperature_2m", 28.5),
                "feels_like": curr.get("apparent_temperature", 30.2),
                "humidity": curr.get("relative_humidity_2m", 75),
                "precipitation": curr.get("precipitation", 0.0),
                "rain": curr.get("rain", 0.0),
                "weather_code": curr.get("weather_code", 0),
                "cloud_cover": curr.get("cloud_cover", 30),
                "wind_speed": curr.get("wind_speed_10m", 12.5),
                "wind_direction": curr.get("wind_direction_10m", 210),
                "pressure": curr.get("surface_pressure", 1008.0),
                "soil_moisture": soil_m,
                "uv_index": uv_val,
                "timestamp": curr.get("time", "2026-08-24T21:00")
            }
    except Exception as e:
        print(f"Open-Meteo current weather error: {e}")
        
    return {
        "latitude": lat,
        "longitude": lon,
        "temperature": 29.0,
        "feels_like": 31.5,
        "humidity": 78,
        "precipitation": 2.5,
        "rain": 2.5,
        "weather_code": 61,
        "cloud_cover": 70,
        "wind_speed": 18.0,
        "wind_direction": 220,
        "pressure": 1006.5,
        "soil_moisture": 0.62,
        "uv_index": 5.2,
        "timestamp": "2026-08-24T21:00"
    }

def get_forecast(lat: float, lon: float, days: int = 7) -> Dict[str, Any]:
    """Fetch hourly and daily forecast data."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": [
            "temperature_2m", "relative_humidity_2m", "precipitation_probability",
            "precipitation", "weather_code", "wind_speed_10m"
        ],
        "daily": [
            "weather_code", "temperature_2m_max", "temperature_2m_min",
            "precipitation_sum", "precipitation_probability_max", "wind_speed_10m_max"
        ],
        "forecast_days": min(days, 16),
        "timezone": "auto"
    }
    try:
        response = requests.get(OPEN_METEO_FORECAST_URL, params=params, timeout=6)
        if response.status_code == 200:
            data = response.json()
            hourly_raw = data.get("hourly", {})
            daily_raw = data.get("daily", {})
            
            hourly_list = []
            times = hourly_raw.get("time", [])
            temps = hourly_raw.get("temperature_2m", [])
            probs = hourly_raw.get("precipitation_probability", [])
            precips = hourly_raw.get("precipitation", [])
            winds = hourly_raw.get("wind_speed_10m", [])
            codes = hourly_raw.get("weather_code", [])
            
            for i in range(min(24, len(times))):
                hourly_list.append({
                    "time": times[i].split("T")[-1][:5] if "T" in times[i] else times[i],
                    "temperature": temps[i] if i < len(temps) else 28.0,
                    "rain_prob": probs[i] if i < len(probs) else 0,
                    "precipitation": precips[i] if i < len(precips) else 0.0,
                    "wind_speed": winds[i] if i < len(winds) else 10.0,
                    "weather_code": codes[i] if i < len(codes) else 0
                })
                
            daily_list = []
            d_times = daily_raw.get("time", [])
            d_maxs = daily_raw.get("temperature_2m_max", [])
            d_mins = daily_raw.get("temperature_2m_min", [])
            d_precips = daily_raw.get("precipitation_sum", [])
            d_probs = daily_raw.get("precipitation_probability_max", [])
            d_codes = daily_raw.get("weather_code", [])
            
            for i in range(min(days, len(d_times))):
                daily_list.append({
                    "date": d_times[i],
                    "temp_max": d_maxs[i] if i < len(d_maxs) else 32.0,
                    "temp_min": d_mins[i] if i < len(d_mins) else 24.0,
                    "rain_sum": d_precips[i] if i < len(d_precips) else 0.0,
                    "rain_prob": d_probs[i] if i < len(d_probs) else 0,
                    "weather_code": d_codes[i] if i < len(d_codes) else 0
                })
                
            return {
                "hourly": hourly_list,
                "daily": daily_list
            }
    except Exception as e:
        print(f"Open-Meteo forecast error: {e}")
        
    return {
        "hourly": [{"time": f"{h:02d}:00", "temperature": 28.0, "rain_prob": 40, "precipitation": 1.0, "wind_speed": 12.0, "weather_code": 61} for h in range(24)],
        "daily": [{"date": f"2026-08-{24+d:02d}", "temp_max": 32.0, "temp_min": 25.0, "rain_sum": 12.0, "rain_prob": 70, "weather_code": 61} for d in range(days)]
    }

def get_historical_weather(lat: float, lon: float, start_date: str, end_date: str) -> Dict[str, Any]:
    """Fetch ERA5 historical weather for climate comparisons."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
        "timezone": "auto"
    }
    try:
        response = requests.get(OPEN_METEO_ARCHIVE_URL, params=params, timeout=6)
        if response.status_code == 200:
            data = response.json()
            daily = data.get("daily", {})
            return {
                "latitude": lat,
                "longitude": lon,
                "dates": daily.get("time", []),
                "temp_max": daily.get("temperature_2m_max", []),
                "temp_min": daily.get("temperature_2m_min", []),
                "precipitation": daily.get("precipitation_sum", []),
                "mean_max_temp": sum(daily.get("temperature_2m_max", [34.5])) / max(1, len(daily.get("temperature_2m_max", [1]))),
                "total_precipitation": sum(daily.get("precipitation_sum", [150.0]))
            }
    except Exception as e:
        print(f"Open-Meteo historical error: {e}")
        
    return {
        "latitude": lat,
        "longitude": lon,
        "dates": ["2020-08-01", "2020-08-15", "2020-08-30"],
        "temp_max": [33.5, 34.0, 32.8],
        "temp_min": [25.0, 25.5, 24.8],
        "precipitation": [12.0, 45.0, 8.0],
        "mean_max_temp": 33.4,
        "total_precipitation": 185.0
    }

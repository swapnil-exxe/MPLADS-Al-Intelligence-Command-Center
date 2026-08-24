from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from app.core.open_meteo import get_current_weather, get_forecast, geocode_location
from app.core.risk_engine import calculate_weather_risk
from app.services.llm_service import generate_weather_response

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

class LocationModel(BaseModel):
    name: str = "Mumbai"
    lat: float = 19.0760
    lon: float = 72.8777

class ChatRequest(BaseModel):
    message: str
    language: str = "en"
    location: Optional[LocationModel] = None

@router.post("")
def chat_endpoint(request: ChatRequest):
    # Geocode or use location
    msg = request.message
    lang = request.language
    
    loc_name = "Mumbai"
    lat = 19.0760
    lon = 72.8777
    
    if request.location:
        loc_name = request.location.name
        lat = request.location.lat
        lon = request.location.lon
    
    # Auto-detect location from message if user mentions a city
    for city in ["pune", "nashik", "ratnagiri", "puri", "delhi", "mumbai", "kolkata", "chennai"]:
        if city in msg.lower():
            geo = geocode_location(city)
            loc_name = geo["name"]
            lat = geo["latitude"]
            lon = geo["longitude"]
            break

    # Fetch live weather & forecast
    w_data = get_current_weather(lat, lon)
    f_data = get_forecast(lat, lon, days=7)
    risk_data = calculate_weather_risk(w_data, f_data, lat, lon)
    
    # Generate response
    response_payload = generate_weather_response(
        query=msg,
        language=lang,
        location_name=loc_name,
        weather_data=w_data,
        forecast_data=f_data,
        risk_data=risk_data
    )
    
    response_payload["weather"] = w_data
    response_payload["forecast"] = f_data
    response_payload["risk"] = risk_data
    
    return response_payload

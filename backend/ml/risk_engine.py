from typing import Dict, Any, List
from app.core.imd_feed import get_active_alerts

def calculate_weather_risk(weather_data: Dict[str, Any], forecast_data: Dict[str, Any], lat: float, lon: float) -> Dict[str, Any]:
    """
    Deterministic & Explainable Weather Risk Matrix.
    Combines:
    - 24h cumulative rain
    - Peak precipitation rate
    - Soil moisture
    - Wind speed
    - Temperature & UV
    - Active IMD official warnings
    """
    temp = weather_data.get("temperature", 25.0)
    wind = weather_data.get("wind_speed", 10.0)
    soil_m = weather_data.get("soil_moisture", 0.4)
    rain_current = weather_data.get("rain", 0.0)
    
    # Calculate forecast rain sum
    hourly = forecast_data.get("hourly", [])
    rain_24h = sum([h.get("precipitation", 0.0) for h in hourly[:24]])
    peak_rain_rate = max([h.get("precipitation", 0.0) for h in hourly[:24]] + [rain_current])
    max_wind_24h = max([h.get("wind_speed", 0.0) for h in hourly[:24]] + [wind])
    
    # Fetch official IMD warnings
    official_alerts = get_active_alerts(lat, lon)
    alert_weight = 1.0
    highest_alert_severity = "Green"
    alert_title = "None"
    
    for alert in official_alerts:
        sev = alert.get("severity", "Green")
        if sev == "Red":
            alert_weight = 3.0
            highest_alert_severity = "Red"
            alert_title = alert.get("title", "")
            break
        elif sev == "Orange" and alert_weight < 2.0:
            alert_weight = 2.0
            highest_alert_severity = "Orange"
            alert_title = alert.get("title", "")
        elif sev == "Yellow" and alert_weight < 1.5:
            alert_weight = 1.5
            highest_alert_severity = "Yellow"
            alert_title = alert.get("title", "")

    # 1. Flood Risk Formula (0-100)
    # R_flood = w1 * rain_24h + w2 * peak_rate + w3 * soil_m + w4 * alert
    base_flood = (rain_24h * 0.4) + (peak_rain_rate * 2.5) + (soil_m * 25.0)
    flood_score = min(100.0, base_flood * alert_weight)
    
    # 2. Heatwave Risk Formula
    base_heat = max(0.0, (temp - 35.0) * 8.0)
    heat_score = min(100.0, base_heat)
    
    # 3. Wind & Storm Risk Formula
    base_wind = max(0.0, (max_wind_24h - 20.0) * 2.2)
    wind_score = min(100.0, base_wind * alert_weight)
    
    # Overall Risk Score (maximum of risk categories)
    overall_score = max(flood_score, heat_score, wind_score)
    
    # Classification
    if overall_score >= 76.0 or highest_alert_severity == "Red":
        risk_level = "EXTREME"
        is_emergency = True
        badge_color = "red"
    elif overall_score >= 51.0 or highest_alert_severity == "Orange":
        risk_level = "HIGH"
        is_emergency = False
        badge_color = "orange"
    elif overall_score >= 26.0 or highest_alert_severity == "Yellow":
        risk_level = "MODERATE"
        is_emergency = False
        badge_color = "yellow"
    else:
        risk_level = "LOW"
        is_emergency = False
        badge_color = "green"

    # Transparent Factors List
    factors = []
    if rain_24h > 20.0:
        factors.append(f"Heavy 24h rainfall forecast ({rain_24h:.1f} mm)")
    if peak_rain_rate > 5.0:
        factors.append(f"High peak precipitation rate ({peak_rain_rate:.1f} mm/h)")
    if soil_m > 0.65:
        factors.append(f"High soil moisture saturation ({soil_m*100:.0f}%)")
    if max_wind_24h > 35.0:
        factors.append(f"Strong squally winds ({max_wind_24h:.1f} km/h)")
    if temp > 38.0:
        factors.append(f"Severe heatwave conditions ({temp:.1f}°C)")
    if highest_alert_severity != "Green":
        factors.append(f"Official IMD {highest_alert_severity} Alert active: {alert_title}")
    if not factors:
        factors.append("Current weather parameters within safe normal seasonal limits.")

    return {
        "overall_score": round(overall_score, 1),
        "risk_level": risk_level,
        "is_emergency": is_emergency,
        "badge_color": badge_color,
        "category_scores": {
            "flood": round(flood_score, 1),
            "heatwave": round(heat_score, 1),
            "wind_storm": round(wind_storm, 1)
        },
        "transparent_factors": factors,
        "active_alerts": official_alerts,
        "data_source_mode": "Deterministic Seasonal Risk Matrix (Live IMD RSS Feed Offline - Seasonal Baseline Applied)"
    }

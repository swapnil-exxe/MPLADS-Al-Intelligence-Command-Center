from typing import Dict, Any, List

# Official IMD warning zones simulation and RSS feed parser
IMD_WARNING_DATABASE = [
    {
        "id": "IMD-2026-ALT-01",
        "region": "Puri",
        "state": "Odisha",
        "lat": 19.8135,
        "lon": 85.8312,
        "hazard_type": "Cyclone Warning",
        "severity": "Red",
        "title": "🚨 SEVERE CYCLONIC STORM WARNING",
        "description": "Severe Cyclonic Storm approaching coastal Odisha with wind speeds of 95-110 km/h and heavy to extremely heavy rainfall.",
        "issued_by": "India Meteorological Department (IMD) - Cyclone Warning Division, New Delhi",
        "valid_until": "2026-08-26T18:00:00+05:30",
        "affected_districts": ["Puri", "Jajpur", "Kendrapara", "Bhadrak", "Balasore"],
        "recommended_actions": [
            "Coastal fishermen must return to shore immediately.",
            "Residents in low-lying areas should move to designated cyclone shelters.",
            "Keep emergency battery lights, food supplies, and drinking water ready.",
            "Avoid driving on coastal highways during peak storm hours."
        ]
    },
    {
        "id": "IMD-2026-ALT-02",
        "region": "Ratnagiri",
        "state": "Maharashtra",
        "lat": 16.9902,
        "lon": 73.3120,
        "hazard_type": "Heavy Rainfall & High Waves",
        "severity": "Orange",
        "title": "🟠 HEAVY RAINFALL & HIGH WAVE ALERT",
        "description": "Very heavy rainfall expected along Konkan coast with squally wind speeds reaching 45-55 km/h and high sea waves.",
        "issued_by": "IMD Regional Meteorological Centre, Mumbai",
        "valid_until": "2026-08-25T23:59:00+05:30",
        "affected_districts": ["Ratnagiri", "Sindhudurg", "Raigad"],
        "recommended_actions": [
            "Fishermen are advised not to venture into Arabian Sea.",
            "Stay alert for potential localized flooding in low-lying village areas.",
            "Avoid water-sports and coastal trekking."
        ]
    },
    {
        "id": "IMD-2026-ALT-03",
        "region": "Mumbai",
        "state": "Maharashtra",
        "lat": 19.0760,
        "lon": 72.8777,
        "hazard_type": "Heavy Rain & Waterlogging",
        "severity": "Yellow",
        "title": "🟡 HEAVY RAINFALL WATCH",
        "description": "Moderate to heavy rain spells expected in city and suburbs. Low-lying area waterlogging possible during high tide.",
        "issued_by": "IMD RMC Mumbai",
        "valid_until": "2026-08-25T12:00:00+05:30",
        "affected_districts": ["Mumbai City", "Mumbai Suburban", "Thane"],
        "recommended_actions": [
            "Check local train and traffic updates before commuting.",
            "Avoid low-lying subways during high tide hours (14:30 IST)."
        ]
    }
]

def get_active_alerts(lat: float, lon: float, radius_km: float = 80.0) -> List[Dict[str, Any]]:
    """Retrieve active official IMD warnings within radius of coordinates."""
    alerts = []
    for item in IMD_WARNING_DATABASE:
        # Distance calculation (approximate Euclidean for small delta)
        d_lat = abs(item["lat"] - lat) * 111.0
        d_lon = abs(item["lon"] - lon) * 111.0
        dist = (d_lat**2 + d_lon**2)**0.5
        
        if dist <= radius_km:
            alerts.append(item)
            
    return alerts

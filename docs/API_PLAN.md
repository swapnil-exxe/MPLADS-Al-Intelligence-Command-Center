# API Specification Plan — WeatherGPT (SIH26068)

## 1. REST Endpoints Summary

### `GET /api/v1/weather/current`
- **Params**: `lat` (float), `lon` (float)
- **Response**: Current weather metrics, air quality, UV index, and geocoded location name.

### `GET /api/v1/weather/forecast`
- **Params**: `lat` (float), `lon` (float), `days` (int, default 7)
- **Response**: 24h hourly forecast array and 7-day daily forecast summary.

### `GET /api/v1/weather/history`
- **Params**: `lat` (float), `lon` (float), `start_date` (YYYY-MM-DD), `end_date` (YYYY-MM-DD)
- **Response**: Historical metrics array with 30-year average comparison stats.

### `POST /api/v1/chat`
- **Body**:
  ```json
  {
    "message": "Can I travel to Pune tomorrow?",
    "language": "en",
    "location": {"lat": 18.5204, "lon": 73.8567},
    "history": []
  }
  ```
- **Response**: Structured JSON containing LLM explanation, tool calls, active risk level, sector advisories, and Generative UI metadata.

### `GET /api/v1/risk/assess`
- **Params**: `lat` (float), `lon` (float)
- **Response**: Detailed Multi-factor Risk Engine output (Flood, Heatwave, Wind, Storm score + Emergency Mode flag).

### `GET /api/v1/alerts/live`
- **Params**: `lat` (float), `lon` (float)
- **Response**: Active official weather warnings, severity level, affected zones, and emergency guidance.

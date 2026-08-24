# Data Sources Strategy — WeatherGPT (SIH26068)

## 1. Primary Live Weather Data
- **Provider**: Open-Meteo REST API (`https://api.open-meteo.com/v1/forecast`)
- **Key Parameters**:
  - `temperature_2m`, `relative_humidity_2m`, `apparent_temperature`
  - `precipitation`, `rain`, `showers`, `snowfall`, `precipitation_probability`
  - `surface_pressure`, `cloud_cover`, `wind_speed_10m`, `wind_direction_10m`
  - `soil_temperature_0_to_7cm`, `soil_moisture_0_to_7cm`
  - `uv_index`

## 2. Official Hazard & Alert Feeds
- **Provider**: India Meteorological Department (IMD) RSS Bulletins / Alert Feed & Open-Meteo Weather Alerts API.
- **Alert Levels**: Green (No Warning), Yellow (Watch), Orange (Be Prepared), Red (Take Action).

## 3. Historical Climate Data
- **Provider**: Open-Meteo Historical Weather API (`https://archive-api.open-meteo.com/v1/archive`)
- **Coverage**: ERA5 Reanalysis Dataset from 1940 to present.
- **Use Case**: Comparing current weather against 30-year climate norms (1991–2020 baseline).

## 4. Domain Knowledge (RAG) Data
- **Content Sources**:
  1. ICAR / IMD Agromet Advisory Service Bulletins.
  2. NDMA (National Disaster Management Authority) Flood & Cyclone Safety Guidelines.
  3. IMD Meteorological Glossary & Alert Specifications.
- **Format**: JSON chunks embedded via `all-MiniLM-L6-v2` into ChromaDB.

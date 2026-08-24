# SIH26068 — WeatherGPT Functional & Non-Functional Requirements

## 1. Problem Statement Overview
**Problem ID**: SIH26068
**Title**: WeatherGPT: Conversational AI for Weather Forecasting, Alerts, and Climate Information
**Target Audience**: Indian citizens, farmers, travelers, urban dwellers, emergency response teams.

---

## 2. Core Functional Requirements (FRs)

### FR1: Conversational Weather Intelligence
- Natural language query understanding in English, Hindi, and Marathi.
- Dynamic card generation (Hourly forecast, Daily forecast, Risk gauge, Agromet advisories).
- Intent classification for weather status, travel safety, pesticide application, cyclone warnings, historical comparisons.

### FR2: Real-time & Multi-Source Weather Engine
- Primary API integration with Open-Meteo for live metrics (Temperature, Precipitation, Humidity, Wind Speed, UV Index, Air Quality).
- Fallback integration with IMD RSS/Alert feeds for official Indian weather bulletins.
- Zero-hallucination guardrails ensuring numerical metrics are strictly sourced from API data.

### FR3: Deterministic & Explainable Risk Matrix
- Multi-factor risk calculation for Floods, Heatwaves, Strong Winds, and Severe Thunderstorms.
- Categorization into LOW (0-25), MODERATE (26-50), HIGH (51-75), and EXTREME (76-100).
- Transparent factor breakdown showing exact triggers (e.g. 24h rain > 50mm, soil moisture > 0.8).

### FR4: Dynamic Emergency Disaster Mode
- Dynamic UI state transformation when Risk Level >= 76 or active IMD Red Alert is present.
- High-visibility red alert layout with NDMA safety instructions, expected timing, affected districts, and emergency helpline numbers.

### FR5: Interactive GIS Weather Mapping
- Interactive Leaflet map with layer controls (Temperature, Precipitation, Wind, Radar).
- Reverse geocoding on map click to retrieve location coordinates, local weather, and trigger WeatherGPT query.

### FR6: Multilingual Voice Interface
- Speech-to-Text (STT) and Text-to-Speech (TTS) integration using Web Speech API.
- Support for `en-IN`, `hi-IN` (Hindi), and `mr-IN` (Marathi).

### FR7: Domain Knowledge RAG System
- ChromaDB vector store containing Indian Agromet Advisory bulletins, NDMA disaster protocols, and meteorological terminology.
- Explicit distinction between live weather API responses and vector knowledge search.

### FR8: Sector-Specific Advisories
- Tailored actionable guidance for:
  - Agriculture: Pesticide spraying, irrigation, harvest timing.
  - Travel & Commute: Highway safety, visibility, flooding risks.
  - Urban: Waterlogging, power outage warnings.
  - Marine: Coastal wind speeds, high wave advisories for fishermen.

---

## 3. Non-Functional Requirements (NFRs)

- **Performance**: API response latency < 1.5 seconds for weather queries; < 3 seconds for LLM + RAG responses.
- **Reliability**: Graceful fallbacks for API downtime and speech recognition unavailability.
- **Usability**: Responsive dark-mode dashboard optimized for mobile and desktop screens.
- **Trust & Transparency**: All weather responses include explicit data source, timestamp, and verification badge.

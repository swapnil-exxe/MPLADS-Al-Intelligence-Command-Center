# WeatherGPT — AI Weather Intelligence & Decision Support Platform (SIH26068)

> **SIH Problem Statement SIH26068**: WeatherGPT — Conversational AI for Weather Forecasting, Alerts, and Climate Information.

---

## 🌟 Features Overview

- 🤖 **Zero-Hallucination Conversational AI**: Combines live weather JSON metrics with Gemini LLM reasoning and RAG context without numerical hallucination.
- 🌍 **Multi-Source Live Weather Engine**: Integrated with Open-Meteo REST API and official IMD RSS alert feeds for current, 7-day hourly, 16-day daily, and ERA5 historical climate trends.
- 🛡️ **Deterministic & Explainable Risk Matrix**: Computes multi-factor risk scores ($0 - 100$) for Floods, Heatwaves, Strong Winds, and Storms with transparent factor trigger breakdowns.
- 🚨 **Dynamic Emergency Disaster Command Mode**: UI morphs into a high-visibility Red Emergency Theme when extreme weather or official IMD Red Alerts are triggered, displaying NDMA safety instructions, evacuation guidance, and emergency helpline numbers.
- 🎙️ **Multilingual Voice AI**: Client-side Speech-to-Text (STT) and Text-to-Speech (TTS) integration in English, Hindi (हिन्दी), and Marathi (मराठी).
- 🗺️ **Interactive GIS Map Canvas**: Leaflet.js interactive map with layer toggling (Temperature, Precipitation, Wind) and click-on-map coordinate reverse geocoding.
- 🌾 **Sector Decision Support**: Custom advisories for Agriculture, Travel & Commute, Urban Infrastructure, and Marine sectors.

---

## 🏗️ Technical Architecture

```
                    USER (Voice / Text / Map Click)
                                  │
                                  ▼
                     Next.js 14 Web Frontend
            (Tailwind CSS + Leaflet GIS + Web Speech AI)
                                  │
                                  ▼
                   FastAPI AI Orchestrator Backend
           ┌──────────────────────┴──────────────────────┐
           ▼                                             ▼
  Live Weather Engine                           RAG Knowledge Engine
(Open-Meteo + IMD Feed)                       (ChromaDB / Agromet Guides)
           │                                             │
           └──────────────────────┬──────────────────────┘
                                  ▼
                    Deterministic Risk Engine
                     (Flood, Heatwave, Wind)
                                  │
                                  ▼
                      Zero-Hallucination LLM
                  (Gemini / OpenAI Localized)
```

---

## 🚀 Getting Started

### Prerequisites
- Node.js (v18+) & npm
- Python (v3.9+)

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```
*API will run on `http://localhost:8001` with Swagger docs at `http://localhost:8001/docs`.*

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
*App will run live on `http://localhost:3000`.*

---

## 📊 Verification & Tests
Run backend test suite:
```bash
python -c "import sys; sys.path.insert(0, 'backend'); from tests.test_weather_api import *; test_current_weather(); test_forecast_7_days(); print('Backend Verified!')"
```

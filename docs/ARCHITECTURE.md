# Technical Architecture — WeatherGPT (SIH26068)

```
                            ┌─────────────────────────────────────────┐
                            │               USER                      │
                            │   (Voice / Text Input / Map Click)      │
                            └────────────────────┬────────────────────┘
                                                 │
                                                 ▼
                            ┌─────────────────────────────────────────┐
                            │    Next.js 14 Frontend Interface        │
                            │   - Web Speech STT/TTS (En/Hi/Mr)       │
                            │   - Leaflet.js Interactive GIS Map      │
                            │   - Generative UI Card Renderer         │
                            └────────────────────┬────────────────────┘
                                                 │ REST / SSE API
                                                 ▼
                            ┌─────────────────────────────────────────┐
                            │     FastAPI AI Orchestrator Backend     │
                            │   - Intent Classification / Router      │
                            │   - Language Translator / Localizer     │
                            └───────┬─────────────────────────┬───────┘
                                    │                         │
            ┌───────────────────────┴──────┐           ┌──────┴───────────────────────┐
            ▼                              ▼           ▼                              ▼
┌───────────────────────┐      ┌────────────────────┐┌────────────────────┐      ┌───────────────────────┐
│ Live Weather Engine   │      │ Historical Engine  ││ RAG Knowledge Engine│      │ Deterministic Risk    │
│ - Open-Meteo API      │      │ - Open-Meteo ERA5  ││ - Chroma Vector DB │      │ Matrix Engine         │
│ - IMD RSS Alerts Feed │      │   Reanalysis Data  ││ - Agromet Bulletins│      │ - Flood Score         │
│ - Geocoding Service   │      │   (1940-Present)   ││ - Disaster Safety  │      │ - Heatwave Index      │
└───────────┬───────────┘      └─────────┬──────────┘└─────────┬──────────┘      │ - Cyclone / Storm     │
            │                            │                     │                 └───────────┬───────────┘
            └────────────────────────────┼─────────────────────┴─────────────────────────────┘
                                         │
                                         ▼
                            ┌─────────────────────────────────────────┐
                            │      LLM Explanation & Structurer       │
                            │  - Synthesizes Data + RAG Context       │
                            │  - Returns Structured JSON + UI Props   │
                            │  - Zero Hallucination Enforcement       │
                            └────────────────────┬────────────────────┘
                                                 │
                                                 ▼
                            ┌─────────────────────────────────────────┐
                            │     Generative Response Generator       │
                            │  - Dynamic Weather UI Widgets           │
                            │  - Emergency Command Banner (If Extreme)│
                            │  - Synthesized Localized Audio Speech   │
                            └─────────────────────────────────────────┘
```

## Modular System Breakdown

1. **Frontend Tier (Next.js 14 + Tailwind CSS + Leaflet.js)**:
   - Client-side Web Speech recognition for `en-IN`, `hi-IN`, `mr-IN`.
   - Interactive GIS Leaflet map with custom weather tiles and click-to-query event binding.
   - Generative UI components for Hourly Chart, Daily Cards, Risk Meter, Sector Cards, and Emergency Mode.

2. **Backend Services (FastAPI + Async Python)**:
   - `open_meteo.py`: Service for current weather, 7-day hourly forecast, 16-day daily forecast, and historical ERA5 climate trends.
   - `imd_feed.py`: Official alert parsing and RSS warning monitor.
   - `risk_engine.py`: Multi-factor deterministic risk calculator.
   - `rag_engine.py`: ChromaDB semantic search interface.
   - `llm_service.py`: Gemini / OpenAI function calling engine and zero-hallucination prompt orchestrator.

3. **Data & Storage Tier**:
   - SQLite / PostgreSQL for saved locations and audit logs.
   - ChromaDB vector store for agricultural guides, NDMA protocols, and terminology.

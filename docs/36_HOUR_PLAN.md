# 36-Hour Hackathon Implementation Roadmap

## Milestone Schedule

| Phase | Timeframe | Target Deliverables | Verification Strategy |
| :--- | :--- | :--- | :--- |
| **Phase 1** | Hours 0–6 | Project setup, FastAPI backend core, Open-Meteo REST API wrapper | `pytest backend/tests/test_weather_api.py` |
| **Phase 2** | Hours 6–14 | Next.js 14 frontend layout, Leaflet GIS map with layers, Click-geocoding | Interactive browser test of map & geocoding |
| **Phase 3** | Hours 14–22| FastAPI Chat API, Gemini LLM function router, ChromaDB RAG store | API testing with sample queries |
| **Phase 4** | Hours 22–28| Deterministic Risk Engine, Dynamic Emergency Command UI Mode | Trigger extreme flood alert & verify Red UI shift |
| **Phase 5** | Hours 28–32| Web Speech API STT/TTS in English, Hindi (`hi-IN`), Marathi (`mr-IN`) | Voice input/output test across 3 languages |
| **Phase 6** | Hours 32–36| UI polish, final E2E scenario testing, demo rehearsal | Run through all 5 demo scenarios cleanly |

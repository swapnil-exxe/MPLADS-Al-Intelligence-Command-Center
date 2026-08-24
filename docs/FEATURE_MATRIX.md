# Feature Matrix — WeatherGPT (SIH26068)

| Feature | Reference A | Reference B | Reference C | SIH26068 Req | Our WeatherGPT | Priority | Build in 36h? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Generative Weather AI Chat** | Tabular ML | RAG text | Gen UI Cards | Essential | Conversational Gen UI Chat | 🔴 MUST HAVE | ✅ YES |
| **Live Multi-Source Weather Engine** | Static CSV | OWM API | OWM API | Essential | Open-Meteo + IMD Feed | 🔴 MUST HAVE | ✅ YES |
| **Location Geocoding & GPS** | Manual Input | Text Query | Hardcoded | Essential | Geolocation + City Search + Click | 🔴 MUST HAVE | ✅ YES |
| **Interactive GIS Weather Map** | None | None | Basic viewer | Essential | Leaflet map with layers & click-query | 🔴 MUST HAVE | ✅ YES |
| **Deterministic Risk Engine** | Tabular ML | None | None | Essential | Multi-factor explainable matrix | 🔴 MUST HAVE | ✅ YES |
| **Dynamic Emergency Command Mode** | None | None | None | Essential | Dynamic Red UI state transition | 🔴 MUST HAVE | ✅ YES |
| **Multilingual Voice AI (En/Hi/Mr)**| None | None | None | Essential | Web Speech STT/TTS in 3 languages | 🔴 MUST HAVE | ✅ YES |
| **Domain Knowledge RAG System** | Chatbase iframe| FAISS forecast | None | High | ChromaDB for Agromet/NDMA knowledge| 🟢 DIFFERENTIATOR| ✅ YES |
| **Sector Decision Support** | None | Generic text | Generic text | High | Agriculture, Travel, Urban, Marine | 🟢 DIFFERENTIATOR| ✅ YES |
| **Climate & Historical Comparison** | Static CSV | None | None | Medium | Open-Meteo ERA5 Reanalysis API | 🟢 DIFFERENTIATOR| ✅ YES |
| **Source Citation & Trust Layer** | None | None | None | High | Verification badge & timestamp | 🟢 DIFFERENTIATOR| ✅ YES |
| **YOLO Disaster Victim Detection** | Deployed | None | None | Outside scope | Excluded | ⚫ DROP | ❌ NO |
| **RAG over Live Weather Text** | None | Deployed | None | Anti-pattern | Excluded (Use Live API instead) | ⚫ DROP | ❌ NO |

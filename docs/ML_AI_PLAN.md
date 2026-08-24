# AI / ML Strategy Plan — WeatherGPT (SIH26068)

## 1. Intent Router & Function Calling
- System uses LLM function/tool calling to map unstructured queries to backend tools:
  - `get_live_weather(lat, lon)`
  - `get_forecast(lat, lon)`
  - `assess_weather_risk(lat, lon)`
  - `search_knowledge_base(query)`
  - `compare_climate_history(lat, lon)`

## 2. Zero-Hallucination Guardrails
- **Strict Rule**: Numeric weather parameters (temperature, rain mm, wind speed) must NEVER be synthesized by the LLM.
- **Context Injection**: Live API JSON is formatted into markdown context blocks. The system prompt enforces strict grounding:
  > *"You are WeatherGPT. Answer strictly based on the provided live weather data JSON. Do not fabricate numerical values. If data is unavailable, state it clearly."*

## 3. RAG Knowledge System
- **Embedding Model**: `all-MiniLM-L6-v2` via SentenceTransformers.
- **Vector DB**: ChromaDB.
- **Top-K Retrieval**: Retrieves top 3 semantic context chunks for domain queries (e.g. agricultural crop safety, flood evacuation procedures).

## 4. Deterministic Multi-Factor Risk Formula
$$R_{\text{flood}} = w_1 \cdot P_{\text{rain\_24h}} + w_2 \cdot I_{\text{precip\_rate}} + w_3 \cdot S_{\text{soil\_moisture}} + w_4 \cdot A_{\text{official\_alert}}$$
- Low: 0-25 | Moderate: 26-50 | High: 51-75 | Extreme: 76-100 (Emergency Mode)

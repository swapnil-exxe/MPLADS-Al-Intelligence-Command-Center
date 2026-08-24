# PROJECT AUDIT — MPLADS AI INTELLIGENCE COMMAND CENTER
**SIH Problem Statement ID**: SIH26102  
**Title**: Development of an AI-powered system to detect anomalies, fraud, and inefficiencies in MPLAD Scheme implementation  
**Organization**: Ministry of Statistics and Programme Implementation (MoSPI) — Data Informatics & Innovation Division (DIID)  
**Date**: August 25, 2026  

---

## 1. Audit Executive Summary

A comprehensive technical and architectural audit of the current repository was performed prior to initiating code development. The audit evaluated existing codebase assets, frontend dependencies, backend APIs, ML infrastructure, database schemas, documentation, design frameworks, and external reference standards.

### Key Finding
The repository previously contained a starter prototype designed for a different domain (*WeatherGPT — SIH26068*). All legacy components, endpoints, and data pipelines must be cleanly migrated and transformed into the **MPLADS AI Intelligence Command Center**.

---

## 2. Codebase Inventory & Asset Assessment

| Area | Existing State | Target MPLADS State | Action Required |
| :--- | :--- | :--- | :--- |
| **Frontend Framework** | Next.js 14.2.5 (App Router), React 18, Tailwind CSS, Leaflet | Next.js 14 + Tailwind CSS + Lucide Icons + MapLibre/Leaflet + Framer Motion | Retain Next.js 14 structure; refactor all UI components for MPLADS Command Center |
| **Frontend UI Components** | Weather cards, emergency overlay, weather map, generic chat | Command Center layout, AI Watch, Risk Map, Fraud Relationship Graph, Anomaly Tables, Project Investigation Workspace | Replace legacy weather components with enterprise financial/risk components |
| **Backend Framework** | FastAPI (v0.100+), Uvicorn, Requests | FastAPI + Pydantic v2 + Structured Service Layer | Retain FastAPI architecture; rewrite endpoints for MPLADS analytics & risk engine |
| **Backend Services** | `open_meteo.py`, `imd_feed.py`, `rag_engine.py`, `risk_engine.py` (Weather) | `mplads_data_service.py`, `anomaly_detector.py`, `risk_engine.py`, `ai_investigator.py` | Overhaul core logic to ingest MPLADS allocation CSV and execute financial ML models |
| **ML & AI Infrastructure** | ChromaDB, basic sentence transformers, LLM wrapper for weather | Scikit-Learn (Isolation Forest, LOF, Statistical Z-Score), Grounded RAG + LLM Tool Calling | Implement scikit-learn anomaly pipeline and grounded AI Investigator |
| **Database Layer** | In-memory / Mock JSON feeds | In-Memory SQLite/PostgreSQL ORM + Pandas Service Layer + Dynamic Ingestion | Build normalized schema & database service layer for MP allocations and synthetic projects |
| **Documentation** | Legacy WeatherGPT docs (`36_HOUR_PLAN.md`, `ARCHITECTURE.md`, etc.) | Comprehensive MPLADS docs (`PROJECT_AUDIT.md`, `DATASET_AUDIT.md`, `IMPLEMENTATION_PLAN.md`, `RISK_ENGINE.md`, etc.) | Replace legacy documentation with official MPLADS system specifications |

---

## 3. Environment & Package Audit

### Frontend (`frontend/package.json`)
- **Next.js**: `14.2.5`
- **React / React-DOM**: `^18.3.1`
- **Styling**: `tailwindcss ^3.4.7`, `postcss ^8.4.40`, `clsx`, `tailwind-merge`
- **Icons**: `lucide-react ^0.424.0`
- **GIS Mapping**: `leaflet ^1.9.4`, `react-leaflet ^4.2.1`
- **Required Additions**: `framer-motion` for Emil Kowalski motion design principles, `recharts` for financial charts.

### Backend (`backend/requirements.txt`)
- **FastAPI**: `>=0.100.0`
- **Pydantic**: `>=2.0.0`
- **Data Engineering**: `pandas>=2.0.0`, `numpy>=1.24.0`
- **Machine Learning**: `scikit-learn>=1.3.0`
- **Vector Search / RAG**: `chromadb>=0.4.0`, `sentence-transformers>=2.2.2`
- **Testing**: `pytest>=7.4.0`, `httpx>=0.24.1`
- **Required Additions**: `scipy` for statistical distributions, `networkx` for graph relationships.

---

## 4. Official MPLADS System Context Inspection

The official MoSPI MPLADS portal ([mplads.mospi.gov.in](https://mplads.mospi.gov.in/digigov/dashboard.html)) tracks funds allocated to Lok Sabha and Rajya Sabha Members of Parliament for constituency development work.

### Structural Insights from MoSPI Guidelines:
1. **Entitlement**: Each MP is entitled to recommend works up to ₹5 Crore per annum (or ₹2.5 Cr per installment), allocated across financial years.
2. **Implementation Flow**: MP recommends work $\rightarrow$ Nodal District Authority examines feasibility $\rightarrow$ Sanctioned $\rightarrow$ Implementing Agency assigned $\rightarrow$ Funds released $\rightarrow$ Execution $\rightarrow$ Completion Certificate & Audit.
3. **System Requirements**: The command center must monitor allocation distribution, detect non-standard allocation values, flag delayed project execution, track peer-group financial variance, and provide actionable evidence for decision-makers.

---

## 5. Emil Kowalski Skills & UI Design Reference Audit

Per the product specification, the visual & interaction model adheres to Emil Kowalski design engineering principles:
- **`emil-design-eng`**: Information density with spatial clarity; crisp borders, dark/light contrast hierarchy, professional typography.
- **`animate` & `animation-vocabulary`**: Motion serves to orient the user ("Where did this come from?", "What changed?").
- **`pick-ui-library` & `prototype`**: Fast, micro-interactive components without UI bloat.
- **Visual Aesthetic**: Inspired by Linear, Vercel, Apple, and Palantir-style financial intelligence interfaces. No purple AI overload, no fake 3D, no generic admin themes.

---

## 6. Audit Verdict & Transformation Roadmap

1. **Clean Slate Refactoring**: Purge WeatherGPT files from `backend/app/api`, `backend/app/core`, `frontend/components`, and `docs/`.
2. **Data Pipeline First**: Establish the `Allocated_Limit_for_Honble_MPs.csv` ingestion engine as the single source of truth for MP allocations.
3. **ML Risk & Anomaly Engine**: Build scikit-learn anomaly detection (Isolation Forest + LOF + Z-Score) on top of verified dataset metrics.
4. **Command Center UI**: Construct the Next.js 14 dashboard with AI Watch, Interactive India Map, Risk Distribution filter, Fraud Intelligence, Anomaly Matrix, and Grounded AI Investigator.

# IMPLEMENTATION PLAN — MPLADS AI INTELLIGENCE COMMAND CENTER
**SIH Problem Statement**: SIH26102 — Development of an AI-powered system to detect anomalies, fraud, and inefficiencies in MPLAD Scheme implementation regd.  
**Target Organization**: Ministry of Statistics and Programme Implementation (MoSPI) — Data Informatics & Innovation Division (DIID)  
**Date**: August 25, 2026  

---

## 1. Core Principles & Strict Data Rules

1. **REAL DATA FIRST**: Real MP allocations from `Allocated Limit for Honble MPs.csv` are the single source of truth for all official KPIs, state statistics, MP analytics, and allocation anomaly scores.
2. **STRICT SEPARATION**: Synthetic/demo project records are NEVER mixed with official statistics or MP allocation totals.
3. **EXPLICIT DATA LIMITATIONS**: Unsupplied features (expenditure, contractors, physical progress) are explicitly flagged in the UI as `"Requires additional project-level dataset"` or `"Demo Simulation"`.
4. **REAL-FEATURE ML & EXPLAINABLE RISK**: ML models and risk engines run strictly on features present in the dataset (allocation amount, state baseline ratio, statistical Z-score, missing data flags).

---

## 2. Revised 10-Phase Implementation Sequence

| Phase | Phase Title | Key Deliverables & Scope |
| :--- | :--- | :--- |
| **Phase 1** | Real CSV Ingestion & Validation | Robust CSV parser in `backend/app/services/real_data_service.py` to ingest 543 MP records, handle Row 108 null amount, validate 36 States/UTs, and verify ₹83,06,21,04,294.53 total sum. |
| **Phase 2** | Real Allocation Analytics | Analytics engine calculating State totals, National mean/median, IQR bounds, state rank, reservation categories, and allocation distribution histograms. |
| **Phase 3** | Data Service & FastAPI Endpoints | Production REST API endpoints (`/api/analytics/overview`, `/api/analytics/states`, `/api/mps`, `/api/mps/{id}`, `/api/system/data-sources`). |
| **Phase 4** | Design System & UI Architecture | Emil Kowalski design engineering principles (`emil-design-eng`, `animate`), dark/light mode toggle, typography, semantic risk colors (Green, Amber, Red, Dark Red). |
| **Phase 5** | Command Center Main UI | Next.js 14 frontend screens: Overview, State Analytics, Fund Analytics, Interactive India Map, MP Directory, System Data Sources ledger. |
| **Phase 6** | Real Allocation Risk & Anomaly Engine | Machine learning pipeline using **Isolation Forest**, **LOF**, and **Statistical Z-Score** strictly on allocation features. Outputs explainable "Allocation Risk Signals". |
| **Phase 7** | Isolated Demo Simulation Layer | Separate `DemoDataService` for project-level investigation, fraud graph, and contractor risk views. Every UI element carrying this data is clearly tagged `"DEMO SIMULATION — NOT DERIVED FROM OFFICIAL MPLADS DATA"`. |
| **Phase 8** | Grounded AI Investigator | Conversational assistant powered by backend tool-calling into verified analytics. Returns clear notice if requested info is outside dataset scope. |
| **Phase 9** | Testing & Verification Suite | Automated test suite in `tests/test_mplads_pipeline.py` verifying real dataset parsing, API schemas, ML model bounds, and zero data leakage. |
| **Phase 10** | Final Demo Flow & Polish | End-to-end judge presentation flow, animation tuning, accessibility audit, responsive checks, and documentation completion. |

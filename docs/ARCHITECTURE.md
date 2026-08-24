# MPLADS AI INTELLIGENCE COMMAND CENTER — SYSTEM ARCHITECTURE
**Problem Statement ID**: SIH26102  
**Organization**: Ministry of Statistics and Programme Implementation (MoSPI)  

---

## 1. System Architecture Overview

```
                      USER / SIH JUDGE
                            │
                            ▼
              Next.js 14 Web Command Center
     (Tailwind CSS + Emil Kowalski Motion + Lucide Icons)
                            │
                            ▼
               FastAPI AI Orchestrator (v2.0)
     ┌──────────────────────┼──────────────────────┐
     ▼                      ▼                      ▼
RealDataService       AnomalyDetector       AIInvestigator
 (Pandas/CSV)      (IsoForest/LOF/ZScore)   (Grounded RAG)
     │                      │                      │
     └──────────────────────┼──────────────────────┘
                            ▼
               Isolated Demo Simulation Layer
            (Explicit Disclosure Badges Enforced)
```

---

## 2. Component Design & Responsibilities

1. **Real Data Pipeline (`real_data_service.py`)**:
   - Ingests `Allocated_Limit_for_Honble_MPs.csv` containing 543 MP records and ₹83,06,21,04,294.53 total allocation.
   - Cleans numeric amounts, handles Row 108 null values, deduplicates Nanded constituency entries, and aggregates 36 State/UT summary metrics.
2. **Machine Learning Anomaly Engine (`anomaly_detector.py`)**:
   - Scikit-learn **Isolation Forest** (contamination=0.08)
   - **Local Outlier Factor (LOF)** (n_neighbors=20)
   - **Statistical Z-Score Analysis** (|Z| > 2.0)
   - Operates strictly on verified features (`allocated_amount`, `dev_baseline`, `dev_state_mean`, `z_score_nat`).
3. **Grounded AI Investigator (`ai_investigator.py`)**:
   - Executes backend tool queries against real MoSPI dataset metrics.
   - Returns explicit boundary notices if query requests out-of-scope dataset features (contractors, live GPS, payment transactions).
4. **Isolated Demo Layer (`demo_data_service.py`)**:
   - Holds 100 simulated micro-project records and fraud relationship graph.
   - Every returned record contains mandatory label: `"DEMO SIMULATION — NOT DERIVED FROM OFFICIAL MPLADS DATA"`.

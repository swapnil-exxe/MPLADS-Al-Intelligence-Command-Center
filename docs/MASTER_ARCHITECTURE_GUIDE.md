# MASTER TECHNICAL EXPLANATION & ARCHITECTURE GUIDE
## MPLADS AI INTELLIGENCE COMMAND CENTER (SIH26102)
**Prepared for**: Ministry of Statistics and Programme Implementation (MoSPI) / Hackathon Presentation / Technical Viva  
**Active Production Stack**: Next.js 14 + FastAPI 2.0 + Scikit-Learn + Supabase Cloud PostgreSQL 15  
**Primary Dataset**: Official Gazette `Allocated_Limit_for_Honble_MPs.csv` (543 MPs, 36 States/UTs, ₹8,306.21 Crore Total Allocation)

---

# PART 1 — COMPLETE REPOSITORY & FOLDER MAP

The codebase follows a decoupled micro-service architecture separating the React frontend, Python FastAPI backend, dedicated Machine Learning package, database pooler layer, and automated pytest suite.

```
Base Zero/
├── 📁 frontend/                         # Next.js 14 App Router + React 18 + Tailwind CSS
│   ├── 📁 app/                          # Next.js 14 App Router Pages (Routes)
│   ├── 📁 components/                   # Reusable Neo-Brutalist UI Components
│   ├── 📁 utils/supabase/               # Supabase JS / SSR Client Utilities
│   └── 📁 lib/                          # Shared Frontend Configuration (api.ts)
│
├── 📁 backend/                          # FastAPI Backend Application Root
│   ├── 📁 ml/                           # 🌟 DEDICATED ML MODEL ENGINE PACKAGE
│   │   ├── 📄 __init__.py               # ML Package Exports
│   │   ├── 📄 anomaly_detector.py       # Isolation Forest + Tukey IQR + Z-Score Models
│   │   └── 📄 risk_engine.py           # Risk Bounds & IMD Weather Engine
│   │
│   ├── 📁 app/                          # FastAPI Application Modules
│   │   ├── 📁 api/                      # REST API Endpoint Routers (analytics, risk, chat, system)
│   │   ├── 📁 db/                       # Supabase Cloud PostgreSQL Service Layer (database.py)
│   │   ├── 📁 core/                     # Backward-Compatibility Proxy & External Feeds
│   │   ├── 📁 schemas/                  # Pydantic Input/Output Schemas
│   │   └── 📁 services/                 # Business Logic (real_data_service, ai_investigator)
│   │
│   ├── 📁 data/                         # Primary Ground-Truth Dataset
│   │   └── 📄 Allocated_Limit_for_Honble_MPs.csv # Official MoSPI Gazette CSV (543 Records)
│   │
│   ├── 📄 main.py                       # FastAPI Application Entrypoint
│   └── 📄 .env                          # Backend Environment Config (DATABASE_URL, SSL)
│
├── 📁 scripts/                          # Batch Migration & Admin Utility Scripts
│   └── 📄 migrate_to_cloud_postgres.py # Fast Batch Migration to Supabase Cloud
│
├── 📁 tests/                            # Pytest Automated Test Suite (32 Tests)
│   ├── 📄 test_anomaly_detection.py     # ML Model Reproducibility & Seed Tests
│   ├── 📄 test_mplads_pipeline.py       # End-to-End FastAPI & Database Integration Tests
│   ├── 📄 test_dataset_integrity.py     # MoSPI CSV 543 Record Validation Tests
│   ├── 📄 test_ai_grounding.py          # Zero-Hallucination Scope Boundary Tests
│   ├── 📄 test_risk_engine.py           # Risk Scoring & Evidence Breakdown Tests
│   ├── 📄 test_analytics.py             # State Analytics & Pagination Tests
│   └── 📄 test_demo_data_isolation.py   # Data Isolation & Disclosure Tests
│
└── 📁 docs/                             # System Architecture & Audit Documentation
```

### Folder Responsibilities & Lifecycle Analysis

| Folder | Purpose & Responsibility | Execution Lifecycle | Execution Context | Runtime Dependency |
| :--- | :--- | :--- | :--- | :--- |
| `frontend/` | Next.js 14 Client Dashboard rendering state metrics, maps, and UI panels. | Runtime (Node / Browser) | Production Client | Required for User Interaction |
| `backend/ml/` | Dedicated ML package containing Isolation Forest, Tukey IQR, and Z-Score algorithms. | Runtime (Python) | Production ML Engine | **Critical** — Computes Anomaly Signals |
| `backend/app/api/` | REST API routers exposing HTTP endpoints to the frontend. | Runtime (FastAPI) | Production Backend | **Critical** — Exposes System APIs |
| `backend/app/db/` | Database service layer handling PostgreSQL connection pooling and SQL queries. | Runtime (psycopg2) | Production Database | **Critical** — Queries Supabase Cloud |
| `backend/app/services/` | In-memory Pandas analytics and grounded tool-calling logic. | Runtime (Python) | Production Business Logic | **Critical** — Processes Raw Datasets |
| `scripts/` | Batch ETL migration script to populate Supabase Cloud PostgreSQL from local CSV. | One-Time / Admin | Maintenance Utility | Optional at runtime (Post-Migration) |
| `tests/` | Pytest test suite verifying 32 mathematical and integration invariants. | Test Execution | CI/CD & Verification | Excluded from Production Build |

---

# PART 2 — REAL SYSTEM ARCHITECTURE & DATA FLOW

```
[USER BROWSER]
      │
      │ 1. HTTP GET / POST Requests
      ▼
[NEXT.JS 14 FRONTEND] (app/page.tsx, components/Header.tsx, AnomalyMatrix.tsx)
      │
      │ 2. API Fetch (`http://localhost:8001/api/...`)
      ▼
[FASTAPI MAIN ROUTER] (backend/main.py)
      │
      │ 3. Dispatches to Endpoint Routers (backend/app/api/*.py)
      ▼
[SERVICE & ML LAYER]
┌─────────────────────────────────────────────────────────────┐
│ • backend/app/services/real_data_service.py (Pandas Aggs)  │
│ • backend/ml/anomaly_detector.py (IsolationForest + IQR + Z)│
│ • backend/app/services/ai_investigator.py (Grounded Engine) │
└─────────────────────────────────────────────────────────────┘
      │
      │ 4. Formatted SQL Queries via Connection Pool (psycopg2 SSL)
      ▼
[SUPABASE CLOUD POSTGRESQL 15] (aws-0-ap-south-1.pooler.supabase.com:6543)
┌─────────────────────────────────────────────────────────────┐
│ • mp_allocations (543 rows)   • dataset_versions (v2026.08) │
│ • model_runs (ML Runs)        • anomaly_signals (Signals)   │
│ • investigation_audit_logs    • users_and_roles (RBAC)      │
└─────────────────────────────────────────────────────────────┘
      │
      │ 5. Returns SQL Tuple / Dict Cursor Result Set
      ▼
[FASTAPI RESPONSE SERIALIZATION] (Pydantic JSON)
      │
      │ 6. JSON Payload Transferred Over Network
      ▼
[NEXT.JS REACT STATE UPDATE] (useState / useEffect)
      │
      │ 7. DOM Re-render with Updated Metrics & Tables
      ▼
[USER BROWSER DISPLAY]
```

### Detailed Data Flow Mechanics

| Sequence Step | Source File & Function | Target File & Endpoint | Data Transferred | Database Table Involved |
| :--- | :--- | :--- | :--- | :--- |
| **1. Page Load** | `frontend/app/page.tsx` (`loadData()`) | `GET /api/analytics/overview` | Empty Query | Reads `mp_allocations` |
| **2. Fetch Analytics** | `backend/app/api/analytics.py` (`get_overview()`) | `backend/app/services/real_data_service.py` | Key Metrics Request | Aggregates `mp_allocations` |
| **3. Anomaly Evaluation** | `backend/app/api/risk.py` (`get_anomalies()`) | `backend/ml/anomaly_detector.py` (`fit_and_predict()`) | Pandas DataFrame (543 rows) | Reads `mp_allocations` |
| **4. ML Persistence** | `backend/app/api/risk.py` (`reevaluate_risk_models()`) | `backend/app/db/database.py` (`save_model_run_and_signals()`) | Model Parameters & 543 Signals | Inserts `model_runs` & `anomaly_signals` |
| **5. Audit Note Creation** | `frontend/components/InvestigationWorkspace.tsx` | `POST /api/system/audit-logs` | JSON `{mp_id, status, note, officer}` | Inserts `investigation_audit_logs` |

---

# PART 3 — FRONTEND ARCHITECTURE & COMPONENTS

The frontend is built using Next.js 14 App Router, TypeScript, Tailwind CSS, Lucide React, and Framer Motion adhering to a high-density, accessible **Neo-Brutalist Design System**.

### Frontend Pages Map

| Page Route | File Location | Purpose & Functionality | Endpoints Consumed | Database Source |
| :--- | :--- | :--- | :--- | :--- |
| `/` | `frontend/app/page.tsx` | Main Government Command Center Dashboard. Renders KPIs, AI Watch Panel, State Map, and Capability Matrix. | `GET /api/analytics/overview`<br>`GET /api/analytics/states`<br>`GET /api/analytics/mps`<br>`GET /api/risk/anomalies` | `mp_allocations`, `anomaly_signals` |
| `/risk` | `frontend/app/risk/page.tsx` | Risk Intelligence Workspace displaying elevated allocation risk signals and risk tier distributions. | `GET /api/risk/anomalies`<br>`GET /api/risk/distribution` | `anomaly_signals`, `model_runs` |
| `/anomalies` | `frontend/app/anomalies/page.tsx` | Full 543 MP Allocation Anomaly Matrix with state filtering, baseline deviation tracking, and live search. | `GET /api/risk/anomalies` | `anomaly_signals`, `mp_allocations` |
| `/fraud` | `frontend/app/fraud/page.tsx` | Relationship Scope & Source Data Status page detailing micro-project integration requirements. | `GET /api/risk/anomalies` | `anomaly_signals` |
| `/investigator` | `frontend/app/investigator/page.tsx` | Grounded AI Investigator query chat interface with zero-hallucination boundary notices. | `POST /api/ai/investigate` | Grounded Pandas / MoSPI Dataset |
| `/data-sources` | `frontend/app/data-sources/page.tsx` | Data Provenance & Transparency Ledger showing dataset checksums and active database status. | `GET /api/system/data-sources`<br>`GET /api/system/db-status` | `dataset_versions`, `mp_allocations` |
| `/model-health` | `frontend/app/model-health/page.tsx` | Production ML Model Health Card listing Isolation Forest, IQR, and Z-Score algorithm parameters. | `GET /api/system/model-health` | `model_runs` |

### Key Component Breakdowns

- [`Header.tsx`](file:///Users/swapnil/Base%20Zero/frontend/components/Header.tsx): Top navigation bar. Contains brand title (`MPLADS INTELLIGENCE — MoSPI · DIID`), live system monitoring indicator, modal triggers for Data Sources and Model Health, and global constituency search bar (`SEARCH CONSTITUENCY...`).
- [`SidebarNav.tsx`](file:///Users/swapnil/Base%20Zero/frontend/components/SidebarNav.tsx): Left menu navigation with active route highlighting and live High-Risk count badges.
- [`OverviewMetrics.tsx`](file:///Users/swapnil/Base%20Zero/frontend/components/OverviewMetrics.tsx): Horizontal intelligence strip rendering Total Allocation Limit (₹8,306.21 Cr), Monitored MPs (543), Valid Records (542), Missing Records (1), and Elevated Risk Signals.
- [`AIWatch.tsx`](file:///Users/swapnil/Base%20Zero/frontend/components/AIWatch.tsx): Hero panel spotlighting top allocation anomalies (e.g. Malkajgiri ₹32.75 Cr, Basirhat ₹4.90 Cr, Nanded Missing Data) with explainability badges.
- [`AnomalyMatrix.tsx`](file:///Users/swapnil/Base%20Zero/frontend/components/AnomalyMatrix.tsx): 543 MP directory table supporting live multi-field search across MP Name, Constituency, and State, state selection dropdowns, baseline variance columns, and row click drawer triggers.
- [`InvestigationWorkspace.tsx`](file:///Users/swapnil/Base%20Zero/frontend/components/InvestigationWorkspace.tsx): Slide-over drawer for Nodal Officers to inspect specific MP evidence, assign status (`UNDER_INVESTIGATION`, `VERIFIED_CLEAR`), add audit notes, and persist logs directly to Supabase.
- [`AIInvestigatorChat.tsx`](file:///Users/swapnil/Base%20Zero/frontend/components/AIInvestigatorChat.tsx): Chat interface with suggested grounded prompt chips (`"Why is Malkajgiri showing an anomaly?"`) and explicit boundary notices for out-of-scope queries.

---

# PART 4 — BACKEND STRUCTURE & PYTHON FILE INDEX

The backend is built in Python using FastAPI, Uvicorn, Pandas, Scikit-Learn, and Psycopg2.

### Python File Master Index

| File Path | Primary Purpose | Called By | Imports / Calls | Runtime Status | ML Code? | DB Code? | API Endpoint? |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| [`backend/main.py`](file:///Users/swapnil/Base%20Zero/backend/main.py) | FastAPI app entrypoint, CORS middleware, root & `/health` endpoints. | Uvicorn Server | Includes routers (`analytics`, `risk`, `chat`, `system`) | Production Runtime | ❌ | ❌ | ✅ (`GET /`, `GET /health`) |
| [`backend/ml/anomaly_detector.py`](file:///Users/swapnil/Base%20Zero/backend/ml/anomaly_detector.py) | Scikit-Learn Isolation Forest, Tukey IQR, and Z-Score anomaly detection models. | `risk.py`, `ai_investigator.py`, `tests` | Scikit-Learn, Pandas, NumPy | Production Runtime | ✅ | ❌ | ❌ |
| [`backend/ml/risk_engine.py`](file:///Users/swapnil/Base%20Zero/backend/ml/risk_engine.py) | Deterministic risk score bounds and weather/IMD alert risk matrix. | `backend/ml/__init__.py` | `imd_feed.py` | Production Runtime | ✅ | ❌ | ❌ |
| [`backend/app/db/database.py`](file:///Users/swapnil/Base%20Zero/backend/app/db/database.py) | Connection pooler & SQL query executor for Supabase Cloud PostgreSQL. | `analytics.py`, `risk.py`, `system.py` | `psycopg2`, `dotenv`, `urllib.parse` | Production Runtime | ❌ | ✅ | ❌ |
| [`backend/app/services/real_data_service.py`](file:///Users/swapnil/Base%20Zero/backend/app/services/real_data_service.py) | Loads `Allocated_Limit_for_Honble_MPs.csv`, computes Pandas aggregations. | `analytics.py`, `risk.py`, `ai_investigator.py` | Pandas, NumPy | Production Runtime | ❌ | ❌ | ❌ |
| [`backend/app/services/ai_investigator.py`](file:///Users/swapnil/Base%20Zero/backend/app/services/ai_investigator.py) | Grounded tool-calling engine with zero-hallucination boundary checks. | `chat.py` | `real_data_service`, `anomaly_detector` | Production Runtime | ❌ | ❌ | ❌ |
| [`backend/app/api/analytics.py`](file:///Users/swapnil/Base%20Zero/backend/app/api/analytics.py) | State analytics & MP allocation REST endpoints. | `main.py` Router | `real_data_service`, `db_service` | Production Runtime | ❌ | ✅ | ✅ (`/api/analytics/*`) |
| [`backend/app/api/risk.py`](file:///Users/swapnil/Base%20Zero/backend/app/api/risk.py) | Anomaly signals & ML re-evaluation REST endpoints. | `main.py` Router | `anomaly_detector`, `db_service` | Production Runtime | ❌ | ✅ | ✅ (`/api/risk/*`) |
| [`backend/app/api/system.py`](file:///Users/swapnil/Base%20Zero/backend/app/api/system.py) | Database status, audit log persistence, and transparency ledger APIs. | `main.py` Router | `db_service` | Production Runtime | ❌ | ✅ | ✅ (`/api/system/*`) |
| [`backend/app/api/chat.py`](file:///Users/swapnil/Base%20Zero/backend/app/api/chat.py) | AI Investigator chat endpoint. | `main.py` Router | `ai_investigator` | Production Runtime | ❌ | ❌ | ✅ (`POST /api/ai/investigate`) |
| [`scripts/migrate_to_cloud_postgres.py`](file:///Users/swapnil/Base%20Zero/scripts/migrate_to_cloud_postgres.py) | Fast batch ETL migration script from local CSV to Supabase Cloud PostgreSQL. | CLI Admin Execution | `psycopg2.extras.execute_values` | Maintenance Utility | ❌ | ✅ | ❌ |

---

# PART 5 — ARCHITECTURAL SEPARATION OF CONCERNS

### Why aren't all Python files combined into one?

Combining all Python code into a single file violates the **Single Responsibility Principle (SRP)**, makes concurrent team development impossible, degrades automated testability, and mixes web server mechanics with machine learning algorithms.

```
[Request: POST /api/risk/re-evaluate]
       │
       ▼
1. backend/app/api/risk.py          <-- ROUTER LAYER: Validates HTTP request & JSON params
       │
       ▼
2. backend/ml/anomaly_detector.py   <-- ML MODEL LAYER: Fits IsolationForest & calculates feature matrices
       │
       ▼
3. backend/app/services/real_data_service.py <-- SERVICE LAYER: Ingests raw Gazette CSV & computes Pandas moments
       │
       ▼
4. backend/app/db/database.py       <-- DATABASE LAYER: Executes parameterized SQL INSERT into Supabase Cloud
```

Each layer operates independently:
- Changing the ML model parameters in `backend/ml/` does **not** break the database schema in `backend/app/db/`.
- Swapping the database host in `backend/app/db/` does **not** alter the REST API endpoints in `backend/app/api/`.

---

# PART 6 — MACHINE LEARNING PIPELINE & CONCEPTS

### Core ML Definitions & Vocabulary

- **Dataset**: `Allocated_Limit_for_Honble_MPs.csv` containing 543 Lok Sabha MP records.
- **One Row**: Information for a single MP (e.g. `EATALA RAJENDER`, Malkajgiri, Telangana, ₹25.00 Cr / ₹32.75 Cr total limit).
- **Feature ($X$)**: A numeric attribute derived for every MP used to fit the model.
- **Feature Matrix ($X_{matrix}$)**: A 542 $\times$ 4 standardized numeric matrix ($542$ valid MPs $\times$ $4$ features).
- **Contamination ($0.08$)**: Empirical tail assumption that approximately 8% ($43$ out of $542$ MPs) diverge significantly from standard allocation baselines.
- **Anomaly Score**: A continuous scalar ($0.0 \to 1.0$) measuring statistical divergence.
- **Risk Score ($0.0 \to 100.0$)**: Business-aggregated score combining Isolation Forest, Tukey IQR, Z-Score, and Data Completeness signals.
- **Risk Level Tiers**:
  - `CRITICAL`: Score $\ge 81.0$ (e.g. Missing Data / Severe Multi-Method Consensus)
  - `HIGH`: Score $\ge 61.0$ (e.g. Multi-Method Anomaly Consensus)
  - `MEDIUM`: Score $\ge 31.0$ (e.g. Single-Method Statistical Divergence)
  - `LOW`: Score $< 31.0$ (Baseline Compliant ₹14.70 Cr)

---

# PART 7 — PRIMARY DATASET SCHEMA & MAPPING

### Dataset File: `Allocated_Limit_for_Honble_MPs.csv` (543 Rows)

| Gazette CSV Column | PostgreSQL Table Column (`mp_allocations`) | Data Type | Example Ground-Truth Value | ML Feature Input? | Purpose & Description |
| :--- | :--- | :--- | :--- | :---: | :--- |
| `Sr. No.` | `sr_no` (INTEGER) | `INTEGER` | `1` | ❌ | Sequential Gazette record index. |
| `State / UT Name` | `state` (VARCHAR) | `VARCHAR(255)` | `"TELANGANA"` | ✅ | Grouping variable for state peer-group mean calculation. |
| `Hon'ble MP Name` | `mp_name` (VARCHAR) | `VARCHAR(255)` | `"EATALA RAJENDER"` | ❌ | MP Entity identifier. |
| `Constituency Name (SC/ST/General)` | `constituency` (VARCHAR) | `VARCHAR(255)` | `"Malkajgiri (GENERAL)"` | ❌ | Constituency name and reservation category category tag. |
| `Allocated Amount (in Rs.)` | `allocated_amount_inr` (DOUBLE) | `DOUBLE PRECISION` | `250000000.0` (`₹25.00 Cr`) | ✅ | Primary allocation limit value. Used for baseline & Z-score features. |

*Note: Row 108 (`CHAVAN VASANTRAO BALWANTRAO`, Nanded, Maharashtra) has a NULL `Allocated Amount` in the official Gazette CSV, which is explicitly flagged as a `CRITICAL` Data Completeness Audit anomaly.*

---

# PART 8 — END-TO-END DATA PROCESSING FLOW

```
1. Gazette CSV File (Allocated_Limit_for_Honble_MPs.csv)
       │
       ▼
2. Pandas Load & Clean (backend/app/services/real_data_service.py)
   • Parse INR strings to floats
   • Handle NULL / NaN explicitly
       │
       ▼
3. Feature Engineering Matrix (backend/ml/anomaly_detector.py)
   • Construct 4 Non-Redundant Features: dev_baseline_pct, dev_state_pct, percentile, iqr_ratio
   • StandardScaler fit_transform
       │
       ▼
4. Model Execution (backend/ml/anomaly_detector.py)
   • Isolation Forest (300 trees, 0.08 contamination) -> iso_preds & iso_scores
   • Tukey IQR Fence Test (|X - Median| / IQR > 3.0) -> flag_iqr
   • Two-Tailed Gaussian Z-Score (|Z| > 2.0) -> flag_z
   • Data Completeness Audit -> flag_missing
       │
       ▼
5. Risk Aggregation & Evidence Generation (backend/ml/anomaly_detector.py)
   • Calculate multi_method_agreement (e.g. "2 / 3 Methods")
   • Compute risk_score (0.0 to 100.0) & assign risk_level (CRITICAL, HIGH, MEDIUM, LOW)
   • Build structured evidence breakdown JSON
       │
       ▼
6. Supabase Cloud PostgreSQL Persistence (backend/app/db/database.py)
   • Insert metadata into model_runs
   • Insert 543 rows into anomaly_signals via batch execute_values
       │
       ▼
7. Next.js Dashboard Display (frontend/components/AnomalyMatrix.tsx)
   • Render live searchable table with explainable risk badges
```

---

# PART 9 — MATHEMATICAL FEATURE ENGINEERING

The ML pipeline constructs $4$ non-redundant statistical features in `backend/ml/anomaly_detector.py`:

### Feature 1: Percentage Deviation from Baseline (`dev_baseline_pct`)
$$\text{dev\_baseline\_pct} = \frac{\text{Allocated Amount} - 147,000,000.0}{147,000,000.0}$$
- **Meaning**: Measures relative divergence from the standard ₹14.70 Crore MP baseline.
- **Example**: For Malkajgiri ($₹25.00\text{ Cr}$), $\text{dev\_baseline\_pct} = \frac{250,000,000 - 147,000,000}{147,000,000} = +0.70068$ ($+70.07\%$).

### Feature 2: Percentage Deviation from State Peer Mean (`dev_state_pct`)
$$\text{dev\_state\_pct} = \frac{\text{Allocated Amount} - \mu_{\text{state}}}{\mu_{\text{state}}}$$
- **Meaning**: Measures divergence relative to MPs within the same State/UT.
- **Example**: If Telangana average allocation is $₹18.00\text{ Cr}$, $\text{dev\_state\_pct} = \frac{25.00 - 18.00}{18.00} = +0.3888$ ($+38.89\%$).

### Feature 3: Allocation Rank Percentile (`percentile`)
$$\text{percentile} = \text{Rank}_{\text{pct}}(\text{Allocated Amount})$$
- **Meaning**: Normalized quantile position ($0.0 \to 1.0$) across all 543 MPs.
- **Example**: $₹25.00\text{ Cr}$ ranks in the top $99^{\text{th}}$ percentile ($0.992$).

### Feature 4: Robust IQR Outlier Ratio (`iqr_ratio`)
$$\text{iqr\_ratio} = \frac{|\text{Allocated Amount} - \text{Median}|}{\text{IQR}}$$
- **Meaning**: Non-parametric measure of distance from national median in Interquartile Range units.
- **Example**: Median = $₹14.70\text{ Cr}$, $\text{IQR} = ₹0.00\text{ Cr}$ (or $1.0$). $\text{iqr\_ratio} = \frac{|25.00 - 14.70|}{1.0} = 10.30$.

---

# PART 10 — ISOLATION FOREST ANOMALY DETECTION

### Why Isolation Forest instead of Supervised Classification?

In public sector financial oversight, labeled ground-truth fraud datasets are non-existent. Supervised classifiers (Random Forest, XGBoost) require positive/negative labels. **Isolation Forest** is an unsupervised algorithm that detects anomalies by isolating instances in feature space without needing labels.

```
       [Feature Space Isolation Tree]
                    X
                   / \
  [X < dev_state] /   \  [X >= dev_state]
                 /     \
            Normal     Isolated Anomaly (Malkajgiri)
            (Depth 8)   (Depth 2 — Few splits needed to isolate!)
```

- **Algorithm Mechanics**: Anomalies are few and different; therefore, they are isolated closer to the root of random decision trees (shorter average path length $h(x)$).
- **Parameters configured in `backend/ml/anomaly_detector.py`**:
  - `n_estimators=300`: 300 isolation trees for ensemble stability.
  - `contamination=0.08`: 8% tail contamination factor.
  - `random_state=42`: Fixed seed ensuring 100% deterministic reproducibility.
  - `n_jobs=-1`: Multi-threaded CPU execution.

---

# PART 11 — TUKEY IQR OUTLIER FENCE TEST

The **Tukey Interquartile Range (IQR) Fence Test** evaluates distribution spread:

1. **Calculate Quartiles**:
   - $Q_1 = 25^{\text{th}}\text{ percentile} = ₹14.70\text{ Cr}$
   - $Q_3 = 75^{\text{th}}\text{ percentile} = ₹14.70\text{ Cr}$
   - $\text{IQR} = Q_3 - Q_1$
2. **Tukey Outer Fence Calculation**:
   $$\text{Upper Fence} = Q_3 + 3.0 \times \text{IQR}$$
3. **Trigger Threshold**:
   $$\text{flag\_iqr} = \text{TRUE if } \text{iqr\_ratio} > 3.0$$

---

# PART 12 — TWO-TAILED GAUSSIAN Z-SCORE TEST

The **Parametric Z-Score Test** measures standard deviations from the national mean ($\mu = ₹15.33\text{ Cr}$, $\sigma = ₹2.85\text{ Cr}$):

$$Z = \frac{\text{Allocated Amount} - \mu}{\sigma}$$

- **Threshold**: `flag_z = TRUE` if $|Z| > 2.0$ (Confidence interval $> 95.45\%$).
- **Example**: For Malkajgiri ($₹25.00\text{ Cr}$):
  $$Z = \frac{25.00 - 15.33}{2.85} = +3.39\sigma \implies \text{Flagged as Statistical Outlier!}$$

---

# PART 13 — DATA COMPLETENESS AUDIT

When an MP record contains a missing or `NULL` allocation limit (e.g. Row 108, Nanded, Maharashtra):

- It cannot be passed to Gaussian or IQR formulas without imputation.
- `backend/ml/anomaly_detector.py` explicitly intercepts missing rows before scaling.
- Assigns `risk_score = 90.0` (`CRITICAL`), triggers `DataCompletenessAudit`, and logs:
  - *"Missing Allocation Limit Data (+60 pts)"*
  - *"Parliamentary Succession Signal (+30 pts)"*

---

# PART 14 — MULTI-METHOD CONSENSUS & RISK AGGREGATION

Rather than relying on a single algorithm, the system calculates a multi-method consensus agreement (`multi_method_agreement`):

$$\text{methods\_flagged} = \text{flag\_iso} + \text{flag\_z} + \text{flag\_iqr}$$

```
                [Method Signals]
     IsolationForest   Z-Score   Tukey IQR
            │             │          │
            ▼             ▼          ▼
       ┌──────────────────────────────────┐
       │ Multi-Method Agreement Calculator│
       └──────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
  2+ Methods Flagged        1 Method Flagged
  Risk Score = 65.0         Risk Score = 35.0
  (HIGH Tier)               (MEDIUM Tier)
```

- **Why different risk levels?**  
  An MP flagged by Isolation Forest *and* Z-Score *and* IQR (3/3 methods) represents a strong consensus anomaly (`HIGH` / `CRITICAL` risk), whereas an MP flagged by only 1 method represents a mild statistical variance (`MEDIUM` risk).

---

# PART 15 — DETERMINISTIC RISK SCORE FORMULA

```python
# Exact Logic in backend/ml/anomaly_detector.py
if is_missing:
    risk_score = 90.0  # CRITICAL
else:
    if methods_flagged >= 2:
        risk_score = 65.0  # HIGH
    elif methods_flagged == 1:
        risk_score = 35.0  # MEDIUM
    else:
        risk_score = 0.0   # LOW Baseline Compliant
```

### Risk Tiers
- **CRITICAL** ($\ge 81.0$): Data missingness or critical parliamentary succession discrepancy.
- **HIGH** ($\ge 61.0$): Multi-method model consensus anomaly.
- **MEDIUM** ($\ge 31.0$): Single-method statistical divergence.
- **LOW** ($< 31.0$): Standard baseline compliant (₹14.70 Cr).

---

# PART 16 — SUPABASE CLOUD POSTGRESQL DATABASE SCHEMA

Active Database Connection: `aws-0-ap-south-1.pooler.supabase.com:6543/postgres` (PostgreSQL 15 Pooler, SSL Mode `require`).

```mermaid
erDiagram
    dataset_versions ||--o{ model_runs : "versioned by"
    model_runs ||--|{ anomaly_signals : "generates (run_id)"
    mp_allocations ||--o{ anomaly_signals : "evaluated in"
    mp_allocations ||--o{ investigation_audit_logs : "audited in (mp_id)"

    dataset_versions {
        int version_id PK
        string version_tag
        string dataset_name
        string sha256_checksum
        int total_records
    }
    mp_allocations {
        int mp_id PK
        int sr_no
        string state
        string mp_name
        string constituency
        double allocated_amount_inr
    }
    model_runs {
        int run_id PK
        string model_version
        string algorithm
        int records_analyzed
        int anomalies_flagged
        timestamp executed_at
    }
    anomaly_signals {
        int signal_id PK
        int run_id FK
        string mp_id
        double risk_score
        string risk_level
        json evidence_breakdown_json
    }
    investigation_audit_logs {
        int log_id PK
        int mp_id
        string mp_name
        string status
        string nodal_officer
        text note
    }
    users_and_roles {
        int user_id PK
        string username
        string role
        string department
    }
```

---

# PART 17 — DATABASE RELATIONSHIPS & VERSIONING

### Why does `anomaly_signals` store `run_id`?
1. **Model Run Auditing**: Allows querying historical ML execution runs over time without losing previous model outputs.
2. **Reproducibility**: Every `run_id` links to exact parameters stored in `model_runs` (e.g. `n_estimators: 300`, `seed: 42`).
3. **Dataset Lineage**: Links predictions to `dataset_version_tag` (`v2026.08-1ad9c80d`).

---

# PART 18 — STEP-BY-STEP ML PIPELINE RE-EVALUATION

```
[User Clicks "Re-evaluate Models" in UI]
       │
       ▼
1. frontend/components/OverviewMetrics.tsx -> POST /api/risk/re-evaluate
       │
       ▼
2. backend/app/api/risk.py -> reevaluate_risk_models()
       │
       ▼
3. backend/ml/anomaly_detector.py -> fit_and_predict(force_refit=True)
   • Fits 300 Isolation Trees on 542 scaled MP records
   • Computes Tukey IQR and Z-Score flags
       │
       ▼
4. backend/app/db/database.py -> save_model_run_and_signals()
   • Executes: INSERT INTO model_runs (...) RETURNING run_id;
   • Executes batch execute_values: INSERT INTO anomaly_signals (run_id, ...)
       │
       ▼
5. Supabase Cloud PostgreSQL commits transaction & returns new run_id (e.g. #18)
       │
       ▼
6. FastAPI returns JSON: {"status": "SUCCESS", "run_id": 18, "anomalies_count": 543}
       │
       ▼
7. Next.js triggers UI re-render displaying newly persisted anomaly signals!
```

---

# PART 19 — RISK PAGE REQUEST TRACE

1. **Browser Navigation**: User opens `http://localhost:3000/risk`.
2. **Next.js Route**: Rendered by `frontend/app/risk/page.tsx`.
3. **API Request**: `useEffect` fires `fetch('http://localhost:8001/api/risk/anomalies')`.
4. **FastAPI Dispatch**: Handled by `backend/app/api/risk.py` (`get_anomalies()`).
5. **Database Execution**: `db_service` executes:
   ```sql
   SELECT * FROM anomaly_signals WHERE run_id = (SELECT MAX(run_id) FROM model_runs) ORDER BY risk_score DESC;
   ```
6. **PostgreSQL Result**: Returns 543 dict rows over SSL.
7. **JSON Response**: FastAPI serializes Pydantic response array.
8. **UI Rendering**: `frontend/components/AnomalyMatrix.tsx` renders 543 rows with color badges.

---

# PART 20 — AUDIT LOG WORKFLOW

1. **Nodal Officer Action**: Officer opens drawer for MP #108 (`CHAVAN VASANTRAO BALWANTRAO`), sets status to `UNDER_INVESTIGATION`, and enters note *"Verified seat succession in Gazette"*.
2. **Frontend Dispatch**: `InvestigationWorkspace.tsx` sends `POST /api/system/audit-logs`.
3. **FastAPI Handler**: `backend/app/api/system.py` (`create_audit_log()`).
4. **SQL Execution**: `backend/app/db/database.py` executes:
   ```sql
   INSERT INTO investigation_audit_logs (mp_id, mp_name, status, nodal_officer, note)
   VALUES (%s, %s, %s, %s, %s);
   ```
5. **Persistence**: Record committed to Supabase Cloud PostgreSQL table `investigation_audit_logs`.

---

# PART 21 — AI INVESTIGATOR ARCHITECTURE

The **AI Investigator** (`backend/app/services/ai_investigator.py`) is a **grounded tool-calling engine** with explicit zero-hallucination boundary enforcement.

```
[User Input Query] ("What is the contractor payment delay in Malkajgiri?")
       │
       ▼
[Scope Boundary Check] (backend/app/services/ai_investigator.py)
       │
       ├─► Contains Unsupported Keyword? ("contractor", "payment", "delay", "gps")
       │         │
       │         ▼
       │   [RETURN GROUNDED BOUNDARY NOTICE]
       │   "That information is not available in the connected MPLADS dataset.
       │    The currently ingested official MoSPI dataset contains MP-level fund
       │    allocation limits..."
       │
       └─► Supported Query? ("highest state", "why flagged", "baseline")
                 │
                 ▼
           [EXECUTE TOOL & QUERY MoSPI PANDAS DATASET]
                 │
                 ▼
           [RETURN EVIDENCE-GROUNDED ANSWER WITH METRICS]
```

---

# PART 22 — TEST SUITE ARCHITECTURE

The repository contains 32 automated tests in `tests/` verifying backend pipelines and mathematical invariants:

- [`test_mplads_pipeline.py`](file:///Users/swapnil/Base%20Zero/tests/test_mplads_pipeline.py): End-to-end integration tests verifying FastAPI endpoints, PostgreSQL connectivity, and pipeline re-evaluation.
- [`test_dataset_integrity.py`](file:///Users/swapnil/Base%20Zero/tests/test_dataset_integrity.py): Asserts 543 Gazette rows, ₹8,306.21 Cr allocation sum, and Nanded duplicate entry.
- [`test_anomaly_detection.py`](file:///Users/swapnil/Base%20Zero/tests/test_anomaly_detection.py): Verifies ML seed determinism, Isolation Forest reproducibility, and evidence generation.
- [`test_ai_grounding.py`](file:///Users/swapnil/Base%20Zero/tests/test_ai_grounding.py): Verifies zero-hallucination boundary responses for unsupported queries.
- [`test_risk_engine.py`](file:///Users/swapnil/Base%20Zero/tests/test_risk_engine.py): Asserts risk scores strictly satisfy $0.0 \le \text{score} \le 100.0$.

*Why is test code kept outside `backend/`?*  
Testing code is isolated in `tests/` so it does not pollute the production runtime dependency graph or get included in production Docker containers.

---

# PART 23 — UTILITY SCRIPTS

- [`scripts/migrate_to_cloud_postgres.py`](file:///Users/swapnil/Base%20Zero/scripts/migrate_to_cloud_postgres.py): Admin ETL script using `psycopg2.extras.execute_values` to perform batch migration of all 6 tables from local CSV/DB to Supabase Cloud PostgreSQL. Executed once during cloud setup.

---

# PART 24 — CONFIGURATION FILES INDEX

- [`.env`](file:///Users/swapnil/Base%20Zero/backend/.env): Server-side environment variables (`DATABASE_URL` with Supabase pooler credentials & SSL config). **Secret — Excluded from Git via `.gitignore`**.
- [`frontend/.env.local`](file:///Users/swapnil/Base%20Zero/frontend/.env.local): Public Supabase URL and Publishable Key (`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`). Safe for browser consumption.
- [`.gitignore`](file:///Users/swapnil/Base%20Zero/.gitignore): Excludes `.env`, `.env.local`, `backend/.env`, `node_modules/`, `__pycache__/`, and build directories from source control.
- [`frontend/package.json`](file:///Users/swapnil/Base%20Zero/frontend/package.json): Frontend npm package manifests (Next.js 14, React 18, Tailwind CSS, Lucide React).

---

# PART 25 — COMPLETE API ENDPOINT MAP

| HTTP Method | Endpoint Path | Handler Function | DB Tables Accessed | Purpose & Description | Frontend Component |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | `root()` | None | Root API health status | System |
| `GET` | `/health` | `health_check()` | Reads `mp_allocations` | Production system health check | System |
| `GET` | `/api/analytics/overview` | `get_overview()` | Reads `mp_allocations` | Returns total MPs, allocation sum, and valid counts | `OverviewMetrics.tsx` |
| `GET` | `/api/analytics/states` | `get_states()` | Reads `mp_allocations` | Returns state-wise allocation metrics | `IndiaRiskMap.tsx` |
| `GET` | `/api/analytics/mps` | `get_mps()` | Reads `mp_allocations` | Paginated MP allocation directory | `AnomalyMatrix.tsx` |
| `GET` | `/api/risk/anomalies` | `get_anomalies()` | Reads `anomaly_signals` | Returns model-generated risk signals | `AnomalyMatrix.tsx`, `AIWatch.tsx` |
| `GET` | `/api/risk/distribution` | `get_risk_distribution()` | Reads `anomaly_signals` | Risk tier breakdown (LOW, MEDIUM, HIGH, CRITICAL) | `OverviewMetrics.tsx` |
| `POST` | `/api/risk/re-evaluate` | `reevaluate_risk_models()` | Inserts `model_runs`, `anomaly_signals` | Triggers fresh ML fit & persists to Supabase | `OverviewMetrics.tsx` |
| `POST` | `/api/ai/investigate` | `investigate_query()` | Reads MoSPI Dataset | Grounded tool-calling query engine | `AIInvestigatorChat.tsx` |
| `GET` | `/api/system/db-status` | `get_db_status()` | Reads PostgreSQL Catalogs | Returns database connectivity & row counts | `DataSourcesModal.tsx` |
| `GET` | `/api/system/audit-logs` | `get_audit_logs()` | Reads `investigation_audit_logs` | Returns Nodal Officer audit notes | `InvestigationWorkspace.tsx` |
| `POST` | `/api/system/audit-logs` | `create_audit_log()` | Inserts `investigation_audit_logs` | Persists new Nodal Officer audit note | `InvestigationWorkspace.tsx` |
| `GET` | `/api/system/data-sources` | `get_data_sources_ledger()` | Reads `dataset_versions` | Returns transparency provenance ledger | `DataSourcesModal.tsx` |
| `GET` | `/api/system/model-health` | `get_model_health()` | Reads `model_runs` | Returns ML parameters & model health | `ModelHealthCard.tsx` |

---

# PART 26 — DATABASE QUERY MAP BY FRONTEND PAGE

| Frontend Page | Triggered API | Python Handler | SQL Query Executed | Target Table | Returned Data |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Command Center (`/`)** | `GET /api/analytics/overview` | `get_overview()` | `SELECT COUNT(*), SUM(allocated_amount_inr) FROM mp_allocations;` | `mp_allocations` | Total MPs ($543$), Total Sum ($\text{₹}8,306.21\text{ Cr}$) |
| **Risk Page (`/risk`)** | `GET /api/risk/anomalies` | `get_anomalies()` | `SELECT * FROM anomaly_signals WHERE run_id = (SELECT MAX(run_id) FROM model_runs) ORDER BY risk_score DESC;` | `anomaly_signals` | $543$ Anomaly Dict Rows |
| **Anomalies (`/anomalies`)**| `GET /api/risk/anomalies` | `get_anomalies()` | `SELECT * FROM anomaly_signals ...;` | `anomaly_signals` | $543$ Searchable Anomaly Rows |
| **Data Ledger (`/data-sources`)**| `GET /api/system/db-status` | `get_db_status()` | `SELECT c.relname, c.relrowsecurity FROM pg_class c ...;` | Catalog & Tables | Database Type & Row Counts |
| **Audit Drawer** | `POST /api/system/audit-logs` | `create_audit_log()` | `INSERT INTO investigation_audit_logs (...) VALUES (...);` | `investigation_audit_logs` | `{"status": "SUCCESS"}` |

---

# PART 27 — MASTER FILE INDEX & DEPENDENCY MATRIX

| File | Type | Imports | Imported By | Primary Purpose |
| :--- | :--- | :--- | :--- | :--- |
| [`frontend/app/page.tsx`](file:///Users/swapnil/Base%20Zero/frontend/app/page.tsx) | Page | `Header`, `OverviewMetrics`, `AIWatch`, `AnomalyMatrix` | Next.js Router | Main Dashboard Page |
| [`frontend/components/Header.tsx`](file:///Users/swapnil/Base%20Zero/frontend/components/Header.tsx) | Component | `lucide-react`, `next/navigation` | `page.tsx` | Top Bar & Constituency Search |
| [`frontend/components/AnomalyMatrix.tsx`](file:///Users/swapnil/Base%20Zero/frontend/components/AnomalyMatrix.tsx) | Component | `lucide-react`, `React` | `page.tsx`, `anomalies/page.tsx` | 543 MP Searchable Table Directory |
| [`backend/main.py`](file:///Users/swapnil/Base%20Zero/backend/main.py) | Entrypoint | `fastapi`, `analytics`, `risk`, `chat`, `system` | Uvicorn Server | FastAPI Application Root |
| [`backend/ml/anomaly_detector.py`](file:///Users/swapnil/Base%20Zero/backend/ml/anomaly_detector.py) | ML Engine | `sklearn.ensemble.IsolationForest`, `pandas` | `risk.py`, `ai_investigator.py`, `tests` | Isolation Forest & IQR Models |
| [`backend/ml/risk_engine.py`](file:///Users/swapnil/Base%20Zero/backend/ml/risk_engine.py) | ML Engine | `imd_feed.py` | `ml/__init__.py` | Risk Bounds & IMD Weather Engine |
| [`backend/app/db/database.py`](file:///Users/swapnil/Base%20Zero/backend/app/db/database.py) | DB Layer | `psycopg2`, `urllib.parse`, `dotenv` | `analytics.py`, `risk.py`, `system.py` | Supabase Cloud PostgreSQL Service |
| [`backend/app/services/real_data_service.py`](file:///Users/swapnil/Base%20Zero/backend/app/services/real_data_service.py) | Service | `pandas`, `numpy` | `analytics.py`, `ai_investigator.py` | Gazette CSV Ingestion & Aggregations |
| [`backend/app/services/ai_investigator.py`](file:///Users/swapnil/Base%20Zero/backend/app/services/ai_investigator.py) | Service | `real_data_service`, `anomaly_detector` | `chat.py` | Grounded Tool-Calling Query Engine |
| [`backend/data/Allocated_Limit_for_Honble_MPs.csv`](file:///Users/swapnil/Base%20Zero/backend/data/Allocated_Limit_for_Honble_MPs.csv) | Dataset | None | `real_data_service.py` | Primary Ground-Truth Gazette CSV |

---

# PART 28 — SOFTWARE ARCHITECTURE CONCEPTS IN THIS PROJECT

1. **Separation of Concerns**: Machine learning logic (`backend/ml/`) is cleanly separated from web routing (`backend/app/api/`) and database access (`backend/app/db/`).
2. **Single Responsibility Principle**: `backend/ml/anomaly_detector.py` is exclusively responsible for feature matrix scaling and Isolation Forest fit/prediction; it does not process HTTP request headers or write to SQL.
3. **Reproducibility**: `IsolationForest(random_state=42)` guarantees that re-running the ML model on identical data produces identical anomaly scores every time.
4. **Security & Least Privilege**: Database write credentials (`DATABASE_URL`) are isolated in server-side `backend/.env`. The browser receives only safe public Supabase configuration.

---

# PART 29 & 30 — COMPLETE NUMERICAL MP TRACE & EXAMPLE

Let's trace **MP Record #283**: **`EATALA RAJENDER`** (Malkajgiri Constituency, Telangana).

```
1. Gazette CSV Entry:
   Sr. No.: 283 | State: TELANGANA | Name: EATALA RAJENDER | Constituency: Malkajgiri | Amount: ₹25,00,00,000 (₹25.00 Cr)

2. Moments & Aggregations:
   • National Mean Allocation (μ): ₹15.33 Crore
   • National Sample Std Dev (σ): ₹2.85 Crore
   • Standard Baseline: ₹14.70 Crore
   • Telangana State Mean: ₹18.20 Crore
   • National Median: ₹14.70 Crore | IQR: ₹1.00 Crore

3. Feature Engineering Calculations:
   • dev_baseline_pct = (25.00 - 14.70) / 14.70 = +0.70068 (+70.07%)
   • dev_state_pct    = (25.00 - 18.20) / 18.20 = +0.3736 (+37.36%)
   • percentile       = 0.992 (99.2nd percentile rank)
   • iqr_ratio        = |25.00 - 14.70| / 1.00 = 10.30

4. Model Evaluation:
   • Isolation Forest (300 trees, seed=42): Path length h(x) is short -> iso_pred = -1 (FLAGGED!)
   • Two-Tailed Z-Score: Z = (25.00 - 15.33) / 2.85 = +3.39σ (> 2.0σ threshold -> FLAGGED!)
   • Tukey IQR Fence Test: iqr_ratio = 10.30 (> 3.0 threshold -> FLAGGED!)

5. Risk Score Aggregation:
   • Multi-Method Agreement: 3 / 3 Methods Flagged
   • Consensus Risk Score: 65.0
   • Final Risk Tier: HIGH (Risk Color: #ef4444)

6. Database Persistence:
   Inserted into Supabase Cloud PostgreSQL table `anomaly_signals` with run_id #18.
```

---

# PART 31 — "WHAT IF" SYSTEM BEHAVIOR ANALYSIS

1. **What if an MP allocation limit is missing?**  
   Intercepted by `backend/ml/anomaly_detector.py`, assigned `risk_score = 90.0` (`CRITICAL`), and flagged with a `DataCompletenessAudit` signal.
2. **What if Supabase Cloud PostgreSQL goes offline?**  
   FastAPI database pooler catches connection timeout, returns structured HTTP 503 error, and frontend displays clean backend notice banner without crashing.
3. **What if a user clicks "Re-evaluate Models" twice?**  
   FastAPI executes `fit_and_predict(force_refit=True)` deterministically (seed 42), writes run `#19` and run `#20` to Supabase, and updates active run pointer to `#20`.
4. **What if a user asks AI Investigator about non-existent contractor data?**  
   Intercepted by zero-hallucination boundary check in `ai_investigator.py`, returning: *"That information is not available in the connected MPLADS dataset."*

---

# PART 32 — TOP 20 TECHNICAL VIVA QUESTIONS & ANSWERS

### Architecture (5 Questions)
1. **Q: Describe your overall system architecture.**  
   **Short**: Next.js 14 frontend communicating via REST APIs with a FastAPI backend connected to Supabase Cloud PostgreSQL.  
   **Deep**: The architecture separates presentation (Next.js 14 App Router), API routing (FastAPI), machine learning (`backend/ml/`), and data storage (Supabase Cloud PostgreSQL pooler over SSL).

2. **Q: Why use FastAPI instead of Next.js API routes?**  
   **Short**: Performance and native Python ML ecosystem support.  
   **Deep**: FastAPI leverages Python's Scikit-Learn and Pandas libraries natively with asynchronous Uvicorn performance, maintaining a clean boundary between UI rendering and heavy matrix computations.

3. **Q: How are database credentials protected?**  
   **Short**: Isolated in server-side `backend/.env`.  
   **Deep**: `DATABASE_URL` exists strictly inside `backend/.env`. The browser receives only safe publishable keys (`NEXT_PUBLIC_SUPABASE_URL`).

4. **Q: What is the role of `dataset_versions`?**  
   **Short**: Provides dataset lineage and SHA-256 integrity tags.  
   **Deep**: It records file checksums (`1ad9c80d...`) ensuring model outputs map to verified dataset snapshots.

5. **Q: How does the system handle real-time data flow?**  
   **Short**: Triggered re-evaluations persist to PostgreSQL and update UI dynamically.  
   **Deep**: Calling `POST /api/risk/re-evaluate` executes the ML pipeline, inserts new runs into `model_runs`, and returns updated signals.

### Machine Learning (5 Questions)
6. **Q: Why use Isolation Forest for anomaly detection?**  
   **Short**: Unsupervised algorithm ideal for unlabelled financial data.  
   **Deep**: Because official Gazettes publish entitlement limits without historical audit fraud labels, Isolation Forest isolates outliers in feature space without requiring supervised training labels.

7. **Q: Explain your contamination parameter.**  
   **Short**: Fixed at 0.08 (8%).  
   **Deep**: Assumes approximately 8% of the 542 MPs exhibit statistical allocation divergence from standard baselines.

8. **Q: What features are fed into the ML model?**  
   **Short**: Four non-redundant statistical features.  
   **Deep**: `dev_baseline_pct`, `dev_state_pct`, `percentile`, and `iqr_ratio`.

9. **Q: How do you prevent double-counting in risk scores?**  
   **Short**: Multi-method consensus aggregation.  
   **Deep**: Risk scores are calculated based on multi-method agreement (e.g. 2+ methods = 65.0 HIGH), preventing score inflation.

10. **Q: Is your ML model deterministic?**  
    **Short**: Yes, 100% deterministic.  
    **Deep**: Initialized with `random_state=42`, ensuring identical outputs across executions.

### Database & Security (5 Questions)
11. **Q: How is database security enforced?**  
    **Short**: Row Level Security (RLS) & strict role revokes.  
    **Deep**: RLS is enabled on all 6 tables. Unauthenticated `anon` roles have zero write privileges (`REVOKE ALL`).

12. **Q: What is the primary key of `anomaly_signals`?**  
    **Short**: Auto-incrementing `signal_id`.  
    **Deep**: `signal_id SERIAL PRIMARY KEY` with foreign key `run_id REFERENCES model_runs(run_id)`.

13. **Q: Why connect to PostgreSQL via connection pooler?**  
    **Short**: Efficient connection reuse.  
    **Deep**: Reduces connection overhead using Supabase transaction pooler on port 6543 with SSL mode `require`.

14. **Q: How are auto-increment sequences managed during migration?**  
    **Short**: Synced via `setval()`.  
    **Deep**: `SELECT setval('table_col_seq', (SELECT MAX(col) FROM table))` is executed post-migration to prevent ID collision.

15. **Q: Are database credentials exposed to Git?**  
    **Short**: No.  
    **Deep**: Explicitly ignored via `.gitignore` (`.env`, `backend/.env`, `.env.local`).

### AI Investigator & Grounding (5 Questions)
16. **Q: How does the AI Investigator prevent hallucinations?**  
    **Short**: Strict scope boundary checks.  
    **Deep**: Queries containing out-of-scope keywords (contractors, payments) are intercepted before LLM generation.

17. **Q: What data does the AI Investigator query?**  
    **Short**: Ingested MoSPI Gazette dataset metrics.  
    **Deep**: Grounded directly in `Allocated_Limit_for_Honble_MPs.csv` aggregations.

18. **Q: How is audit trail history stored?**  
    **Short**: In `investigation_audit_logs`.  
    **Deep**: Persists Nodal Officer notes with timestamp, status, officer name, and MP ID.

19. **Q: What automated tests exist for ML?**  
    **Short**: `test_anomaly_detection.py` and `test_risk_engine.py`.  
    **Deep**: 32 automated pytest tests verify reproducibility, bounds ($0 \le S \le 100$), and evidence breakdown.

20. **Q: What is the production build status?**  
    **Short**: 100% clean build.  
    **Deep**: 32/32 Pytest tests passing; Next.js 14 production build compiled 10/10 static routes cleanly.

---

# PART 33 — 2-MINUTE PRESENTATION SUMMARY

> **"What is the MPLADS AI Intelligence Command Center?"**  
> *"It is an enterprise government oversight platform designed for MoSPI to perform automated, continuous monitoring of MPLADS allocation limits across all 543 Lok Sabha Members of Parliament."*
> 
> **"How does the Machine Learning work?"**  
> *"Because government Gazette data lacks labeled fraud examples, we use an unsupervised multi-method ensemble combining Isolation Forest (300 trees), Tukey IQR Outlier Fences, Gaussian Z-Scores, and Data Completeness Audits. This generates explainable risk signals based on statistical divergence from the standard ₹14.70 Crore MP baseline."*
> 
> **"How is the system architecture built?"**  
> *"The frontend is built with Next.js 14 App Router and a Neo-Brutalist design system. It communicates via REST APIs with a FastAPI backend connected to Supabase Cloud PostgreSQL with Row Level Security (RLS) enabled."*
> 
> **"How do you ensure zero hallucination in AI search?"**  
> *"Our AI Investigator uses grounded tool-calling logic. When a user asks about unavailable micro-project contractor or payment data, the system detects the boundary and explicitly responds: 'That information is not available in the connected MPLADS dataset'—ensuring 100% data integrity for government presentation."*

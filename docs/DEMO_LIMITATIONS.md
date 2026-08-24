# DEMO LIMITATIONS & DATA PROVENANCE — MPLADS COMMAND CENTER
**SIH Problem Statement ID**: SIH26102  
**Target Organization**: Ministry of Statistics and Programme Implementation (MoSPI)  
**Date**: August 25, 2026  

---

## 1. Data Classification Summary

| Feature / Domain | Data Provenance | Source File | Status & Handling |
| :--- | :--- | :--- | :--- |
| **MP Fund Allocation Limits** | **Official Verified Data** | `Allocated Limit for Honble MPs.csv` | 543 MP records, ₹83,06,21,04,294.53 total allocation ingested and verified. Single source of truth for all MP & State analytics. |
| **State Allocation Summaries** | **Calculated Analytics** | `Allocated Limit for Honble MPs.csv` | Derived strictly by aggregating official MP allocation records across 36 States/UTs. |
| **Allocation Risk Signals** | **Unsupervised ML Output** | Scikit-Learn IsolationForest + LOF | ML anomaly scores derived strictly from verified dataset features (`allocated_amount`, `dev_baseline`, `dev_state_mean`, `z_score_nat`). |
| **Project Expenditure / Work Progress** | **Isolated Demo Simulation** | `demo_data_service.py` | Simulated layer for UI demonstration. Explicitly tagged `"DEMO SIMULATION — NOT DERIVED FROM OFFICIAL MPLADS DATA"`. |
| **Contractors & Payment Anomalies** | **Isolated Demo Simulation** | `demo_data_service.py` | Entity graph simulation demonstrating extensible platform architecture. |

---

## 2. Analytical Honesty & Scope Boundaries

### What is Supported by Real Data:
- MP-level fund allocation limit monitoring.
- State-level allocation aggregates, averages, and national skews.
- Baseline divergence detection against standard ₹14.70 Crore MP entitlement limit.
- Isolation Forest and LOF statistical anomaly detection on allocation figures.
- Grounded AI Investigator answers for allocation queries.

### What Requires Additional Datasets:
- **Work-level expenditure & unspent balances**: Requires MoSPI project-level release dataset.
- **Contractor tender awards & vendor networks**: Requires e-Procurement / GeM vendor database.
- **PFMS payment transactions & bank disbursement dates**: Requires PFMS transaction ledger.
- **Physical progress % & geotagged site completion certificates**: Requires District Nodal geotagged inspection database.

*Notice: Backend services and API models are architected with modular interfaces so these additional datasets can be plugged in when provided.*

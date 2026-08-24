# ALLOCATION RISK SCORING METHODOLOGY — MPLADS COMMAND CENTER
**Methodology Version**: 2.0  
**Data Basis**: Official MoSPI `Allocated Limit for Honble MPs.csv`  

---

## 1. Risk Tier Specification

Each MP record is evaluated against a 0–100 risk scale:

| Risk Range | Tier Level | Visual Indicator | Recommended Action |
| :---: | :---: | :---: | :--- |
| **0 – 30** | **LOW** | Green (`#10b981`) | Standard Baseline Allocation (₹14.70 Cr). Normal monitoring. |
| **31 – 60** | **MEDIUM** | Amber (`#f59e0b`) | Moderate peer variance or minor statistical skew. Periodic audit. |
| **61 – 80** | **HIGH** | Red (`#ef4444`) | Flagged by Isolation Forest / LOF or extreme deviation (>30%). High priority review. |
| **81 – 100** | **CRITICAL** | Dark Red (`#dc2626`) | Data completeness anomaly (e.g. Row 108 missing amount) or dual seat entry. Immediate investigation. |

---

## 2. Supported Risk Signals & Impact Factors

1. **Data Completeness Risk Signal (+60 pts)**: Missing allocation limit entry in official CSV.
2. **Mid-Term Succession Signal (+30 pts)**: Duplicate constituency entry in CSV.
3. **Isolation Forest Outlier Signal (+35 pts)**: Flagged as anomalous in 4D feature space by IsolationForest.
4. **LOF Local Outlier Density Signal (+25 pts)**: Low density local outlier factor signal.
5. **Statistical Z-Score Skew (+15 to +35 pts)**: |Z-Score| > 1.5 standard deviations from national mean (₹15.33 Cr).
6. **State Peer Group Variance (+20 pts)**: Allocation deviates >25% from State average.

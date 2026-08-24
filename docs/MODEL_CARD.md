# MODEL CARD — MPLADS ANOMALY & RISK DETECTOR
**Model Name**: MPLADS Allocation Anomaly Detector v2.0  
**Model Type**: Unsupervised Multi-Method Anomaly Consensus Engine  
**Release Date**: August 25, 2026  
**Primary Dataset**: Official MoSPI Entitlement Register (`Allocated_Limit_for_Honble_MPs.csv`)  

---

## 1. Model Purpose & Intended Use
- **Purpose**: Screen official MoSPI Member of Parliament allocation limits to detect administrative anomalies, baseline divergences, state peer-group variances, and missing data signals.
- **Intended Users**: MoSPI Data Informatics & Innovation Division (DIID), District Nodal Officers, and Public Audit Researchers.
- **Out-of-Scope Uses**: Automatic criminal fraud determination, contractor blacklisting, or payment delay diagnosis without supplementary datasets.

---

## 2. Input Features & Preprocessing
The feature matrix uses **4 non-redundant normalized features**:
1. `dev_baseline_pct`: Normalized percentage deviation from standard $\text{₹}14.70\text{ Cr}$ baseline.
2. `dev_state_pct`: Normalized percentage deviation from local state average allocation.
3. `percentile`: Rank-based percentile ($0.0$ to $1.0$) across all $543$ MPs.
4. `iqr_ratio`: Robust IQR Outlier Ratio ($\frac{|X - \text{Median}|}{\text{IQR}}$).

- **Preprocessing**: Median Imputation for missing values + `StandardScaler()` zero-mean unit-variance scaling.

---

## 3. Algorithms & Configuration
1. **Isolation Forest**: `n_estimators=300`, `contamination=0.08`, `random_state=42`, `n_jobs=-1`.
2. **Parametric Z-Score**: Two-tailed Gaussian test ($|Z_{\text{sample}}| > 2.0$).
3. **Tukey IQR Outlier Detector**: Distributional spread test ($\text{IQR Ratio} > 3.0$).

---

## 4. Multi-Method Anomaly Consensus & Risk Engine
- **Risk Score Brackets**:
  - `3 / 3` or `2 / 3` Methods Flagged $\implies$ **HIGH ANOMALY CONSENSUS (Score 65.0 / HIGH)**
  - `1 / 3` Method Flagged $\implies$ **SINGLE MODEL SIGNAL (Score 35.0 / MEDIUM)**
  - `0 / 3` Methods Flagged $\implies$ **BASELINE COMPLIANT (Score 0.0 / LOW)**
  - Missing Data Flagged $\implies$ **DATA COMPLETENESS SIGNAL (Score 90.0 / CRITICAL)**

---

## 5. Unsupervised Model Validation
- **Ground Truth Fraud Labels**: **None available in official publication**.
- **Supervised Accuracy (F1/AUC)**: **Not Applicable**.
- **Top-20 Rank Stability**: **90.0% Overlap** across 5 independent random seeds (`seed = 42, 43, 44, 100, 2026`).

---

## 6. Analytical Limitations & Bias Considerations
- **Data Boundary**: Dataset contains MP entitlement limits only. Expenditure, contractors, and PFMS payment transactions require extensible dataset integration.
- **Inherited Policy Variations**: Mid-term seat succession and carry-over allocations legitimately cause baseline divergence and must be verified by Nodal Officers.

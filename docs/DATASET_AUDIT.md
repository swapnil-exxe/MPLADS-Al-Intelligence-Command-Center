# DATASET AUDIT — OFFICIAL MPLADS MP ALLOCATION DATASET
**Dataset File**: `Allocated Limit for Honble MPs.csv`  
**Storage Location**: `backend/data/Allocated_Limit_for_Honble_MPs.csv`  
**Verification Date**: August 25, 2026  

---

## 1. Verified Dataset Totals & Empirical Calculation

All numbers below have been calculated directly from the official CSV file:

| Metric | Recalculated Value | Exact Formula / Source | Notes & Verification |
| :--- | :--- | :--- | :--- |
| **Raw Line Count in File** | `544` lines | `len(df_raw)` | 1 Header + 542 Valid MP Rows + 1 Missing MP Row + 1 Grand Total Row |
| **Total MP Records** | `543` records | `len(df_data)` | Excludes the CSV Grand Total summary row |
| **Valid Allocation Rows** | `542` rows | `df['Allocated_Amount'].notna().sum()` | Rows with parseable monetary allocation figures |
| **Missing Allocation Rows** | `1` row | `df['Allocated_Amount'].isna().sum()` | **Row 108**: `CHAVAN VASANTRAO BALWANTRAO` (Nanded, Maharashtra) |
| **Calculated Total Sum** | `₹83,06,21,04,294.53` | `df['Allocated_Amount'].sum()` | Matches CSV Grand Total string `"83,06,21,04,294.53"` exactly |
| **Unique MP Names** | `543` names | `df['MP_Name'].nunique()` | Every MP record has a distinct name entry |
| **Unique States / UTs** | `36` entities | `df['State'].nunique()` | Covers 28 States and 8 Union Territories |
| **Unique Constituencies** | `542` names | `df['Constituency'].nunique()` | 542 unique names (Nanded appears twice) |
| **Duplicate Entities** | `1` duplicate | Constituency `NANDED` (Maharashtra) | Row 108 (Missing amount) & Row 390 (`₹14.70 Cr`) due to mid-term succession |

---

## 2. Real Allocation Statistical Distribution

- **Baseline Allocation**: $389$ MPs out of $543$ ($71.6\%$) are allocated exactly $\text{₹}14,70,00,000.00$ ($\text{₹}14.70\text{ Crore}$).
- **National Mean**: $\text{₹}15,32,51,114.93$ ($\text{₹}15.33\text{ Crore}$).
- **National Median**: $\text{₹}14,70,00,000.00$ ($\text{₹}14.70\text{ Crore}$).
- **Standard Deviation**: $\text{₹}2,00,13,952.78$ ($\text{₹}2.00\text{ Crore}$).
- **Minimum Allocation**: $\text{₹}4,90,00,000.00$ ($\text{₹}4.90\text{ Cr}$) — `SK NURUL ISLAM` (`BASIRHAT`, West Bengal).
- **Maximum Allocation**: $\text{₹}32,74,77,390.86$ ($\text{₹}32.75\text{ Cr}$) — `EATALA RAJENDER` (`MALKAJGIRI`, Telangana).

---

## 3. Mandatory Rules for Data Separation & Limitations

### Rule 1: Zero Contamination of Official Data
Official statistics (State totals, MP rankings, National KPIs, Allocation averages) **MUST ONLY** be computed from `Allocated Limit for Honble MPs.csv`.

### Rule 2: Explicit Data Limitations
The official dataset contains **ONLY allocation limits per MP**. It does NOT contain:
- Project expenditure or unspent balances
- Physical progress percentages or completion dates
- Vendor / contractor names or payment transactions
- Project titles, categories, or GPS locations

### Rule 3: Extensible Architecture for Future Datasets
Backend models and APIs are architected with modular interfaces so additional project-level datasets can be ingested when made available by MoSPI.

### Rule 4: Isolated Demo Simulation Tagging
Any optional simulated project-level data created for demonstration purposes (e.g. project investigation view, fraud relationship graph) is kept strictly isolated in a separate `DemoDataService` and clearly tagged in the UI with:
`"DEMO SIMULATION — NOT DERIVED FROM OFFICIAL MPLADS DATA"`

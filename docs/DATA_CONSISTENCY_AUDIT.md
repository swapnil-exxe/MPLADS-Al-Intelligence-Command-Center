# DATA CONSISTENCY & GROUND TRUTH AUDIT
**Project**: SIH26102 — MPLADS AI Intelligence Command Center  
**Date**: August 25, 2026  
**Source of Truth**: `Allocated_Limit_for_Honble_MPs.csv` (Official MoSPI Dataset)  

---

## 1. Discrepancy Resolution & Raw CSV Ground Truth

A thorough audit of raw CSV values was conducted to resolve discrepancies between historical prompt mentions and actual ingested data:

| MP Name | Constituency | State | Historical Mention in Prompts | Raw CSV Ground Truth Value | Discrepancy Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **EATALA RAJENDER** | Malkajgiri | Telangana | ₹32.75 Cr | **₹32.7477 Cr** (₹327,477,390.86) | ✅ **Accurate** (Highest Allocation in Dataset) |
| **BANDI SANJAY KUMAR** | Karimnagar | Telangana | ₹30.00 Cr (in prompt text) | **₹17.2775 Cr** (₹172,775,317.11) | ⚠️ **Resolved**: Prompt text had typo; CSV is ₹17.28 Cr |
| **DR. M.P. ABDUSSAMAD SAMADANI** | Ponnani | Kerala | ₹29.40 Cr (in prompt text) | **₹17.0434 Cr** (₹170,434,031.11) | ⚠️ **Resolved**: Prompt text had typo; CSV is ₹17.04 Cr |
| **SK NURUL ISLAM** | Basirhat | West Bengal | ₹4.90 Cr | **₹4.9000 Cr** (₹49,000,000.00) | ✅ **Accurate** (Lowest Allocation in Dataset) |
| **T. R. BAALU** | Sriperumbudur | Tamil Nadu | ₹9.80 Cr (in prompt text) | **₹19.6906 Cr** (₹196,905,535.11) | ⚠️ **Resolved**: Prompt text had typo; CSV is ₹19.69 Cr |
| **CHAVAN VASANTRAO BALWANTRAO** | Nanded | Maharashtra | Missing | **MISSING (`NaN`)** | ✅ **Accurate** (Mid-term Seat Succession) |

---

## 2. Statistical Moments & Exact Z-Score Verification

### Empirical Dataset Moments ($N = 542$ Valid MP Allocations):
- **Mean ($\mu$)**: $\text{₹}15,32,51,114.93$ ($\text{₹}15.3251\text{ Cr}$)
- **Sample Standard Deviation ($\sigma_{\text{sample}}$)**: $\text{₹}2,00,13,952.78$ ($\text{₹}2.0014\text{ Cr}$)
- **Population Standard Deviation ($\sigma_{\text{pop}}$)**: $\text{₹}19,995,481.20$ ($\text{₹}1.9995\text{ Cr}$)
- **Median**: $\text{₹}14,70,00,000.00$ ($\text{₹}14.70\text{ Cr}$)
- **Interquartile Range ($\text{IQR} = Q_3 - Q_1$)**: $\text{₹}5,38,185.03$ ($\text{₹}5.38\text{ Lakhs}$, or $\text{₹}0.0538\text{ Cr}$)

### Exact Z-Score Formula Verification:
Using sample standard deviation $\sigma_{\text{sample}} = \text{₹}20,013,952.78$:

1. **EATALA RAJENDER** ($\text{₹}32.7477\text{ Cr}$):
   $$Z = \frac{327,477,390.86 - 153,251,114.93}{20,013,952.78} = \mathbf{+8.7052} \quad (+8.71)$$
2. **SK NURUL ISLAM** ($\text{₹}4.90\text{ Cr}$):
   $$Z = \frac{49,000,000.00 - 153,251,114.93}{20,013,952.78} = \mathbf{-5.2089} \quad (-5.21)$$
3. **T. R. BAALU** ($\text{₹}19.69\text{ Cr}$):
   $$Z = \frac{196,905,535.11 - 153,251,114.93}{20,013,952.78} = \mathbf{+2.1812} \quad (+2.18)$$
4. **BANDI SANJAY KUMAR** ($\text{₹}17.28\text{ Cr}$):
   $$Z = \frac{172,775,317.11 - 153,251,114.93}{20,013,952.78} = \mathbf{+0.9755} \quad (+0.98)$$
5. **DR. M.P. ABDUSSAMAD SAMADANI** ($\text{₹}17.04\text{ Cr}$):
   $$Z = \frac{170,434,031.11 - 153,251,114.93}{20,013,952.78} = \mathbf{+0.8585} \quad (+0.86)$$

*Conclusion*: Z-scores of $+8.71$ and $-5.21$ are 100% mathematically correct and consistent with $\sigma \approx \text{₹}2.00\text{ Cr}$.

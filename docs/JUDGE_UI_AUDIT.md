# BROWSER & UI/UX AUDIT — MPLADS AI INTELLIGENCE COMMAND CENTER
**SIH Problem Statement**: SIH26102 — Development of an AI-powered system to detect anomalies, fraud, and inefficiencies in MPLAD Scheme implementation regd.  
**Target Organization**: Ministry of Statistics and Programme Implementation (MoSPI) — Data Informatics & Innovation Division (DIID)  
**Date**: August 25, 2026  

---

## 1. First 10 Seconds Evaluation

| Evaluation Question | Audit Result | UI Implementation & Evidence |
| :--- | :--- | :--- |
| **1. What is this?** | **Instant Clarity** | "MPLADS AI INTELLIGENCE COMMAND CENTER — MoSPI DIID" |
| **2. What problem does it solve?** | **Clear Value Prop** | "AI-powered continuous monitoring of allocation anomalies, statistical skews, and risk signals across official MoSPI MPLADS records." |
| **3. Where is the AI?** | **Hero Prominence** | "AI WATCH — Continuous Anomaly Monitoring" displaying Isolation Forest + LOF real-time anomaly detection stream. |
| **4. What data is it monitoring?** | **Transparent Provenance** | "Official MoSPI Allocated Limit for Honble MPs.csv (543 MPs • 36 States/UTs • ₹8,306.21 Cr Total Ingested Allocation)" |
| **5. What action can an authority take?** | **Actionable Workflows** | "Investigate Anomaly", "Assign Nodal Officer", "Mark Verified & Resolve", "Ask AI Investigator". |

---

## 2. Component Design & Emil Kowalski Principles Review

| Component | Design Engineering Applied | Before/After Impact |
| :--- | :--- | :--- |
| **Header** | Crisp contrast (`#0d1322`), subtle borders, status indicators | Replaced generic navbar with official MoSPI Command Center header and live data ledger triggers. |
| **Overview Metrics** | High-density font-mono stats, subtle card glows | Replaced decorative cards with verified allocation metrics ($543$ MPs, $\text{₹}8,306.21\text{ Cr}$, $389$ baseline). |
| **AI WATCH (Hero)** | Dominant monitoring board, real-time counters, active pulse | Upgraded into hero section showing real backend anomaly counts ($45$ signals, $26$ high-priority cases). |
| **Why Flagged?** | Visual evidence bars, impact scores, grounded explanations | Displays exact mathematical factor breakdowns and mandatory disclaimer: *"ANOMALY SIGNAL ≠ PROOF OF FRAUD"*. |
| **Investigation Workspace** | Origin-aware drawer, audit trail, note logging | Provides deep-dive MP investigation flow and explicit **WHAT DATA IS MISSING?** section. |
| **AI Investigator** | Tool-execution logs, structured evidence format | Grounded conversational interface with zero-hallucination boundary checks. |

---

## 3. Responsive & Interaction Matrix

- **1440px Desktop**: Full 3-column Command Center view.
- **1280px Laptop**: Optimized layout with sticky sidebar and collapsible data drawer.
- **1024px / 768px Tablet**: Grid adapts gracefully with horizontal scrolling for matrices.
- **390px Mobile**: Priority order: Hero Banner $\rightarrow$ Overview Metrics $\rightarrow$ AI Watch $\rightarrow$ AI Investigator.

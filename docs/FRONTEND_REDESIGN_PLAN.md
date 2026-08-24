# FRONTEND MASTER REDESIGN & ARCHITECTURE PLAN
**SIH Problem Statement**: SIH26102 — Development of an AI-powered system to detect anomalies, fraud, and inefficiencies in MPLAD Scheme implementation.  
**Product Name**: MPLADS AI INTELLIGENCE — Government Monitoring & Risk Intelligence Platform  
**Target Organization**: Ministry of Statistics and Programme Implementation (MoSPI) — Data Informatics & Innovation Division (DIID)  
**Date**: August 25, 2026  

---

## 1. Design System & Tokens (Emil Kowalski Craft)

### Typography & Optical Sizing
- **Font Stack**: System UI (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`) with font-mono for metrics.
- **Headings**: Negative letter tracking (`letter-spacing: -0.02em`), tight line-height (`1.1`), bold/black weight.
- **Body**: Standard letter-spacing (`0`), line-height (`1.5`), crisp gray-blue text (`#9ca3af`).
- **Data / Metrics**: Monospaced font stack for alignment and rapid scanning.

### Palette & Semantic Colors
- **Canvas Base**: `#090d16` (Deep Navy Obsidian).
- **Secondary Surfaces**: `#0d1322`, `#111827` (Navy Charcoal).
- **Borders**: `rgba(255, 255, 255, 0.08)` (Subtle low-contrast hairline borders).
- **Semantic Risk Levels**:
  - **LOW**: `#10b981` (Emerald Green)
  - **MEDIUM**: `#f59e0b` (Amber Yellow)
  - **HIGH**: `#ef4444` (Rose Red)
  - **CRITICAL**: `#dc2626` (Deep Crimson Red)
- **AI Accent**: `#6366f1` (Restrained Indigo / Blue).

### Motion & Micro-Interactions (`animate`, `apple-design`)
- **Press Feedback**: `active:scale-[0.97]` on all pressable buttons and rows with `100ms var(--ease-out)`.
- **Physical Entrances**: Modals/drawers animate from `scale(0.95)` + `opacity: 0` (`.animate-entrance`).
- **Custom Easing**: `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)`, `--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1)`.
- **GPU Acceleration**: Animate strictly `transform` and `opacity`.
- **Pointer & Accessibility Gating**: `@media (hover: hover) and (pointer: fine)` and `@media (prefers-reduced-motion: reduce)`.

---

## 2. Route & Page Architecture

We implement Next.js App Router sub-routes and dynamic state views:

| Route Path | View / Component | Purpose |
| :--- | :--- | :--- |
| `/` | `CommandCenterPage` | Master Command Center (AI Watch Hero, KPIs, Map, Scope Card). |
| `/risk` | `RiskIntelligenceView` | Risk Distribution & High-Priority Anomaly Matrix. |
| `/anomalies` | `AnomalyMatrix` | Filterable MP Allocation Anomaly Stream. |
| `/fraud` | `FraudIntelligence` | Extensible Fraud Graph & Simulation Layer with explicit disclosures. |
| `/states` | `StateAnalyticsView` | State Ranking Table & Choropleth Analytics. |
| `/mps` | `AnomalyMatrix` | Full 543 MP Constituency Directory. |
| `/alerts` | `AlertCenterView` | Priority Early Warning System. |
| `/analytics` | `OverviewMetrics` | Deep Fund Analytics & Baseline Divergence. |
| `/investigator` | `AIInvestigatorChat` | Grounded Tool-Calling AI Investigator. |
| `/data-sources` | `DataSourcesModal` | Provenance Ledger (CSV verification). |
| `/model-health` | `ModelHealthCard` | ML Model Architecture & Validation Disclosure. |

---

## 3. Reusable Component Hierarchy

```
frontend/components/
├── app-shell/
│   ├── Header.tsx                 # MoSPI Header with AI Status & Data Provenance
│   └── SidebarNav.tsx             # Intelligence Workstation Navigation
├── ai-watch/
│   └── AIWatch.tsx                # Hero Monitoring Section (543 MPs, 45 Anomalies)
├── kpi/
│   └── OverviewMetrics.tsx        # High-Information Compact Financial Metrics
├── maps/
│   └── IndiaRiskMap.tsx           # State Allocation Choropleth Intelligence Map
├── risk/
│   └── AnomalyMatrix.tsx          # Data Table with Search, Filter & Risk Badges
├── investigation/
│   └── InvestigationWorkspace.tsx # Full Drawer: WHY WAS THIS FLAGGED? + Missing Data
├── investigator/
│   └── AIInvestigatorChat.tsx     # Grounded Conversational Investigator (Structured Output)
├── alerts/
│   └── AlertCenter.tsx            # Early Warning Notification Cards
├── provenance/
│   └── DataSourcesModal.tsx       # Provenance Ledger (Allocated Limit for Honble MPs.csv)
├── model-health/
│   └── ModelHealthCard.tsx        # Isolation Forest + LOF Model Health & Credibility
└── scope/
    └── CapabilityScopeCard.tsx    # Analytical Honesty: What We Investigate vs Extensible Scope
```

---

## 4. REST API Endpoint Mapping

- `GET http://localhost:8001/api/analytics/overview` $\rightarrow$ Overview KPIs
- `GET http://localhost:8001/api/analytics/states` $\rightarrow$ State Analytics
- `GET http://localhost:8001/api/analytics/mps` $\rightarrow$ MP Directory & Filtering
- `GET http://localhost:8001/api/risk/anomalies` $\rightarrow$ ML Allocation Anomalies
- `GET http://localhost:8001/api/risk/distribution` $\rightarrow$ Risk Level Totals
- `POST http://localhost:8001/api/ai/investigate` $\rightarrow$ Grounded Query Engine
- `GET http://localhost:8001/api/demo/projects` $\rightarrow$ Isolated Demo Projects
- `GET http://localhost:8001/api/demo/fraud-graph` $\rightarrow$ Simulated Relationship Network
- `GET http://localhost:8001/api/system/data-sources` $\rightarrow$ Dataset Provenance Ledger
- `GET http://localhost:8001/api/system/model-health` $\rightarrow$ ML Validation Status

---

## 5. First 10-Second Judge Communication Strategy

1. **What is this?**: `MPLADS AI INTELLIGENCE COMMAND CENTER — MoSPI DIID`.
2. **Why build it?**: AI-powered continuous monitoring of allocation anomalies and public fund risk signals.
3. **Where is the AI?**: **AI WATCH** Hero Board showing real-time ML anomaly streams.
4. **What data is monitored?**: Official MoSPI CSV ($543$ MPs, $36$ States/UTs, $\text{₹}8,306.21\text{ Cr}$).
5. **What action can an authority take?**: Investigate Anomaly, Assign Nodal Officer, Mark Verified & Resolve.

# NovaDrive Technologies | Chief Risk Officer Decision-Support Platform

> **Executive Multi-Tier Supply Network Mapping, Forensic Evidence Audit, Threat Triage & Sourcing Strategy**  
> *Prepared for the Board Audit & Risk Committee and Chief Risk Officer Advisory.*

---

## Executive Summary & Business Case Context

NovaDrive Technologies operates a **$1.560 Billion USD** annual revenue portfolio across three commercial product platforms:

| Platform ID | Platform Name | Annual Revenue | Weekly Volume | Primary Manufacturing Footprint |
| :--- | :--- | :--- | :--- | :--- |
| **P1** | DriveCore Industrial Inverter | **$624M** | 2,000 units / wk | Harbor Works (60%), Plateau Works (40%) |
| **P2** | ChargeBridge Power Conversion | **$520M** | 1,000 units / wk | Harbor Works (30%), Coastal Works (70%) |
| **P3** | StoreLink Storage Control Cabinet | **$416M** | 800 units / wk | Plateau Works (100%) |

### The Executive Risk Mandate
Legacy supply chain scorecards evaluate suppliers through isolated financial ratios and historical on-time delivery percentages. Under these backward-looking tools, NovaDrive appeared well-hedged:
- **Aster Power Assemblies** held an acceptable risk score of 52/100.
- Power assembly component M10 was considered safely dual-sourced across **Aster (60%)** and **Boreal (40%)**.

**Forensic Supply Chain Disclosures Discovered by This Platform:**
1. **The Dual-Sourcing Illusion:** Aster Power Assemblies and Boreal Power Systems are **100% owned operating subsidiaries of CommonSpan Holdings** (`DOC-075`). Corporate distress at CommonSpan immediately threatens **$1.144B in annual revenue**.
2. **The Upstream Chokepoint Triad:**
   - **IonPeak Semiconductor (Tier-2):** Sole qualified silicon carbide die supplier feeding both Aster and Boreal ($1,560M exposed). Secondary SITE-900 is an unapproved pilot line (`DOC-077`, `DOC-078`).
   - **Jade Printed Circuits (Tier-2):** Sole qualified bare PCB substrate supplier for C10 & B10 ($1,560M exposed, `DOC-079`).
   - **Meridian Dielectrics (Tier-3):** Sole supplier of 2.8μm BOPP dielectric film for film capacitors, currently renegotiating trade debt covenants (`EV-003`).
3. **Zone Z01 Flood Plain Clustering:** Five essential facilities (**IonPeak SITE-074, Jade SITE-081, Orion SITE-116, Umber SiC SITE-158, Verdant Gases SITE-165**) are clustered in the East Delta flood basin (Zone Z01). Regional flood warning **EV-001** threatens 100% of portfolio production lines.
4. **The Alternate Qualification Lead-Time Trap:** Market alternates (e.g., Semikron Danfoss, Vincotech) require **12 to 16 weeks** of bench, dyno, and thermal testing to re-qualify, and still rely on external third-party dice.

---

## Platform Architecture & Design Standards

The platform follows a **McKinsey / BCG / Bain executive consulting aesthetic**:
- **Palette:** Deep Slate Navy (`#0A2540`), Royal Blue (`#0066CC`), Cool Grey canvas (`#F8FAFC`), and Charcoal text (`#1E293B`).
- **Typography:** Inter sans-serif font stack with crisp hierarchy and micro-uppercase KPI labels.
- **Tabs:** Minimalist underline tabs with active indicator lines.
- **Panels:** Sharp 4px white cards with 1px slate borders (`#E2E8F0`) and subtle status accents.
- **Zero Decorative Emojis:** Strict corporate tone with muted pill tags (`#FEE2E2` / `#991B1B` for Critical, `#FEF3C7` / `#92400E` for Elevated, `#ECFDF5` / `#065F46` for Stable).

---

## Core Operational Modules

1. **Executive Risk Scorecard & Evidence Audit (`modules/scorecard_view.py`, `modules/evidence_inspector.py`)**
   - Quantitative decomposition: Financial liquidity, leverage, delivery timeliness trend, and physical hazard indices.
   - Forensic evidence audit dossiers: Inspect verbatim regulatory filings, program disclosures (`DOC-001` through `DOC-084`), qualification dates, and allocation caveats.
   - Enterprise Danger Matrix: Revenue dependent ($M) vs. Composite risk score.

2. **Supply Network Architecture & Upstream Dependencies (`modules/network_view.py`)**
   - End-to-end dependency graph tracing Products -> Tier-1 -> Tier-2 -> Tier-3.
   - CommonSpan corporate ownership overlay connecting Aster and Boreal.
   - Critical chokepoint inventory table.

3. **Real-Time Event Audit Log & Threat Triage (`modules/alerts_view.py`)**
   - Live event log tracking regional weather advisories and counterparty debt negotiations.
   - Automated deduplication logic linking bulletin `EV-002` to parent `EV-001` (`WX-0923`).
   - False-positive quarantine suppressing non-production look-alikes (e.g., Delta Consumer Plastics).

4. **Supplier Qualification Directory & MCDA Engine (`modules/search_view.py`)**
   - Multi-Criteria Decision Analysis (MCDA) evaluating market alternates across 6 dimensions.
   - Dynamic weight adjustment sliders for strategic sensitivity modeling.
   - Upstream dependency verification identifying whether candidates eliminate or perpetuate die-level bottlenecks.

5. **Strategic Case Analysis & Scenario Simulation (`modules/case_study_view.py`)**
   - Executive problem architecture detailing the 4 structural vulnerabilities.
   - Interactive disruption simulator calculating buffer runway, line stoppages, and net revenue loss.
   - Actionable 30-60-90 day Chief Risk Officer decision roadmap.

---

## Running the Platform

Ensure dependencies are installed:
```bash
pip install -r requirements.txt
```

Start the Streamlit application:
```bash
python -m streamlit run app.py
```

Access the platform at:
`http://localhost:8501`

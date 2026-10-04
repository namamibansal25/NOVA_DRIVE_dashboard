"""
NovaDrive Technologies | Executive Decision-Support Platform
Multi-Tier Supply Chain Network Mapping, Forensic Evidence Inspection, Active Event Triage & Sourcing Strategy
"""

import os
import streamlit as st
import pandas as pd

from modules.data_loader import load_all_data, calculate_master_scorecard
from modules.scorecard_view import render_scorecard_view
from modules.evidence_inspector import render_evidence_inspector
from modules.network_view import render_network_view
from modules.alerts_view import render_alerts_view
from modules.search_view import render_alternate_search
from modules.case_study_view import render_case_study_view

# Page Configuration
st.set_page_config(
    page_title="NovaDrive Technologies | CRO Risk Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Google Fonts reliably via HTML Link tags
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Load CSS Theme with resilient fallback
css_path = os.path.join(os.path.dirname(__file__), "assets", "custom.css")
if not os.path.exists(css_path):
    css_path = os.path.join(os.path.dirname(__file__), "assests", "custom.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load Operational Data Pack
try:
    (
        df_bus, df_univ, df_score_build, df_network, df_excluded,
        df_evid, df_comp, df_crit, df_events, df_flood, df_alts, df_rules
    ) = load_all_data()
    df_scorecard = calculate_master_scorecard(df_univ, df_crit, df_network, df_evid)
except Exception as e:
    st.error(f"System data initialization error: {str(e)}")
    st.stop()

# ================= SIDEBAR: EXECUTIVE COMMAND PANE =================
with st.sidebar:
    st.markdown("""
    <div style="padding-bottom: 12px;">
        <span class="pill pill-blue"><span class="pill-dot"></span> CRO COMMAND SUITE</span>
        <h2 style="margin: 8px 0 2px 0; font-size: 20px; font-weight: 800; color: #FFFFFF !important; letter-spacing: -0.02em;">
            NovaDrive CRO
        </h2>
        <div style="color: #38BDF8; font-size: 12px; font-weight: 600;">Board Risk Oversight System</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown("<div style='font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700; color: #94A3B8; margin-bottom: 8px;'>Active Portfolio Footprint</div>", unsafe_allow_html=True)
    st.markdown("""
    - <span style="color:#94A3B8;">Total Turnover:</span> <strong style="color:#38BDF8;">$1.560B / Year</strong>
    - <span style="color:#94A3B8;">P1 DriveCore Inverter:</span> <strong style="color:#FFFFFF;">$624M</strong> (Harbor & Plateau)
    - <span style="color:#94A3B8;">P2 ChargeBridge Power:</span> <strong style="color:#FFFFFF;">$520M</strong> (Harbor & Coastal)
    - <span style="color:#94A3B8;">P3 StoreLink Storage:</span> <strong style="color:#FFFFFF;">$416M</strong> (Plateau Works)
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown("<div style='font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700; color: #94A3B8; margin-bottom: 8px;'>Regulatory & Contract Dossier</div>", unsafe_allow_html=True)
    quick_doc = st.text_input("Lookup Filing / Contract ID:", placeholder="e.g. DOC-001, DOC-075, EV-001").strip().upper()
    if quick_doc:
        doc_hit = df_evid[df_evid["Evidence ID"] == quick_doc]
        if not doc_hit.empty:
            st.markdown(f"<span class='pill pill-green' style='margin-bottom: 6px;'><span class='pill-dot'></span> Verified Record: {quick_doc}</span>", unsafe_allow_html=True)
            st.caption(f"**Parties:** {doc_hit.iloc[0].get('Title / Parties', '')}")
            st.caption(f"**Filing Date:** {doc_hit.iloc[0].get('Evidence Date', '')}")
            st.caption(f"**Extract:** {doc_hit.iloc[0].get('Evidence Detail', '')[:140]}...")
        else:
            st.markdown(f"<span class='pill pill-gray'>No record matching {quick_doc}</span>", unsafe_allow_html=True)

    st.divider()
    st.markdown("<div style='font-size: 11px; color: #64748B; line-height: 1.45;'>Data Provenance: Clean Research Data Pack v2.0<br>Strict Confidential — Board Audit & Risk Committee</div>", unsafe_allow_html=True)

# ================= LIVELY EXECUTIVE HERO COMMAND BANNER =================
st.markdown("""
<div class="executive-hero">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px;">
        <div>
            <div class="hero-kicker">
                <span class="pill-dot" style="background: #38BDF8; box-shadow: 0 0 8px #38BDF8;"></span>
                Enterprise Risk Management & Supply Chain Resilience
            </div>
            <h1 class="hero-title">
                NovaDrive Technologies
                <span class="hero-title-sub">| Chief Risk Officer Decision Suite</span>
            </h1>
            <p class="hero-desc">
                Forensic multi-tier supply chain reconstruction, primary regulatory disclosures audit, real-time threat triage, and alternate supplier qualification.
            </p>
        </div>
        <div style="text-align: right; min-width: 220px;">
            <span class="pill pill-red" style="font-size: 12px; padding: 5px 14px;"><span class="pill-dot"></span> Active Alert: Zone Z01 Basin</span>
            <div style="color: #CBD5E1; font-size: 12px; font-weight: 700; margin-top: 8px;">
                Classification: Strict Confidential
            </div>
            <div style="color: #94A3B8; font-size: 11.5px; margin-top: 2px;">
                Governance: Board Audit & Risk Committee
            </div>
        </div>
    </div>
</div>

<div class="crisis-flash">
    <div class="crisis-flash-title">
        <span class="pill-dot" style="background: #E11D48; box-shadow: 0 0 6px #E11D48;"></span>
        CRISIS EXECUTIVE SUMMARY: The Dual-Sourcing Fiction Disclosed
    </div>
    <div class="crisis-flash-body">
        <strong>Surface dual-sourcing is an illusion.</strong> Tier-1 suppliers Aster Power (60%) and Boreal Power (40%) are both 100% owned subsidiaries of CommonSpan Holdings (<code>DOC-075</code>). Sub-tier power dies (IonPeak, $1.560B reach) and bare PCBs (Jade, $1.560B reach) sit in the Zone Z01 flood basin with zero qualified alternates. <strong>100% of NovaDrive annual revenue is exposed.</strong>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= LIVELY EXECUTIVE KPI TILES (No Ellipses / Zero Truncation) =================
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown("""
    <div class="kpi-tile kpi-tile-blue">
        <div class="kpi-label">Portfolio Revenue Base</div>
        <div class="kpi-value">$1.560B</div>
        <div class="kpi-subtext"><span style="color: #0066CC; font-weight: 700;">100% Active Turnover</span> across Platforms P1-P3</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown("""
    <div class="kpi-tile kpi-tile-red">
        <div class="kpi-label">Critical Upstream Chokepoints</div>
        <div class="kpi-value" style="color: #E11D48;">3 Core Nodes</div>
        <div class="kpi-subtext"><span style="color: #E11D48; font-weight: 700;">IonPeak, Jade, Meridian</span> (Zero Backup)</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown("""
    <div class="kpi-tile kpi-tile-amber">
        <div class="kpi-label">Zone Z01 Flood Exposure</div>
        <div class="kpi-value" style="color: #D97706;">5 Facilities</div>
        <div class="kpi-subtext"><span style="color: #D97706; font-weight: 700;">Active Advisory EV-001</span> (East Delta Basin)</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown("""
    <div class="kpi-tile kpi-tile-green">
        <div class="kpi-label">Re-qualification Runway</div>
        <div class="kpi-value" style="color: #059669;">12 - 16 Wks</div>
        <div class="kpi-subtext"><span style="color: #059669; font-weight: 700;">PPAP Dyno Sprint</span> (Automotive Grade)</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)

# ================= EXECUTIVE NAVIGATION TABS =================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Executive Risk Roster",
    "Multi-Tier Network Flow",
    "Threat Triage & Event Log",
    "Alternate Qualification",
    "Disruption War Room"
])

with tab1:
    render_scorecard_view(df_scorecard, df_evid, df_excluded, df_flood, df_crit)

with tab2:
    render_network_view(df_network, df_scorecard, df_crit, df_bus, df_evid)

with tab3:
    render_alerts_view(df_events, df_flood, df_excluded, df_scorecard, df_evid)

with tab4:
    render_alternate_search(df_alts, df_comp, df_rules)

with tab5:
    render_case_study_view(df_bus, df_scorecard, df_crit, df_flood, df_alts)

# ================= EXECUTIVE FOOTER =================
st.markdown("""
<div style="margin-top: 36px; border-top: 1px solid #CBD5E1; padding-top: 16px; display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: #64748B;">
    <div>NovaDrive Technologies Decision Support Platform | Grounded in Verified Regulatory Filings, Program Awards & Shipping Records</div>
    <div>Strict Confidential — For Internal Governance & Audit Committee Use Only</div>
</div>
""", unsafe_allow_html=True)
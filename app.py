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
    page_title="NovaDrive CRO Risk Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# ================= SIDEBAR NAVIGATION & CONTEXT =================
with st.sidebar:
    st.markdown("""
    <div style="padding-bottom: 8px;">
        <span class="pill pill-blue"><span class="pill-dot"></span> NovaDrive CRO</span>
        <h2 style="margin: 6px 0 2px 0; font-size: 16px; font-weight: 700; color: #FFFFFF; letter-spacing: -0.01em;">
            Risk Intelligence
        </h2>
        <div style="color: #94A3B8; font-size: 11px;">Executive Decision Support System</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown("<div style='font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; color: #94A3B8; margin-bottom: 8px;'>Portfolio Revenue Footprint</div>", unsafe_allow_html=True)
    st.markdown("""
    - **Total Active Revenue:** **$1.560B**
    - **P1 DriveCore Inverter:** $624M (Harbor & Plateau)
    - **P2 ChargeBridge Power:** $520M (Harbor & Coastal)
    - **P3 StoreLink Storage:** $416M (Plateau Works)
    """)
    st.divider()

    st.markdown("<div style='font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; color: #94A3B8; margin-bottom: 8px;'>Document Dossier Lookup</div>", unsafe_allow_html=True)
    quick_doc = st.text_input("Enter Document Reference ID:", placeholder="e.g., DOC-001, DOC-075").strip().upper()
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
    st.markdown("<div style='font-size: 11px; color: #64748B;'>Data Provenance: Clean Research Data Pack v2.0<br>Strict Confidential — Board Audit & Risk Committee</div>", unsafe_allow_html=True)

# ================= EXECUTIVE MASTHEAD =================
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: flex-end; padding-bottom: 12px; margin-bottom: 14px; border-bottom: 1px solid #E2E8F0;">
    <div>
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
            <span class="pill pill-blue"><span class="pill-dot"></span> Board Audit & Risk Committee</span>
            <span style="color: #CBD5E1;">|</span>
            <span style="color: #64748B; font-size: 12px; font-weight: 500;">Enterprise Risk Advisory</span>
        </div>
        <h1 style="margin: 0; font-size: 22px; font-weight: 700; color: #0A2540; letter-spacing: -0.025em;">
            NovaDrive Technologies <span style="font-weight: 400; color: #64748B;">| Chief Risk Officer Decision-Support Platform</span>
        </h1>
        <p style="margin: 3px 0 0 0; color: #64748B; font-size: 12.5px;">
            Evidence-based supply chain mapping, multi-tier chokepoint diagnostics, real-time threat triage, and alternate qualification.
        </p>
    </div>
    <div style="text-align: right;">
        <span class="pill pill-red"><span class="pill-dot"></span> Active Alert: Zone Z01 Basin</span>
        <div style="color: #94A3B8; font-size: 11px; margin-top: 4px;">Classification: Strict Confidential</div>
    </div>
</div>

<div class="tldr-box">
    <span class="tldr-tag">CRISIS TL;DR</span>
    <strong>Surface dual-sourcing is an illusion.</strong> Aster (60%) and Boreal (40%) are both 100% owned subsidiaries of CommonSpan Holdings (<code>DOC-075</code>). Sub-tier dies (IonPeak, $1.56B) and bare PCBs (Jade, $1.56B) sit in flood zone Z01 with zero qualified backups. <strong>100% of NovaDrive annual revenue is exposed.</strong>
</div>
""", unsafe_allow_html=True)

# Executive KPI Ribbon (Crisp 4 metrics with breathing room)
k1, k2, k3, k4 = st.columns(4)
k1.metric("Portfolio Revenue Base", "$1.560B", "100% Portfolio (P1-P3)")
k2.metric("Critical Upstream Chokepoints", "3 Core Nodes", "IonPeak, Jade, Meridian")
k3.metric("Zone Z01 Flood Exposure", "5 Key Facilities", "Active Advisory (EV-001)", delta_color="inverse")
k4.metric("Re-qualification Runway", "12 - 16 Weeks", "Active Sprint Required", delta_color="off")

st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

# ================= EXECUTIVE NAVIGATION TABS =================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Executive Risk Roster",
    "Multi-Tier Architecture",
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
<div style="margin-top: 24px; border-top: 1px solid #E2E8F0; padding-top: 12px; display: flex; justify-content: space-between; align-items: center; font-size: 11px; color: #94A3B8;">
    <div>NovaDrive Technologies Decision Support Platform | Grounded in Verified Regulatory Filings, Program Awards & Shipping Records</div>
    <div>Confidential — For Internal Governance Use Only</div>
</div>
""", unsafe_allow_html=True)
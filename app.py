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
    <div style="background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.25); padding: 12px 14px; border-radius: 10px; margin-bottom: 14px;">
        <span style="background: rgba(56, 189, 248, 0.2); color: #38BDF8; padding: 2px 8px; border-radius: 12px; font-size: 10.5px; font-weight: 800; letter-spacing: 0.06em; text-transform: uppercase;">
            ● CRO COMMAND SUITE
        </span>
        <h2 style="margin: 6px 0 2px 0; font-size: 19px; font-weight: 800; color: #FFFFFF !important; letter-spacing: -0.02em;">
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
            st.markdown(f"<div style='background: rgba(5, 150, 105, 0.2); border: 1px solid #10B981; color: #A7F3D0; padding: 6px 10px; border-radius: 6px; font-size: 12px; font-weight: 700; margin-bottom: 6px;'>Verified Record: {quick_doc}</div>", unsafe_allow_html=True)
            st.caption(f"**Parties:** {doc_hit.iloc[0].get('Title / Parties', '')}")
            st.caption(f"**Filing Date:** {doc_hit.iloc[0].get('Evidence Date', '')}")
            st.caption(f"**Extract:** {doc_hit.iloc[0].get('Evidence Detail', '')[:140]}...")
        else:
            st.markdown(f"<div style='color: #94A3B8; font-size: 12px;'>No record matching {quick_doc}</div>", unsafe_allow_html=True)

    st.divider()
    st.markdown("<div style='font-size: 11px; color: #64748B; line-height: 1.45;'>Data Provenance: Clean Research Data Pack v2.0<br>Strict Confidential — Board Audit & Risk Committee</div>", unsafe_allow_html=True)

# ================= LIVELY EXECUTIVE HERO COMMAND BANNER (Bulletproof Inline Gradient) =================
st.markdown("""
<div style="background: linear-gradient(135deg, #0A192F 0%, #112240 50%, #081B2E 100%); 
            border: 1px solid #1E3A5F; border-radius: 14px; padding: 24px 28px; 
            margin-bottom: 20px; box-shadow: 0 8px 24px rgba(10, 25, 47, 0.2); color: #FFFFFF;">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px;">
        <div style="flex: 1; min-width: 300px;">
            <div style="display: inline-flex; align-items: center; gap: 8px; font-size: 11.5px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; color: #38BDF8; background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.3); padding: 4px 12px; border-radius: 20px; margin-bottom: 10px;">
                <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #38BDF8; box-shadow: 0 0 8px #38BDF8;"></span>
                Enterprise Risk Management & Supply Chain Resilience
            </div>
            <h1 style="font-size: 32px !important; font-weight: 800 !important; color: #FFFFFF !important; letter-spacing: -0.03em; margin: 0 0 6px 0; line-height: 1.2;">
                NovaDrive Technologies
                <span style="font-weight: 400; color: #94A3B8; font-size: 24px;">| Chief Risk Officer Decision Suite</span>
            </h1>
            <p style="font-size: 13.5px; color: #CBD5E1; margin: 0; line-height: 1.55; max-width: 880px;">
                Forensic multi-tier supply chain reconstruction, primary regulatory disclosures audit, real-time threat triage, and alternate supplier qualification.
            </p>
        </div>
        <div style="text-align: right; min-width: 200px; background: rgba(255, 255, 255, 0.05); padding: 12px 16px; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.1);">
            <div style="display: inline-block; background: #FFE4E6; color: #9F1239; font-size: 11.5px; font-weight: 700; padding: 4px 10px; border-radius: 14px; text-transform: uppercase;">
                <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #E11D48; margin-right: 4px;"></span>
                Active Alert: Zone Z01 Basin
            </div>
            <div style="color: #E2E8F0; font-size: 12px; font-weight: 700; margin-top: 6px;">
                Classification: Strict Confidential
            </div>
            <div style="color: #94A3B8; font-size: 11px; margin-top: 2px;">
                Governance: Board Audit & Risk Committee
            </div>
        </div>
    </div>
</div>

<div style="background: #FFF1F2; border: 1px solid #FECDD3; border-left: 6px solid #E11D48; border-radius: 10px; padding: 16px 20px; margin-bottom: 22px; box-shadow: 0 2px 8px rgba(225, 29, 72, 0.06);">
    <div style="display: flex; align-items: center; gap: 8px; font-size: 12.5px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em; color: #9F1239; margin-bottom: 6px;">
        <span style="display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #E11D48; box-shadow: 0 0 6px #E11D48;"></span>
        CRISIS EXECUTIVE SUMMARY: The Dual-Sourcing Fiction Disclosed
    </div>
    <div style="font-size: 13.5px; color: #1E293B; line-height: 1.55;">
        <strong>Surface dual-sourcing is an illusion.</strong> Tier-1 suppliers Aster Power (60%) and Boreal Power (40%) are both 100% owned subsidiaries of CommonSpan Holdings (<code>DOC-075</code>). Sub-tier power dies (IonPeak, $1.560B reach) and bare PCBs (Jade, $1.560B reach) sit in the Zone Z01 flood basin with zero qualified alternates. <strong>100% of NovaDrive annual revenue is exposed.</strong>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= LIVELY EXECUTIVE KPI TILES (No Ellipses / Zero Truncation) =================
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-top: 4px solid #0066CC; border-radius: 12px; padding: 16px 18px; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05); height: 100%;">
        <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; color: #64748B;">Portfolio Revenue Base</div>
        <div style="font-size: 26px; font-weight: 800; color: #0A2540; line-height: 1.1; margin: 6px 0 6px 0;">$1.560B</div>
        <div style="font-size: 12px; font-weight: 600; color: #0066CC;">100% Active Turnover (P1-P3)</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-top: 4px solid #E11D48; border-radius: 12px; padding: 16px 18px; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05); height: 100%;">
        <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; color: #64748B;">Critical Upstream Chokepoints</div>
        <div style="font-size: 26px; font-weight: 800; color: #E11D48; line-height: 1.1; margin: 6px 0 6px 0;">3 Core Nodes</div>
        <div style="font-size: 12px; font-weight: 600; color: #E11D48;">IonPeak, Jade, Meridian (Zero Backup)</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-top: 4px solid #D97706; border-radius: 12px; padding: 16px 18px; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05); height: 100%;">
        <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; color: #64748B;">Zone Z01 Flood Exposure</div>
        <div style="font-size: 26px; font-weight: 800; color: #D97706; line-height: 1.1; margin: 6px 0 6px 0;">5 Facilities</div>
        <div style="font-size: 12px; font-weight: 600; color: #D97706;">Active Advisory EV-001 (East Delta)</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-top: 4px solid #059669; border-radius: 12px; padding: 16px 18px; box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05); height: 100%;">
        <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; color: #64748B;">Re-qualification Runway</div>
        <div style="font-size: 26px; font-weight: 800; color: #059669; line-height: 1.1; margin: 6px 0 6px 0;">12 - 16 Wks</div>
        <div style="font-size: 12px; font-weight: 600; color: #059669;">PPAP Dyno Sprint (Automotive Grade)</div>
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
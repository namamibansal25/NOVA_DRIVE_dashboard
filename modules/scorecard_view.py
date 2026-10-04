"""
NovaDrive Technologies | Executive Scorecard & Evidence Audit Module
Action-oriented CRO supplier scorecard, danger matrix, and forensic evidence launcher.
"""

import streamlit as st
import pandas as pd
try:
    import plotly.express as px
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

from modules.evidence_inspector import render_evidence_inspector

def render_scorecard_view(df_scorecard, df_evid, df_excluded=None, df_flood=None, df_crit=None):
    """
    Renders an uncluttered, action-oriented supplier risk scorecard and forensic audit inspector.
    """
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
        <div>
            <h3 style="margin: 0; font-size: 16px; font-weight: 600; color: #0A2540;">Executive Counterparty Screening</h3>
            <p style="margin: 2px 0 0 0; color: #64748B; font-size: 12.5px;">
                Identify high-risk bottlenecks across liquidity, operational delivery, and geographic concentration.
            </p>
        </div>
        <div>
            <span class="pill pill-red"><span class="pill-dot"></span> 3 Critical Chokepoints Identified</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Clean Filter Bar (Minimalist 3 columns)
    f_c1, f_c2, f_c3 = st.columns([1, 1, 2])
    role_options = ["All Tiers", "Tier 1", "Tier 2", "Tier 3"]
    selected_role = f_c1.selectbox("Filter Tier:", role_options, index=0)
    
    band_options = ["All Risk Levels", "CRITICAL (>=75)", "HIGH (60-74)", "MEDIUM (40-59)", "LOW (<40)"]
    selected_band = f_c2.selectbox("Risk Level:", band_options, index=0)
    
    search_query = f_c3.text_input("Quick Search Counterparty or Node:", placeholder="e.g., IonPeak, Jade, Meridian, CommonSpan").strip().lower()

    # Filter logic
    filtered_df = df_scorecard.copy()
    if selected_role != "All Tiers":
        filtered_df = filtered_df[filtered_df["Network role"].str.contains(selected_role, na=False)]
    if selected_band != "All Risk Levels":
        raw_band = selected_band.split()[0]
        filtered_df = filtered_df[filtered_df["Risk Category"] == raw_band]

    if search_query:
        mask = (
            filtered_df["Legal Name"].astype(str).str.lower().str.contains(search_query) |
            filtered_df["Entity ID"].astype(str).str.lower().str.contains(search_query) |
            filtered_df["Components fed"].astype(str).str.lower().str.contains(search_query) |
            filtered_df["Chokepoint Status"].astype(str).str.lower().str.contains(search_query)
        )
        filtered_df = filtered_df[mask]

    # TOP 4 CRITICAL EXPOSURE TILES (Action-Oriented Cards instead of table overwhelm)
    st.markdown("<div style='font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #64748B; margin: 12px 0 8px 0;'>Critical Threat Roster — Immediate Board Priority</div>", unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("""
        <div class="action-card-critical">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <span class="pill pill-red"><span class="pill-dot"></span> Sole Source Die Maker</span>
                    <h4 style="margin: 4px 0 0 0; font-size: 15px; color: #0A2540;">IonPeak Semiconductor (ORG-439)</h4>
                    <div style="font-size: 11.5px; color: #64748B;">Tier-2 | Feeds M10, M20 Power Assemblies | SITE-074 in Zone Z01</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 18px; font-weight: 700; color: #991B1B;">$1,560M</div>
                    <div style="font-size: 10px; color: #64748B;">100% Portfolio Reach</div>
                </div>
            </div>
            <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid #FEE2E2; font-size: 12px; color: #334155;">
                <strong>Verdict:</strong> 100% of NovaDrive dies rely on single facility in flood plain. Secondary SITE-900 is an unapproved pilot line.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="action-card-warning">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <span class="pill pill-amber"><span class="pill-dot"></span> Debt Covenant Distress</span>
                    <h4 style="margin: 4px 0 0 0; font-size: 15px; color: #0A2540;">Meridian Dielectrics (ORG-454)</h4>
                    <div style="font-size: 11.5px; color: #64748B;">Tier-3 | Feeds DC-Link Film Capacitors | Event EV-003</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 18px; font-weight: 700; color: #B45309;">$624M</div>
                    <div style="font-size: 10px; color: #64748B;">P1 Inverter Reach</div>
                </div>
            </div>
            <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid #FEF3C7; font-size: 12px; color: #334155;">
                <strong>Verdict:</strong> Sole supplier of 2.8μm BOPP dielectric film. Facing delayed trade payments and covenant renegotiation.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_c2:
        st.markdown("""
        <div class="action-card-critical">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <span class="pill pill-red"><span class="pill-dot"></span> Sole PCB Substrate</span>
                    <h4 style="margin: 4px 0 0 0; font-size: 15px; color: #0A2540;">Jade Printed Circuits (ORG-453)</h4>
                    <div style="font-size: 11.5px; color: #64748B;">Tier-2 | Feeds C10 Control & B10 Power Boards | SITE-081 in Zone Z01</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 18px; font-weight: 700; color: #991B1B;">$1,560M</div>
                    <div style="font-size: 10px; color: #64748B;">100% Portfolio Reach</div>
                </div>
            </div>
            <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid #FEE2E2; font-size: 12px; color: #334155;">
                <strong>Verdict:</strong> Exclusive high-density PCB fabricator. Zero secondary qualified bare-board source in network.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="action-card-warning">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <span class="pill pill-amber"><span class="pill-dot"></span> Shared Parent Trap</span>
                    <h4 style="margin: 4px 0 0 0; font-size: 15px; color: #0A2540;">Aster Power & Boreal Power (CommonSpan)</h4>
                    <div style="font-size: 11.5px; color: #64748B;">Tier-1 Direct Assemblers | Contract 60/40 Split | Filing DOC-075</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 18px; font-weight: 700; color: #B45309;">$1,144M</div>
                    <div style="font-size: 10px; color: #64748B;">P1 & P2 Inverter Reach</div>
                </div>
            </div>
            <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid #FEF3C7; font-size: 12px; color: #334155;">
                <strong>Verdict:</strong> Purported dual-sourcing hedge is fictitious. Both are wholly owned subsidiaries of CommonSpan Holdings.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Expandable Full Roster Table (Progressive Disclosure: Clean, Not Cluttered)
    with st.expander(f"View Full Supplier Screening Table ({len(filtered_df)} Entities)", expanded=False):
        display_cols = [
            "Entity ID", "Legal Name", "Network role", "Revenue dependent (USD m)",
            "Supplier Risk Score", "Risk Category", "Facility Zone", "Chokepoint Status"
        ]
        avail_cols = [c for c in display_cols if c in filtered_df.columns]
        st.dataframe(filtered_df[avail_cols], use_container_width=True, height=240)

    st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)

    # FORENSIC EVIDENCE AUDIT SECTION
    st.markdown("""
    <div style="border-top: 1px solid #E2E8F0; padding-top: 14px; margin-bottom: 10px;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <h4 style="margin: 0; font-size: 15px; font-weight: 600; color: #0A2540;">Forensic Evidence Audit & Disclosure Dossier</h4>
                <div style="font-size: 12px; color: #64748B; margin-top: 2px;">Inspect verified regulatory filings, test certificates, and contract planning caveats.</div>
            </div>
            <div>
                <span class="pill pill-blue"><span class="pill-dot"></span> Traceability Verified</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    entity_list = filtered_df["Entity ID"].tolist()
    default_entity = "ORG-439" if "ORG-439" in entity_list else (entity_list[0] if entity_list else None)
    
    selected_entity = st.selectbox(
        "Select Counterparty Node to Audit:",
        entity_list,
        index=entity_list.index(default_entity) if default_entity in entity_list else 0
    )

    if selected_entity:
        render_evidence_inspector(selected_entity, df_scorecard, df_evid, df_excluded, df_flood, df_crit)

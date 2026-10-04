"""
NovaDrive Technologies | Executive Scorecard & Evidence Audit Module
Action-oriented CRO supplier scorecard, danger matrix, and forensic evidence launcher.
"""

import streamlit as st
import pandas as pd
try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

from modules.evidence_inspector import render_evidence_inspector

def render_scorecard_view(df_scorecard, df_evid, df_excluded=None, df_flood=None, df_crit=None):
    """
    Renders an executive-grade supplier risk scorecard, forensic risk gap chart,
    and primary evidence dossier inspector.
    """
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <div>
            <h3 style="margin: 0; font-size: 20px; font-weight: 800; color: #0A2540;">Executive Counterparty Risk Roster & Blindspot Diagnostic</h3>
            <p style="margin: 3px 0 0 0; color: #64748B; font-size: 13.5px;">
                Forensic multi-tier risk scoring exposing the gap between surface compliance metrics and intrinsic operational reality.
            </p>
        </div>
        <div>
            <span class="pill pill-red" style="font-size: 12px; padding: 5px 12px;"><span class="pill-dot"></span> 3 Critical Chokepoints Identified</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Clean Filter Bar
    f_c1, f_c2, f_c3 = st.columns([1, 1, 2])
    role_options = ["All Tiers", "Tier 1", "Tier 2", "Tier 3"]
    selected_role = f_c1.selectbox("Filter Tier:", role_options, index=0)
    
    band_options = ["All Risk Levels", "CRITICAL (>=75)", "HIGH (60-74)", "MEDIUM (40-59)", "LOW (<40)"]
    selected_band = f_c2.selectbox("Risk Level:", band_options, index=0)
    
    search_query = f_c3.text_input("Quick Search Counterparty or Node:", placeholder="e.g. IonPeak, Jade, Meridian, CommonSpan").strip().lower()

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

    # EXECUTIVE INFOGRAPHIC: Reported vs. Intrinsic Risk Gap (The Blindspot Chart)
    if HAS_PLOTLY:
        gap_entities = [
            {"name": "IonPeak Semi (T2)", "rep": 65, "intr": 88, "tier": "Tier 2", "cause": "Sole SiC Die Source in Z01 Basin ($1,560M Reach)"},
            {"name": "Jade Circuits (T2)", "rep": 62, "intr": 86, "tier": "Tier 2", "cause": "Sole Bare PCB Fabricator in Z01 Basin ($1,560M Reach)"},
            {"name": "Meridian Diel. (T3)", "rep": 58, "intr": 84, "tier": "Tier 3", "cause": "Sole BOPP Film Maker under Debt Default (EV-003)"},
            {"name": "Aster Power (T1)", "rep": 52, "intr": 82, "tier": "Tier 1", "cause": "CommonSpan 100% Owned + 100% IonPeak Die Dependent"},
            {"name": "Boreal Power (T1)", "rep": 48, "intr": 82, "tier": "Tier 1", "cause": "CommonSpan 100% Owned + 100% IonPeak Die Dependent"},
            {"name": "Umber SiC (T3)", "rep": 55, "intr": 78, "tier": "Tier 3", "cause": "Sole Wafer Substrate in Z01 Flood Basin"},
            {"name": "Cobalt Control (T1)", "rep": 42, "intr": 68, "tier": "Tier 1", "cause": "100% Dependent on Jade Printed for Bare PCBs"},
            {"name": "Grove Energy (T1)", "rep": 40, "intr": 66, "tier": "Tier 1", "cause": "100% Dependent on Jade Printed for Bare PCBs"}
        ]
        
        y_labels = [g["name"] for g in gap_entities][::-1]
        rep_scores = [g["rep"] for g in gap_entities][::-1]
        intr_scores = [g["intr"] for g in gap_entities][::-1]
        causes = [g["cause"] for g in gap_entities][::-1]

        fig_gap = go.Figure()

        # Shaded connector lines (Blindspot gap)
        for i in range(len(y_labels)):
            fig_gap.add_trace(go.Scatter(
                x=[rep_scores[i], intr_scores[i]],
                y=[y_labels[i], y_labels[i]],
                mode="lines",
                line=dict(color="rgba(225, 29, 72, 0.45)", width=7),
                hoverinfo="skip",
                showlegend=False
            ))

        # Reported Score Markers
        fig_gap.add_trace(go.Scatter(
            x=rep_scores,
            y=y_labels,
            mode="markers+text",
            marker=dict(size=13, color="#64748B", line=dict(color="#FFFFFF", width=2)),
            name="Surface Reported Score (Legacy)",
            text=[f"{s}" for s in rep_scores],
            textposition="middle left",
            textfont=dict(size=11, family="Plus Jakarta Sans", color="#64748B", weight="bold"),
            hovertemplate="<b>%{y}</b><br>Legacy Reported Score: %{x}/100<extra></extra>"
        ))

        # Intrinsic Score Markers
        fig_gap.add_trace(go.Scatter(
            x=intr_scores,
            y=y_labels,
            mode="markers+text",
            marker=dict(size=15, color="#E11D48", line=dict(color="#FFFFFF", width=2.5)),
            name="Intrinsic Multi-Tier Risk (Forensic)",
            text=[f"{s}" for s in intr_scores],
            textposition="middle right",
            textfont=dict(size=12, family="Plus Jakarta Sans", color="#E11D48", weight="bold"),
            hovertemplate="<b>%{y}</b><br>Intrinsic Risk Score: %{x}/100<br>Driver: %{customdata}<extra></extra>",
            customdata=causes
        ))

        fig_gap.update_layout(
            title=dict(
                text="<b>Diagnostic: The 'Risk Blindspot Gap' (Legacy Reported Score vs. Forensic Multi-Tier Reality)</b>",
                font=dict(size=14, color="#0A2540", family="Plus Jakarta Sans, sans-serif")
            ),
            xaxis=dict(
                title="Risk Severity Score (0 - 100 scale; >75 is Critical)",
                range=[25, 102],
                showgrid=True,
                gridcolor="#E2E8F0",
                zeroline=False
            ),
            yaxis=dict(showgrid=False),
            height=340,
            margin=dict(l=15, r=15, t=45, b=25),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            font=dict(family="Plus Jakarta Sans, sans-serif", size=11, color="#334155")
        )

        st.plotly_chart(fig_gap, use_container_width=True)

    # TOP 4 CRITICAL EXPOSURE TILES (Lively, High-Contrast Action Cards)
    st.markdown("<div style='font-size: 13px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #64748B; margin: 20px 0 12px 0;'>Critical Threat Roster — Immediate Board Priority</div>", unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("""
        <div class="action-card-critical" style="background: #FFF8F8; border: 1px solid #FECDD3; border-left: 6px solid #E11D48; border-radius: 12px; padding: 20px 24px; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <span class="pill pill-red"><span class="pill-dot"></span> Sole Source Die Maker</span>
                    <h4 style="margin: 6px 0 0 0; font-size: 16px; font-weight: 800; color: #0A2540;">IonPeak Semiconductor (ORG-439)</h4>
                    <div style="font-size: 12.5px; color: #64748B; margin-top: 3px;">Tier-2 | Feeds M10, M20 Power Assemblies | SITE-074 in Zone Z01</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 22px; font-weight: 800; color: #E11D48;">$1,560M</div>
                    <div style="font-size: 11px; font-weight: 700; color: #64748B;">100% Portfolio Reach</div>
                </div>
            </div>
            <div style="margin-top: 12px; padding-top: 10px; border-top: 1px solid #FECDD3; font-size: 13px; color: #1E293B; line-height: 1.55;">
                <strong style="color: #9F1239;">Verdict:</strong> 100% of NovaDrive dies rely on single facility in flood plain. Secondary SITE-900 is an unapproved pilot line.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="action-card-warning" style="background: #FFFDF7; border: 1px solid #FDE68A; border-left: 6px solid #D97706; border-radius: 12px; padding: 20px 24px; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <span class="pill pill-amber"><span class="pill-dot"></span> Debt Covenant Distress</span>
                    <h4 style="margin: 6px 0 0 0; font-size: 16px; font-weight: 800; color: #0A2540;">Meridian Dielectrics (ORG-454)</h4>
                    <div style="font-size: 12.5px; color: #64748B; margin-top: 3px;">Tier-3 | Feeds DC-Link Film Capacitors | Event EV-003</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 22px; font-weight: 800; color: #D97706;">$624M</div>
                    <div style="font-size: 11px; font-weight: 700; color: #64748B;">P1 Inverter Reach</div>
                </div>
            </div>
            <div style="margin-top: 12px; padding-top: 10px; border-top: 1px solid #FDE68A; font-size: 13px; color: #1E293B; line-height: 1.55;">
                <strong style="color: #92400E;">Verdict:</strong> Sole supplier of 2.8μm BOPP dielectric film. Facing delayed trade payments and covenant renegotiation.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_c2:
        st.markdown("""
        <div class="action-card-critical" style="background: #FFF8F8; border: 1px solid #FECDD3; border-left: 6px solid #E11D48; border-radius: 12px; padding: 20px 24px; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <span class="pill pill-red"><span class="pill-dot"></span> Sole PCB Substrate</span>
                    <h4 style="margin: 6px 0 0 0; font-size: 16px; font-weight: 800; color: #0A2540;">Jade Printed Circuits (ORG-453)</h4>
                    <div style="font-size: 12.5px; color: #64748B; margin-top: 3px;">Tier-2 | Feeds C10 Control & B10 Power Boards | SITE-081 in Zone Z01</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 22px; font-weight: 800; color: #E11D48;">$1,560M</div>
                    <div style="font-size: 11px; font-weight: 700; color: #64748B;">100% Portfolio Reach</div>
                </div>
            </div>
            <div style="margin-top: 12px; padding-top: 10px; border-top: 1px solid #FECDD3; font-size: 13px; color: #1E293B; line-height: 1.55;">
                <strong style="color: #9F1239;">Verdict:</strong> Exclusive high-density PCB fabricator. Zero secondary qualified bare-board source in network.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="action-card-warning" style="background: #FFFDF7; border: 1px solid #FDE68A; border-left: 6px solid #D97706; border-radius: 12px; padding: 20px 24px; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <span class="pill pill-amber"><span class="pill-dot"></span> Shared Parent Trap</span>
                    <h4 style="margin: 6px 0 0 0; font-size: 16px; font-weight: 800; color: #0A2540;">Aster Power & Boreal Power (CommonSpan)</h4>
                    <div style="font-size: 12.5px; color: #64748B; margin-top: 3px;">Tier-1 Direct Assemblers | Contract 60/40 Split | Filing DOC-075</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 22px; font-weight: 800; color: #D97706;">$1,144M</div>
                    <div style="font-size: 11px; font-weight: 700; color: #64748B;">P1 & P2 Inverter Reach</div>
                </div>
            </div>
            <div style="margin-top: 12px; padding-top: 10px; border-top: 1px solid #FDE68A; font-size: 13px; color: #1E293B; line-height: 1.55;">
                <strong style="color: #92400E;">Verdict:</strong> Purported dual-sourcing hedge is fictitious. Both are wholly owned subsidiaries of CommonSpan Holdings.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Expandable Full Roster Table (Progressive Disclosure)
    with st.expander(f"Inspect Full Supplier Screening Registry ({len(filtered_df)} Entities)", expanded=False):
        display_cols = [
            "Entity ID", "Legal Name", "Network role", "Revenue dependent (USD m)",
            "Supplier Risk Score", "Risk Category", "Facility Zone", "Chokepoint Status"
        ]
        avail_cols = [c for c in display_cols if c in filtered_df.columns]
        st.dataframe(filtered_df[avail_cols], use_container_width=True, height=240)

    st.markdown("<div style='margin-top: 24px;'></div>", unsafe_allow_html=True)

    # FORENSIC EVIDENCE AUDIT SECTION
    st.markdown("""
    <div style="border-top: 2px solid #E2E8F0; padding-top: 20px; margin-bottom: 14px;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <h4 style="margin: 0; font-size: 17px; font-weight: 800; color: #0A2540;">Forensic Evidence Audit & Disclosure Dossier</h4>
                <div style="font-size: 13px; color: #64748B; margin-top: 3px;">Inspect verified regulatory filings, test certificates, and contract planning caveats.</div>
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

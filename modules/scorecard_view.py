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
    dynamic responsive search cards, and primary evidence dossier inspector.
    """
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <div>
            <h3 style="margin: 0; font-size: 20px; font-weight: 800; color: #0A2540;">Executive Counterparty Risk Roster & Dynamic Screening</h3>
            <p style="margin: 3px 0 0 0; color: #64748B; font-size: 13.5px;">
                Forensic multi-tier risk scoring exposing the gap between surface compliance metrics and intrinsic operational reality.
            </p>
        </div>
        <div>
            <span style="background: #FFE4E6; color: #9F1239; border: 1px solid #FDA4AF; padding: 5px 12px; border-radius: 20px; font-size: 11.5px; font-weight: 700; text-transform: uppercase;">
                ● 3 Critical Chokepoints Identified
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Clean Filter Bar with Smart Search & Reset
    f_c1, f_c2, f_c3, f_c4 = st.columns([1, 1, 2, 0.6])
    role_options = ["All Tiers", "Tier 1", "Tier 2", "Tier 3"]
    selected_role = f_c1.selectbox("Filter Tier:", role_options, index=0)
    
    band_options = ["All Risk Levels", "CRITICAL (>=75)", "HIGH (60-74)", "MEDIUM (40-59)", "LOW (<40)"]
    selected_band = f_c2.selectbox("Risk Level:", band_options, index=0)
    
    search_query = f_c3.text_input("Quick Search Counterparty or Node:", placeholder="e.g. IonPeak, Jade, Meridian, CommonSpan").strip().lower()

    # Clear Filters button
    with f_c4:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        clear_clicked = st.button("Reset", help="Reset all filters to default")

    if clear_clicked:
        selected_role = "All Tiers"
        selected_band = "All Risk Levels"
        search_query = ""

    # Intelligent Filtering Logic
    filtered_df = df_scorecard.copy()
    search_override_notice = None

    if search_query:
        # Check if search query matches anything in the entire dataset
        search_mask_global = (
            df_scorecard["Legal Name"].astype(str).str.lower().str.contains(search_query) |
            df_scorecard["Entity ID"].astype(str).str.lower().str.contains(search_query) |
            df_scorecard["Components fed"].astype(str).str.lower().str.contains(search_query) |
            df_scorecard["Chokepoint Status"].astype(str).str.lower().str.contains(search_query)
        )
        global_matches = df_scorecard[search_mask_global]

        # Check with existing tier / band filters
        temp_filtered = filtered_df.copy()
        if selected_role != "All Tiers":
            temp_filtered = temp_filtered[temp_filtered["Network role"].str.contains(selected_role, na=False)]
        if selected_band != "All Risk Levels":
            raw_band = selected_band.split()[0]
            temp_filtered = temp_filtered[temp_filtered["Risk Category"] == raw_band]

        local_mask = (
            temp_filtered["Legal Name"].astype(str).str.lower().str.contains(search_query) |
            temp_filtered["Entity ID"].astype(str).str.lower().str.contains(search_query) |
            temp_filtered["Components fed"].astype(str).str.lower().str.contains(search_query) |
            temp_filtered["Chokepoint Status"].astype(str).str.lower().str.contains(search_query)
        )
        local_matches = temp_filtered[local_mask]

        if not local_matches.empty:
            filtered_df = local_matches
        elif not global_matches.empty:
            # Smart fallback: Found matches in another tier or band!
            filtered_df = global_matches
            matched_entity = global_matches.iloc[0]
            m_name = matched_entity.get("Legal Name", "")
            m_tier = matched_entity.get("Network role", "")
            m_cat = matched_entity.get("Risk Category", "")
            search_override_notice = f"Found '{m_name}' in <strong>{m_tier}</strong> ({m_cat} Risk). Showing search match across all tiers."
        else:
            filtered_df = pd.DataFrame()
    else:
        if selected_role != "All Tiers":
            filtered_df = filtered_df[filtered_df["Network role"].str.contains(selected_role, na=False)]
        if selected_band != "All Risk Levels":
            raw_band = selected_band.split()[0]
            filtered_df = filtered_df[filtered_df["Risk Category"] == raw_band]

    if search_override_notice:
        st.markdown(f"""
        <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-left: 5px solid #0066CC; border-radius: 8px; padding: 10px 14px; margin-bottom: 14px; font-size: 13px; color: #1E3A8A;">
            {search_override_notice}
        </div>
        """, unsafe_allow_html=True)

    # EXECUTIVE INFOGRAPHIC: Reported vs. Intrinsic Risk Gap (Zero-Collision Header & Legend)
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

        # External Clean Header + Legend (Guarantees ZERO Collision on any screen size)
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 10px; padding: 14px 18px 6px 18px; margin-top: 10px; margin-bottom: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div>
                    <div style="font-size: 14.5px; font-weight: 800; color: #0A2540;">
                        Diagnostic: The 'Risk Blindspot Gap' (Legacy Reported Score vs. Forensic Multi-Tier Reality)
                    </div>
                    <div style="font-size: 12px; color: #64748B;">
                        Dumbbell delta chart proving why traditional procurement metrics blindsided NovaDrive.
                    </div>
                </div>
                <div style="display: flex; gap: 14px; font-size: 11.5px; font-weight: 700;">
                    <span style="color: #64748B;">● Surface Reported Score (Legacy)</span>
                    <span style="color: #E11D48;">● Intrinsic Multi-Tier Risk (Forensic)</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        fig_gap = go.Figure()

        # Shaded connector lines (Blindspot gap)
        for i in range(len(y_labels)):
            fig_gap.add_trace(go.Scatter(
                x=[rep_scores[i], intr_scores[i]],
                y=[y_labels[i], y_labels[i]],
                mode="lines",
                line=dict(color="rgba(225, 29, 72, 0.45)", width=6),
                hoverinfo="skip",
                showlegend=False
            ))

        # Reported Score Markers
        fig_gap.add_trace(go.Scatter(
            x=rep_scores,
            y=y_labels,
            mode="markers+text",
            marker=dict(size=12, color="#64748B", line=dict(color="#FFFFFF", width=2)),
            name="Surface Reported Score (Legacy)",
            text=[f"{s}" for s in rep_scores],
            textposition="middle left",
            textfont=dict(size=11, family="Plus Jakarta Sans", color="#64748B", weight="bold"),
            hovertemplate="<b>%{y}</b><br>Legacy Reported Score: %{x}/100<extra></extra>",
            showlegend=False
        ))

        # Intrinsic Score Markers
        fig_gap.add_trace(go.Scatter(
            x=intr_scores,
            y=y_labels,
            mode="markers+text",
            marker=dict(size=14, color="#E11D48", line=dict(color="#FFFFFF", width=2)),
            name="Intrinsic Multi-Tier Risk (Forensic)",
            text=[f"{s}" for s in intr_scores],
            textposition="middle right",
            textfont=dict(size=11.5, family="Plus Jakarta Sans", color="#E11D48", weight="bold"),
            hovertemplate="<b>%{y}</b><br>Intrinsic Risk Score: %{x}/100<br>Driver: %{customdata}<extra></extra>",
            customdata=causes,
            showlegend=False
        ))

        fig_gap.update_layout(
            title=None,
            xaxis=dict(
                title="Risk Severity Score (0 - 100 scale; >75 is Critical)",
                range=[25, 102],
                showgrid=True,
                gridcolor="#E2E8F0",
                zeroline=False
            ),
            yaxis=dict(showgrid=False),
            height=280,
            margin=dict(l=15, r=15, t=10, b=25),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            font=dict(family="Plus Jakarta Sans, sans-serif", size=11, color="#334155")
        )

        st.plotly_chart(fig_gap, use_container_width=True)

    # DYNAMIC COUNTERPARTY CARDS (Responds Instantly to User Filter & Search!)
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin: 18px 0 12px 0;">
        <div style="font-size: 13.5px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.07em; color: #64748B;">
            Filtered Counterparty Dossiers ({len(filtered_df)} Entities Matching)
        </div>
        <div style="font-size: 12px; color: #64748B;">
            Showing top active risk nodes
        </div>
    </div>
    """, unsafe_allow_html=True)

    if filtered_df.empty:
        st.markdown("""
        <div style="background: #FFFBEB; border: 1px solid #FCD34D; border-left: 6px solid #D97706; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
            <h4 style="margin: 0 0 6px 0; color: #92400E; font-size: 15px; font-weight: 800;">No Suppliers Match Current Filter Criteria</h4>
            <p style="margin: 0; font-size: 13px; color: #78350F; line-height: 1.5;">
                Try selecting <strong>'All Tiers'</strong> or <strong>'All Risk Levels'</strong>, or click <strong>'Reset'</strong> to view the full 30-supplier roster.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Render cards dynamically for the top matching entities (up to 4 cards)
        cards_to_show = filtered_df.head(4)
        c_cols = st.columns(2)

        for idx, (_, row) in enumerate(cards_to_show.iterrows()):
            col = c_cols[idx % 2]
            eid = row.get("Entity ID", "")
            ename = row.get("Legal Name", "Unknown")
            role = row.get("Network role", "Supplier")
            score = row.get("Supplier Risk Score", 0)
            cat = str(row.get("Risk Category", "UNSCORED")).upper()
            rev = row.get("Revenue dependent (USD m)", 0)
            choke = str(row.get("Chokepoint Status", "Standard Node"))
            zone = row.get("Facility Zone", "N/A")
            comps = row.get("Components fed", "N/A")

            # Determine colors based on risk category
            if "CRITICAL" in cat or score >= 75:
                card_bg = "#FFF8F8"
                card_border = "#FECDD3"
                card_accent = "#E11D48"
                pill_bg = "#FFE4E6"
                pill_color = "#9F1239"
                pill_dot = "#E11D48"
                rev_color = "#E11D48"
                badge_text = "CRITICAL CHOKEPOINT"
            elif "HIGH" in cat or score >= 60:
                card_bg = "#FFFDF7"
                card_border = "#FDE68A"
                card_accent = "#D97706"
                pill_bg = "#FEF3C7"
                pill_color = "#92400E"
                pill_dot = "#D97706"
                rev_color = "#D97706"
                badge_text = "HIGH EXPOSURE"
            elif "MEDIUM" in cat or score >= 40:
                card_bg = "#F8FAFF"
                card_border = "#BAE6FD"
                card_accent = "#0066CC"
                pill_bg = "#E0F2FE"
                pill_color = "#0369A1"
                pill_dot = "#0284C7"
                rev_color = "#0066CC"
                badge_text = "MEDIUM EXPOSURE"
            else:
                card_bg = "#FAFEF9"
                card_border = "#A7F3D0"
                card_accent = "#059669"
                pill_bg = "#D1FAE5"
                pill_color = "#065F46"
                pill_dot = "#059669"
                rev_color = "#059669"
                badge_text = "MONITORED NODE"

            with col:
                st.markdown(f"""
                <div style="background: {card_bg}; border: 1px solid {card_border}; border-left: 6px solid {card_accent}; border-radius: 12px; padding: 20px 24px; margin-bottom: 16px; box-shadow: 0 2px 6px rgba(0,0,0,0.03);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <span style="background: {pill_bg}; color: {pill_color}; border: 1px solid {card_border}; padding: 3px 9px; border-radius: 16px; font-size: 11px; font-weight: 800; text-transform: uppercase;">
                                <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: {pill_dot}; margin-right: 4px;"></span>
                                {badge_text}
                            </span>
                            <h4 style="margin: 6px 0 0 0; font-size: 16px; font-weight: 800; color: #0A2540;">{ename} ({eid})</h4>
                            <div style="font-size: 12.5px; color: #64748B; margin-top: 2px;">{role} | Zone {zone} | Score: <strong>{score}/100</strong></div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 22px; font-weight: 800; color: {rev_color};">${rev}M</div>
                            <div style="font-size: 10.5px; font-weight: 700; color: #64748B;">Revenue At Risk</div>
                        </div>
                    </div>
                    <div style="margin-top: 10px; font-size: 13px; color: #1E293B; line-height: 1.5;">
                        <strong>Feed Path:</strong> {comps}
                    </div>
                    <div style="margin-top: 6px; padding-top: 6px; border-top: 1px solid {card_border}; font-size: 12px; color: #475569;">
                        <strong>Chokepoint Status:</strong> {choke}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ALWAYS-VISIBLE LIVE SUPPLIER SCREENING REGISTRY
    st.markdown(f"""
    <div style="margin-top: 14px; margin-bottom: 8px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="font-size: 14px; font-weight: 800; color: #0A2540;">
                Active Counterparty Data Registry ({len(filtered_df)} Suppliers)
            </div>
            <div style="font-size: 12px; color: #64748B;">
                Click column headers to sort
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    display_cols = [
        "Entity ID", "Legal Name", "Network role", "Revenue dependent (USD m)",
        "Supplier Risk Score", "Risk Category", "Facility Zone", "Chokepoint Status"
    ]
    avail_cols = [c for c in display_cols if c in filtered_df.columns]
    st.dataframe(filtered_df[avail_cols], use_container_width=True, height=220)

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
                <span style="background: #E0F2FE; color: #0369A1; border: 1px solid #BAE6FD; padding: 4px 10px; border-radius: 16px; font-size: 11px; font-weight: 700; text-transform: uppercase;">
                    ● Traceability Verified
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    entity_list = filtered_df["Entity ID"].tolist() if not filtered_df.empty else df_scorecard["Entity ID"].tolist()
    default_entity = "ORG-439" if "ORG-439" in entity_list else (entity_list[0] if entity_list else None)
    
    selected_entity = st.selectbox(
        "Select Counterparty Node to Audit:",
        entity_list,
        index=entity_list.index(default_entity) if default_entity in entity_list else 0
    )

    if selected_entity:
        render_evidence_inspector(selected_entity, df_scorecard, df_evid, df_excluded, df_flood, df_crit)

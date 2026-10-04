"""
NovaDrive Technologies | Supply Network Architecture Module
Multi-tier network dependency mapping, corporate ownership overlays, and chokepoint diagnostics.
"""

import streamlit as st
import pandas as pd
try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

from modules.evidence_inspector import render_evidence_inspector

def render_network_view(df_network, df_scorecard, df_crit, df_bus, df_evid):
    """
    Renders an executive-grade value-chain flow infographic, corporate ownership
    governance overlay, and chokepoint diagnostics.
    """
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <div>
            <h3 style="margin: 0; font-size: 18px; font-weight: 700; color: #0A2540;">Multi-Tier Supply Chain Architecture & Value-Chain Flow</h3>
            <p style="margin: 3px 0 0 0; color: #64748B; font-size: 13px;">
                Structural dependency mapping from finished vehicle platforms down to Tier-3 raw material suppliers.
            </p>
        </div>
        <div>
            <span class="pill pill-red"><span class="pill-dot"></span> CommonSpan Ownership Exposed</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Executive Risk Callouts (Crisp Consulting Cards)
    c_w1, c_w2 = st.columns(2)
    with c_w1:
        st.markdown("""
        <div class="action-card-critical">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <span class="pill pill-red"><span class="pill-dot"></span> Corporate Governance Illusion</span>
                    <h4 style="margin: 5px 0 0 0; font-size: 15px; font-weight: 700; color: #0A2540;">The CommonSpan Dual-Sourcing Fiction</h4>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 20px; font-weight: 800; color: #991B1B;">$1,144M</div>
                    <div style="font-size: 10.5px; font-weight: 600; color: #64748B;">P1 & P2 Exposure</div>
                </div>
            </div>
            <p style="font-size: 13px; color: #334155; margin: 8px 0 0 0; line-height: 1.55;">
                NovaDrive ostensibly dual-sources power assemblies <strong>M10 & M20</strong> across <strong>Aster Power (60%)</strong> and <strong>Boreal Power (40%)</strong>.<br>
                Regulatory disclosure <code>DOC-075</code> confirms both entities are <strong>100% owned subsidiaries of CommonSpan Holdings</strong>. Distress or debt default at the parent halts assembly across both suppliers simultaneously.
            </p>
            <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid #FEE2E2; font-size: 12px; color: #7F1D1D; font-weight: 600;">
                CRO Mandate: Require independent bank ring-fencing guarantees or qualify an un-affiliated module supplier.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c_w2:
        st.markdown("""
        <div class="action-card-warning">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <span class="pill pill-amber"><span class="pill-dot"></span> Sub-Tier Vulnerability</span>
                    <h4 style="margin: 5px 0 0 0; font-size: 15px; font-weight: 700; color: #0A2540;">The Upstream Chokepoint Triad</h4>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 20px; font-weight: 800; color: #B45309;">$1,560M</div>
                    <div style="font-size: 10.5px; font-weight: 600; color: #64748B;">100% Portfolio Reach</div>
                </div>
            </div>
            <p style="font-size: 13px; color: #334155; margin: 8px 0 0 0; line-height: 1.55;">
                <strong>IonPeak Semiconductor (Tier-2):</strong> Sole SiC die supplier ($1,560M reach, flood basin SITE-074).<br>
                <strong>Jade Printed Circuits (Tier-2):</strong> Sole bare PCB supplier for C10 & B10 ($1,560M reach).<br>
                <strong>Meridian Dielectrics (Tier-3):</strong> Sole BOPP film supplier ($624M reach, debt distress <code>EV-003</code>).
            </p>
            <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid #FEF3C7; font-size: 12px; color: #92400E; font-weight: 600;">
                CRO Mandate: Audit off-site forward buffer inventory and initiate dual-sourcing sprints.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Filter Bar
    f1, f2 = st.columns([2, 1])
    filter_prod = f1.selectbox(
        "Highlight Value Stream Path:",
        [
            "All Enterprise Value Streams ($1.560B Total)",
            "P1 DriveCore Inverter Path ($624M Revenue)",
            "P2 ChargeBridge Power Path ($520M Revenue)",
            "P3 StoreLink Storage Path ($416M Revenue)"
        ]
    )
    show_choke_only = f2.checkbox("Highlight Chokepoint Paths in Red", value=True)

    # Executive Sankey Flow Infographic
    if HAS_PLOTLY:
        # Define Sankey Nodes
        node_labels = [
            # 0-2: Platforms
            "P1 DriveCore ($624M)",
            "P2 ChargeBridge ($520M)",
            "P3 StoreLink ($416M)",
            # 3-7: Tier 1 Direct Suppliers
            "Aster Power (T1, 60% CommonSpan)",
            "Boreal Power (T1, 40% CommonSpan)",
            "Cobalt Control (T1)",
            "Grove Energy (T1)",
            "HarborSense (T1)",
            # 8-12: Tier 2 Sub-Suppliers
            "IonPeak Semi (T2 Chokepoint)",
            "Jade Circuits (T2 Chokepoint)",
            "Orion Ceramics (T2)",
            "Lumen Magnetics (T2)",
            "Delta Capacitor (T2)",
            # 13-16: Tier 3 Raw Materials
            "Umber SiC Wafers (T3)",
            "Verdant Silane Gas (T3)",
            "Yarrow Alumina (T3)",
            "Meridian BOPP Film (T3 Chokepoint)"
        ]

        # Colors for Nodes
        node_colors = [
            # Platforms (Slate Navy)
            "#0A2540", "#0A2540", "#0A2540",
            # Tier 1 (Royal Blue & CommonSpan)
            "#1E40AF", "#1E40AF", "#0284C7", "#0284C7", "#0284C7",
            # Tier 2 (Critical Red / Amber / Slate)
            "#DC2626", "#DC2626", "#D97706", "#64748B", "#D97706",
            # Tier 3
            "#DC2626", "#D97706", "#64748B", "#DC2626"
        ]

        # Links (source_idx, target_idx, value_in_millions, link_color)
        # P1 = 0, P2 = 1, P3 = 2
        # Aster = 3, Boreal = 4, Cobalt = 5, Grove = 6, Harbor = 7
        # IonPeak = 8, Jade = 9, Orion = 10, Lumen = 11, Delta = 12
        # Umber = 13, Verdant = 14, Yarrow = 15, Meridian = 16

        raw_links = [
            # P1 to T1
            (0, 3, 374, "#FECACA" if show_choke_only else "#CBD5E1"),  # P1 to Aster (60%)
            (0, 4, 250, "#FECACA" if show_choke_only else "#CBD5E1"),  # P1 to Boreal (40%)
            (0, 5, 200, "#E2E8F0"),                                     # P1 to Cobalt (Control)
            # P2 to T1
            (1, 3, 364, "#FECACA" if show_choke_only else "#CBD5E1"),  # P2 to Aster (70%)
            (1, 4, 156, "#FECACA" if show_choke_only else "#CBD5E1"),  # P2 to Boreal (30%)
            (1, 6, 180, "#E2E8F0"),                                     # P2 to Grove
            # P3 to T1
            (2, 3, 250, "#FECACA" if show_choke_only else "#CBD5E1"),  # P3 to Aster
            (2, 4, 166, "#FECACA" if show_choke_only else "#CBD5E1"),  # P3 to Boreal
            (2, 7, 120, "#E2E8F0"),                                     # P3 to HarborSense

            # T1 to T2 (The Critical Funnels)
            (3, 8, 700, "rgba(220, 38, 38, 0.45)" if show_choke_only else "#CBD5E1"),   # Aster to IonPeak (SiC dies)
            (4, 8, 444, "rgba(220, 38, 38, 0.45)" if show_choke_only else "#CBD5E1"),   # Boreal to IonPeak (SiC dies)
            (3, 10, 150, "rgba(217, 119, 6, 0.3)"),                                      # Aster to Orion
            (4, 10, 100, "rgba(217, 119, 6, 0.3)"),                                      # Boreal to Orion
            (3, 12, 180, "rgba(217, 119, 6, 0.3)"),                                      # Aster to Delta Cap
            (4, 12, 120, "rgba(217, 119, 6, 0.3)"),                                      # Boreal to Delta Cap
            (5, 9, 200, "rgba(220, 38, 38, 0.45)" if show_choke_only else "#CBD5E1"),   # Cobalt to Jade (PCBs)
            (6, 9, 180, "rgba(220, 38, 38, 0.45)" if show_choke_only else "#CBD5E1"),   # Grove to Jade (PCBs)

            # T2 to T3 (Upstream Raw Materials)
            (8, 13, 600, "rgba(220, 38, 38, 0.5)"),  # IonPeak to Umber SiC
            (8, 14, 300, "rgba(217, 119, 6, 0.3)"),  # IonPeak to Verdant Gas
            (10, 15, 180, "#E2E8F0"),                # Orion to Yarrow Alumina
            (12, 16, 250, "rgba(220, 38, 38, 0.5)"), # Delta Cap to Meridian BOPP Film
        ]

        # Filter by product if chosen
        if "P1" in filter_prod:
            active_links = [l for l in raw_links if l[0] in [0, 3, 4, 5, 8, 10, 12, 13, 14, 16]]
        elif "P2" in filter_prod:
            active_links = [l for l in raw_links if l[0] in [1, 3, 4, 6, 8, 10, 12, 13, 14]]
        elif "P3" in filter_prod:
            active_links = [l for l in raw_links if l[0] in [2, 3, 4, 7, 8, 10, 12, 13, 14]]
        else:
            active_links = raw_links

        sources = [l[0] for l in active_links]
        targets = [l[1] for l in active_links]
        values = [l[2] for l in active_links]
        colors = [l[3] for l in active_links]

        fig_sankey = go.Figure(data=[go.Sankey(
            node=dict(
                pad=18,
                thickness=18,
                line=dict(color="#CBD5E1", width=0.5),
                label=node_labels,
                color=node_colors,
                hovertemplate="<b>%{label}</b><br>Flow Throughput: $%{value}M<extra></extra>"
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                color=colors,
                hovertemplate="<b>%{source.label}</b> -> <b>%{target.label}</b><br>Value Funnel: $%{value}M<extra></extra>"
            )
        )])

        fig_sankey.update_layout(
            title=dict(
                text="<b>Multi-Tier Value Stream Flow (End Platforms -> Tier-1 -> Tier-2 -> Tier-3 Raw Materials)</b>",
                font=dict(size=14, color="#0A2540", family="Plus Jakarta Sans, sans-serif")
            ),
            font=dict(family="Plus Jakarta Sans, sans-serif", size=11, color="#334155"),
            height=480,
            margin=dict(l=15, r=15, t=45, b=15),
            paper_bgcolor="#FFFFFF"
        )

        st.plotly_chart(fig_sankey, use_container_width=True)

        st.markdown("""
        <div style="display: flex; gap: 20px; align-items: center; justify-content: center; margin-top: -6px; margin-bottom: 20px; font-size: 12px; color: #64748B;">
            <div><span style="display: inline-block; width: 12px; height: 12px; background: #0A2540; border-radius: 2px; vertical-align: middle;"></span> Finished Platforms</div>
            <div><span style="display: inline-block; width: 12px; height: 12px; background: #1E40AF; border-radius: 2px; vertical-align: middle;"></span> Tier-1 Direct Assemblers</div>
            <div><span style="display: inline-block; width: 12px; height: 12px; background: #DC2626; border-radius: 2px; vertical-align: middle;"></span> Critical Chokepoint Nodes</div>
            <div><span style="display: inline-block; width: 12px; height: 12px; background: #D97706; border-radius: 2px; vertical-align: middle;"></span> Clustered Z01 Facilities</div>
        </div>
        """, unsafe_allow_html=True)

    # Chokepoint Action Cards
    st.markdown("<div style='font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #64748B; margin: 20px 0 10px 0;'>Critical Chokepoint Diagnostics — Forensic Takeaways</div>", unsafe_allow_html=True)
    
    crit_entities = [
        {
            "id": "ORG-439",
            "name": "IonPeak Semiconductor",
            "tier": "Tier-2",
            "badge": "pill-red",
            "badge_text": "Sole Die Maker",
            "rev": "$1,560M",
            "comp": "M10 & M20 Power Dies",
            "cause": "Sole qualified die maker globally. Primary facility SITE-074 is in the Zone Z01 flood plain. Backup SITE-900 is an unapproved pilot line.",
            "evidence": "DOC-077, DOC-078"
        },
        {
            "id": "ORG-453",
            "name": "Jade Printed Circuits",
            "tier": "Tier-2",
            "badge": "pill-red",
            "badge_text": "Sole Bare PCB Maker",
            "rev": "$1,560M",
            "comp": "C10 Control & B10 Power Boards",
            "cause": "Sole qualified high-density PCB substrate supplier. Plant SITE-081 is located directly in the Zone Z01 East Delta flood plain.",
            "evidence": "DOC-079, DOC-080"
        },
        {
            "id": "ORG-454",
            "name": "Meridian Dielectrics",
            "tier": "Tier-3",
            "badge": "pill-amber",
            "badge_text": "Sole BOPP Film",
            "rev": "$624M",
            "comp": "DC-Link Film Capacitors",
            "cause": "Sole supplier of 2.8μm BOPP dielectric film. Currently renegotiating trade debt covenants and creditor terms under formal watch.",
            "evidence": "EV-003, DOC-081"
        },
        {
            "id": "ORG-247 / ORG-725",
            "name": "Aster Power / Boreal Power",
            "tier": "Tier-1",
            "badge": "pill-amber",
            "badge_text": "CommonSpan Dual Source",
            "rev": "$1,144M",
            "comp": "M10 & M20 Module Assemblies",
            "cause": "Ostensibly competing dual sources are 100% owned subsidiaries of CommonSpan Holdings. Shared treasury and cross-default covenants.",
            "evidence": "DOC-001, DOC-075"
        }
    ]

    c_rows = st.columns(2)
    for idx, c_item in enumerate(crit_entities):
        col = c_rows[idx % 2]
        with col:
            st.markdown(f"""
            <div class="action-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <span class="pill {c_item['badge']}"><span class="pill-dot"></span> {c_item['badge_text']}</span>
                        <h4 style="margin: 6px 0 0 0; font-size: 15px; font-weight: 700; color: #0A2540;">{c_item['name']} ({c_item['id']})</h4>
                        <div style="font-size: 12px; color: #64748B; margin-top: 2px;">{c_item['tier']} | Feeds: {c_item['comp']}</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 18px; font-weight: 800; color: #0A2540;">{c_item['rev']}</div>
                        <div style="font-size: 10px; font-weight: 600; color: #64748B;">Revenue At Risk</div>
                    </div>
                </div>
                <div style="margin-top: 10px; font-size: 12.5px; color: #334155; line-height: 1.5;">
                    <strong>Root Cause:</strong> {c_item['cause']}
                </div>
                <div style="margin-top: 6px; font-size: 11.5px; color: #64748B;">
                    <strong>Evidence Dossier:</strong> <code>{c_item['evidence']}</code>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Forensic Evidence Drilldown
    with st.expander("Audit Forensic Evidence Dossier on Selected Chokepoint", expanded=False):
        selected_choke_eid = st.selectbox(
            "Select Counterparty ID to Audit:",
            ["ORG-439", "ORG-453", "ORG-454", "ORG-247", "ORG-725"],
            index=0
        )
        if selected_choke_eid:
            render_evidence_inspector(selected_choke_eid, df_scorecard, df_evid)

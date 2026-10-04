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
    Renders an uncluttered, high-impact supply network architecture map,
    corporate ownership overlays, and chokepoint diagnostics.
    """
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
        <div>
            <h3 style="margin: 0; font-size: 16px; font-weight: 600; color: #0A2540;">Multi-Tier Architecture & Dependency Graph</h3>
            <p style="margin: 2px 0 0 0; color: #64748B; font-size: 12.5px;">
                Structural mapping from finished platforms down to Tier-3 raw material suppliers.
            </p>
        </div>
        <div>
            <span class="pill pill-red"><span class="pill-dot"></span> CommonSpan Disclosed</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Executive Strategic Callouts (High visual breathing room, crisp action cards)
    c_w1, c_w2 = st.columns(2)
    with c_w1:
        st.markdown("""
        <div class="action-card-critical">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <span class="pill pill-red"><span class="pill-dot"></span> Corporate Governance Risk</span>
                    <h4 style="margin: 4px 0 0 0; font-size: 14.5px; color: #0A2540;">The CommonSpan Dual-Sourcing Illusion</h4>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 17px; font-weight: 700; color: #991B1B;">$1,144M</div>
                    <div style="font-size: 10px; color: #64748B;">P1 & P2 Revenue</div>
                </div>
            </div>
            <p style="font-size: 12px; color: #334155; margin: 8px 0 0 0; line-height: 1.5;">
                NovaDrive ostensibly dual-sources power assemblies <strong>M10 & M20</strong> across <strong>Aster Power (60%)</strong> and <strong>Boreal Power (40%)</strong>.<br>
                Filing <code>DOC-075</code> confirms both entities are <strong>100% owned subsidiaries of CommonSpan Holdings</strong>. Parent insolvency halts assembly across both suppliers simultaneously.
            </p>
            <div style="margin-top: 8px; padding-top: 6px; border-top: 1px solid #FEE2E2; font-size: 11.5px; color: #7F1D1D;">
                <strong>CRO Action:</strong> Require independent bank ring-fencing guarantees or qualify an un-affiliated module supplier.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c_w2:
        st.markdown("""
        <div class="action-card-warning">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <span class="pill pill-amber"><span class="pill-dot"></span> Sub-Tier Concentration</span>
                    <h4 style="margin: 4px 0 0 0; font-size: 14.5px; color: #0A2540;">The Upstream Chokepoint Triad</h4>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 17px; font-weight: 700; color: #B45309;">$1,560M</div>
                    <div style="font-size: 10px; color: #64748B;">100% Portfolio Reach</div>
                </div>
            </div>
            <p style="font-size: 12px; color: #334155; margin: 8px 0 0 0; line-height: 1.5;">
                <strong>IonPeak Semiconductor (Tier-2):</strong> Sole SiC die supplier ($1,560M reach, flood basin SITE-074).<br>
                <strong>Jade Printed Circuits (Tier-2):</strong> Sole bare PCB supplier for C10 & B10 ($1,560M reach).<br>
                <strong>Meridian Dielectrics (Tier-3):</strong> Sole BOPP film supplier ($624M reach, debt distress <code>EV-003</code>).
            </p>
            <div style="margin-top: 8px; padding-top: 6px; border-top: 1px solid #FEF3C7; font-size: 11.5px; color: #92400E;">
                <strong>CRO Action:</strong> Audit off-site forward buffer inventory and initiate dual-sourcing sprints.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Clean Filter Bar
    f1, f2, f3 = st.columns([1, 1, 1])
    filter_prod = f1.selectbox("Filter Path by Product Line:", ["All Products (P1, P2, P3)", "P1 - DriveCore Inverter ($624M)", "P2 - ChargeBridge Power ($520M)", "P3 - StoreLink Storage ($416M)"])
    filter_comp = f2.selectbox("Filter Path by Component:", ["All Components", "M10 - Standard power assembly", "M20 - High-voltage power assembly", "C10 - Control board", "B10 - Power distribution board", "D10 - Inverter sub-assembly"])
    highlight_chokepoints = f3.checkbox("Highlight CommonSpan Ownership Link", value=True)

    # Plotly Graph Construction
    if HAS_PLOTLY:
        nodes = [
            # Tier 0: Products
            {"id": "P1", "label": "P1 DriveCore<br>($624M)", "tier": 0, "x": 0.08, "y": 0.8, "color": "#0A2540", "size": 26, "info": "Industrial Inverter | $624M Revenue | Harbor & Plateau Works"},
            {"id": "P2", "label": "P2 ChargeBridge<br>($520M)", "tier": 0, "x": 0.08, "y": 0.5, "color": "#0A2540", "size": 24, "info": "Charging Unit | $520M Revenue | Harbor & Coastal Works"},
            {"id": "P3", "label": "P3 StoreLink<br>($416M)", "tier": 0, "x": 0.08, "y": 0.2, "color": "#0A2540", "size": 22, "info": "Storage Cabinet | $416M Revenue | Plateau Works"},

            # Tier 1: Direct Suppliers
            {"id": "ORG-247", "label": "Aster Power<br>(T1, 60%)", "tier": 1, "x": 0.35, "y": 0.85, "color": "#0066CC", "size": 20, "info": "Tier-1 | M10/M20 Assembler | Subsidiary of CommonSpan (DOC-075)"},
            {"id": "ORG-725", "label": "Boreal Power<br>(T1, 40%)", "tier": 1, "x": 0.35, "y": 0.65, "color": "#0066CC", "size": 20, "info": "Tier-1 | M10/M20 Assembler | Subsidiary of CommonSpan (DOC-075)"},
            {"id": "ORG-119", "label": "Cobalt Control<br>(T1)", "tier": 1, "x": 0.35, "y": 0.45, "color": "#0284C7", "size": 17, "info": "Tier-1 | C10 Control Board"},
            {"id": "ORG-268", "label": "Grove Energy<br>(T1)", "tier": 1, "x": 0.35, "y": 0.25, "color": "#0284C7", "size": 17, "info": "Tier-1 | B10 Power Board"},
            {"id": "ORG-333", "label": "HarborSense<br>(T1)", "tier": 1, "x": 0.35, "y": 0.05, "color": "#0284C7", "size": 15, "info": "Tier-1 | S10 Sensor Assembly"},

            # Tier 2: Sub-Suppliers
            {"id": "ORG-439", "label": "IonPeak Semi<br>(T2 Chokepoint)", "tier": 2, "x": 0.65, "y": 0.85, "color": "#DC2626", "size": 26, "info": "CRITICAL CHOKEPOINT | Sole SiC Die Supplier | Zone Z01 Flood Basin | $1,560M Reach"},
            {"id": "ORG-440", "label": "Lumen Magnetics<br>(T2)", "tier": 2, "x": 0.65, "y": 0.65, "color": "#64748B", "size": 15, "info": "Tier-2 | Magnetic Inductor Cores"},
            {"id": "ORG-441", "label": "Orion Ceramics<br>(T2)", "tier": 2, "x": 0.65, "y": 0.50, "color": "#D97706", "size": 17, "info": "Tier-2 | Ceramic Substrates | Located in Zone Z01"},
            {"id": "ORG-453", "label": "Jade Printed<br>(T2 Chokepoint)", "tier": 2, "x": 0.65, "y": 0.30, "color": "#DC2626", "size": 26, "info": "CRITICAL CHOKEPOINT | Sole PCB Substrate | Zone Z01 Flood Basin | $1,560M Reach"},
            {"id": "ORG-922", "label": "Delta Capacitor<br>(T2)", "tier": 2, "x": 0.65, "y": 0.10, "color": "#D97706", "size": 17, "info": "Tier-2 | DC-Link Film Capacitors"},

            # Tier 3: Upstream Raw Materials
            {"id": "ORG-455", "label": "Umber SiC<br>(T3)", "tier": 3, "x": 0.92, "y": 0.95, "color": "#DC2626", "size": 18, "info": "Tier-3 | SiC Boules/Wafers to IonPeak | Zone Z01 Flood Basin"},
            {"id": "ORG-456", "label": "Verdant Gases<br>(T3)", "tier": 3, "x": 0.92, "y": 0.80, "color": "#D97706", "size": 15, "info": "Tier-3 | Process Silane Gas to IonPeak | Zone Z01 Flood Basin"},
            {"id": "ORG-457", "label": "Yarrow Minerals<br>(T3)", "tier": 3, "x": 0.92, "y": 0.55, "color": "#64748B", "size": 14, "info": "Tier-3 | High-Purity Alumina to Orion"},
            {"id": "ORG-454", "label": "Meridian Diel.<br>(T3 Chokepoint)", "tier": 3, "x": 0.92, "y": 0.15, "color": "#DC2626", "size": 22, "info": "CRITICAL CHOKEPOINT | Sole 2.8μm BOPP Dielectric Film | EV-003 Debt Default Watch"},
        ]

        edges = [
            ("P1", "ORG-247", "M10 Assembly (60%)", "#94A3B8", 1.5),
            ("P1", "ORG-725", "M10 Assembly (40%)", "#94A3B8", 1.2),
            ("P1", "ORG-119", "C10 Control Board", "#94A3B8", 1.0),
            ("P2", "ORG-247", "M20 HV Assembly (70%)", "#94A3B8", 1.5),
            ("P2", "ORG-725", "M20 HV Assembly (30%)", "#94A3B8", 1.2),
            ("P2", "ORG-268", "B10 Power Board", "#94A3B8", 1.0),
            ("P3", "ORG-247", "M10 Assembly", "#94A3B8", 1.2),
            ("P3", "ORG-333", "S10 Sensors", "#94A3B8", 1.0),
            ("ORG-247", "ORG-439", "SiC Power Dies", "#DC2626", 2.2),
            ("ORG-725", "ORG-439", "SiC Power Dies", "#DC2626", 2.2),
            ("ORG-247", "ORG-440", "Magnetic Cores", "#CBD5E1", 1.0),
            ("ORG-725", "ORG-440", "Magnetic Cores", "#CBD5E1", 1.0),
            ("ORG-247", "ORG-441", "Ceramic Substrates", "#D97706", 1.5),
            ("ORG-725", "ORG-441", "Ceramic Substrates", "#D97706", 1.5),
            ("ORG-119", "ORG-453", "Bare PCB Substrates", "#DC2626", 2.2),
            ("ORG-268", "ORG-453", "Bare PCB Substrates", "#DC2626", 2.2),
            ("ORG-247", "ORG-922", "DC-link Capacitors", "#D97706", 1.5),
            ("ORG-725", "ORG-922", "DC-link Capacitors", "#D97706", 1.5),
            ("ORG-439", "ORG-455", "SiC Wafers", "#DC2626", 1.8),
            ("ORG-439", "ORG-456", "Silane Gas", "#D97706", 1.2),
            ("ORG-441", "ORG-457", "Specialty Alumina", "#CBD5E1", 1.0),
            ("ORG-922", "ORG-454", "Dielectric Film", "#DC2626", 2.2),
        ]

        ownership_edges = [
            ("ORG-247", "ORG-725", "CommonSpan Holdings (100% Shared Ownership)", "#DC2626", 2.0, "dash")
        ]

        fig = go.Figure()

        # Render edges
        for src_id, dst_id, edge_lbl, e_color, e_width in edges:
            src_n = next((n for n in nodes if n["id"] == src_id), None)
            dst_n = next((n for n in nodes if n["id"] == dst_id), None)
            if src_n and dst_n:
                fig.add_trace(go.Scatter(
                    x=[src_n["x"], dst_n["x"]],
                    y=[src_n["y"], dst_n["y"]],
                    mode="lines",
                    line=dict(color=e_color, width=e_width),
                    hoverinfo="text",
                    text=f"{edge_lbl}: {src_n['id']} -> {dst_n['id']}",
                    showlegend=False
                ))

        if highlight_chokepoints:
            for src_id, dst_id, edge_lbl, e_color, e_width, dash_style in ownership_edges:
                src_n = next((n for n in nodes if n["id"] == src_id), None)
                dst_n = next((n for n in nodes if n["id"] == dst_id), None)
                if src_n and dst_n:
                    fig.add_trace(go.Scatter(
                        x=[src_n["x"], dst_n["x"]],
                        y=[src_n["y"], dst_n["y"]],
                        mode="lines+text",
                        line=dict(color="#DC2626", width=2.0, dash="dot"),
                        hoverinfo="text",
                        text=[None, "CommonSpan 100% Shared Ownership"],
                        textposition="middle right",
                        name="CommonSpan Shared Ownership",
                        showlegend=True
                    ))

        # Render nodes
        for n in nodes:
            fig.add_trace(go.Scatter(
                x=[n["x"]],
                y=[n["y"]],
                mode="markers+text",
                marker=dict(size=n["size"], color=n["color"], line=dict(color="#FFFFFF", width=2)),
                text=[n["label"]],
                textposition="bottom center",
                textfont=dict(size=9.5, family="Inter, sans-serif", color="#0A2540"),
                hoverinfo="text",
                hovertext=f"<b>{n['id']}</b><br>{n['info']}",
                showlegend=False
            ))

        fig.update_layout(
            title=dict(
                text="<b>Multi-Tier Supply Chain Architecture & Corporate Ownership Overlay</b>",
                font=dict(size=13, color="#0A2540", family="Inter, sans-serif")
            ),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.02, 1.05]),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.12, 1.05]),
            height=460,
            margin=dict(l=15, r=15, t=40, b=20),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

    # Chokepoint Action Cards
    st.markdown("<div style='font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #64748B; margin: 16px 0 8px 0;'>Critical Chokepoint Roster — High-Risk Nodes</div>", unsafe_allow_html=True)
    
    crit_entities = [
        {
            "id": "ORG-439",
            "name": "IonPeak Semiconductor",
            "tier": "Tier-2",
            "badge": "pill-red",
            "badge_text": "Sole Die Maker",
            "rev": "$1,560M",
            "comp": "M10 & M20 Power Dies",
            "cause": "Sole qualified die maker globally. Primary plant SITE-074 is in Zone Z01 flood plain. Backup SITE-900 unapproved.",
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
            "cause": "Sole qualified high-density PCB substrate supplier. Plant SITE-081 located in Zone Z01 flood plain.",
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
            "cause": "Sole supplier of 2.8μm BOPP dielectric film. Currently renegotiating trade debt covenants and creditor terms.",
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
            "cause": "Ostensibly competing dual sources are 100% owned subsidiaries of CommonSpan Holdings. Shared treasury.",
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
                        <h4 style="margin: 4px 0 0 0; font-size: 14px; color: #0A2540;">{c_item['name']} ({c_item['id']})</h4>
                        <div style="font-size: 11.5px; color: #64748B;">{c_item['tier']} | Feeds: {c_item['comp']}</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 16px; font-weight: 700; color: #0A2540;">{c_item['rev']}</div>
                        <div style="font-size: 10px; color: #64748B;">Revenue At Risk</div>
                    </div>
                </div>
                <div style="margin-top: 8px; font-size: 12px; color: #334155; line-height: 1.45;">
                    <strong>Root Cause:</strong> {c_item['cause']}
                </div>
                <div style="margin-top: 4px; font-size: 11px; color: #64748B;">
                    <strong>Evidence Dossier:</strong> <code>{c_item['evidence']}</code>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Forensic Drilldown Expander
    with st.expander("Forensic Evidence Audit on Selected Chokepoint", expanded=False):
        selected_choke_eid = st.selectbox(
            "Select Counterparty ID to Audit:",
            ["ORG-439", "ORG-453", "ORG-454", "ORG-247", "ORG-725"],
            index=0
        )
        if selected_choke_eid:
            render_evidence_inspector(selected_choke_eid, df_scorecard, df_evid)

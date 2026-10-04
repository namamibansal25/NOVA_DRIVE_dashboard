"""
NovaDrive Technologies | Real-Time Event Audit Log & Threat Triage Module
Real-time monitoring of operational disruptions, deduplication controls, and false-alarm suppression.
"""

import streamlit as st
import pandas as pd
try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

def render_alerts_view(df_events, df_flood, df_excluded, df_scorecard, df_evid):
    """
    Renders an uncluttered, action-oriented real-time event audit log,
    false-positive quarantine, and flood exposure assessment.
    """
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <div>
            <h3 style="margin: 0; font-size: 18px; font-weight: 700; color: #0A2540;">Real-Time Threat Triage & Event Audit Feed</h3>
            <p style="margin: 3px 0 0 0; color: #64748B; font-size: 13px;">
                Continuous event monitoring with automated false-positive quarantine and multi-tier flood plain surveillance.
            </p>
        </div>
        <div>
            <span class="pill pill-red"><span class="pill-dot"></span> Active Flood Advisory EV-001</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Active High-Priority Strategic Event Banner
    st.markdown("""
    <div class="action-card-critical">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 14px;">
            <div>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                    <span class="pill pill-red"><span class="pill-dot"></span> Active Threat Advisory</span>
                    <strong style="color: #991B1B; font-size: 14px;">Event EV-001: East Delta Basin Flood Warning (Zone Z01)</strong>
                </div>
                <div style="font-size: 13px; color: #334155; line-height: 1.55; margin-top: 4px;">
                    Regional hydrologic authority published a formal flood warning for the East Delta industrial corridor. While physical floodwalls currently hold, <strong>5 interconnected sole-source facilities</strong> reside in this flood basin.<br>
                    <strong>Exposed Counterparties:</strong> IonPeak Semi (SITE-074), Jade Printed (SITE-081), Orion Ceramics (SITE-116), Umber SiC (SITE-158), Verdant Gases (SITE-165).
                </div>
            </div>
            <div style="text-align: right; min-width: 160px;">
                <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: #64748B;">Total Portfolio Exposure</div>
                <div style="font-size: 24px; font-weight: 800; color: #991B1B;">$1,560M</div>
                <div style="font-size: 11.5px; font-weight: 600; color: #64748B;">100% Active Turnover</div>
            </div>
        </div>
        <div style="margin-top: 12px; padding-top: 10px; border-top: 1px solid #FEE2E2; font-size: 12.5px; color: #7F1D1D; display: flex; justify-content: space-between; align-items: center;">
            <div><strong>Qualified Alternate in Network:</strong> Zero. Any flood crest breach at IonPeak or Jade halts vehicle assembly globally.</div>
            <div><span class="pill pill-gray">Source Family: WX-0923</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Clean Line Tabs
    a_tab1, a_tab2, a_tab3 = st.tabs([
        "Active Threat Feed & Triage",
        "Zone Z01 Flood Exposure Assessment",
        "Automated False-Positive Quarantine"
    ])

    # 1. LIVE THREAT FEED & TRIAGE
    with a_tab1:
        f_c1, f_c2 = st.columns([2, 1])
        prio_filter = f_c1.radio(
            "Filter Feed by Status:",
            ["All Events", "Actionable Alerts", "Duplicates & Informational", "Financial Distress"],
            horizontal=True
        )

        events_list = []
        if not df_events.empty:
            for _, ev in df_events.iterrows():
                prio = str(ev.get("Alert Priority", "INFORMATIONAL")).upper()
                detail = ev.get("Event Detail", "")
                src_fam = ev.get("Source Family ID", "")

                if prio_filter == "Actionable Alerts" and ("DUPLICATE" in prio or "INFORMATIONAL" in prio):
                    continue
                if prio_filter == "Duplicates & Informational" and not ("DUPLICATE" in prio or "INFORMATIONAL" in prio):
                    continue
                if prio_filter == "Financial Distress" and not ("MD-FIN" in src_fam or "financial" in detail.lower() or "covenant" in detail.lower()):
                    continue

                events_list.append(ev)

        for ev in events_list:
            ev_id = ev.get("Event ID", "")
            title = ev.get("Title", "")
            prio = str(ev.get("Alert Priority", "INFORMATIONAL")).upper()
            detail = ev.get("Event Detail", "")
            match_res = ev.get("Match Result", "")
            comps_aff = ev.get("Affected Component(s)", "")
            prods_aff = ev.get("Affected Product(s)", "")
            action = ev.get("Required Verification / Next Action", "")
            dup_ctrl = ev.get("False Positive / Duplication Control", "")
            src_fam = ev.get("Source Family ID", "")

            if "HIGH" in prio or "CRITICAL" in prio:
                card_border = "#FECDD3"
                card_accent = "#E11D48"
                card_bg = "#FFF8F8"
                pill_cls = "pill-red"
            elif "DUPLICATE" in prio or "INFORMATIONAL" in prio:
                card_border = "#CBD5E1"
                card_accent = "#64748B"
                card_bg = "#F8FAFC"
                pill_cls = "pill-gray"
            else:
                card_border = "#FDE68A"
                card_accent = "#D97706"
                card_bg = "#FFFDF7"
                pill_cls = "pill-amber"

            st.markdown(f"""
            <div class="action-card" style="background: {card_bg}; border: 1px solid {card_border}; border-left: 6px solid {card_accent}; border-radius: 12px; padding: 20px 24px; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                    <div>
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                            <span class="pill {pill_cls}"><span class="pill-dot"></span> {prio}</span>
                            <span style="font-size: 11.5px; color: #64748B; font-weight: 700;">ID: {ev_id}</span>
                            <span style="color: #CBD5E1;">|</span>
                            <span style="font-size: 11.5px; color: #64748B; font-weight: 600;">SOURCE: <code>{src_fam}</code></span>
                        </div>
                        <h4 style="margin: 0; font-size: 16px; font-weight: 800; color: #0A2540;">{title}</h4>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 12.5px; font-weight: 700; color: #0A2540;">Products: {prods_aff}</span><br>
                        <span style="font-size: 11.5px; color: #64748B;">Components: {comps_aff}</span>
                    </div>
                </div>
                <p style="margin: 8px 0 6px 0; font-size: 13px; color: #334155; line-height: 1.55;">{detail}</p>
                <div style="background-color: #FFFFFF; border: 1px solid {card_border}; padding: 8px 12px; border-radius: 6px; margin-top: 8px; font-size: 12px; color: #1E293B;">
                    <strong>Match & Significance:</strong> {match_res}
                </div>
                <div style="margin-top: 10px; font-size: 13px; color: #0A2540; font-weight: 700;">
                    CRO Mandate: {action}
                </div>
                <div style="margin-top: 4px; font-size: 11.5px; color: #64748B;">
                    <strong>Deduplication Control:</strong> {dup_ctrl}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 2. Z01 FLOOD-WATCH EXPOSURE MAP
    with a_tab2:
        st.markdown("<div style='font-size: 15px; font-weight: 700; color: #0A2540; margin-bottom: 4px;'>Zone Z01 East Delta Facility Exposure Assessment</div>", unsafe_allow_html=True)
        st.caption("Site-by-site inventory identifying unmitigated sole-source vulnerabilities in the flood plain.")

        # Infographic: Facility Exposure Breakdown
        if HAS_PLOTLY:
            z01_sites = [
                {"site": "SITE-074 IonPeak (T2)", "role": "SiC Power Dies", "rev": 1560, "alt": "None (Sole Source)"},
                {"site": "SITE-081 Jade Circuits (T2)", "role": "Bare PCB Substrates", "rev": 1560, "alt": "None (Sole Source)"},
                {"site": "SITE-116 Orion Ceramics (T2)", "role": "Ceramic DBC Substrates", "rev": 1144, "alt": "None (Sole Source)"},
                {"site": "SITE-158 Umber SiC (T3)", "role": "SiC Boules / Wafers", "rev": 1144, "alt": "None (Sole Source)"},
                {"site": "SITE-165 Verdant Gases (T3)", "role": "Process Silane Gas", "rev": 1144, "alt": "None (Sole Source)"}
            ]

            fig_z01 = go.Figure()
            fig_z01.add_trace(go.Bar(
                x=[s["rev"] for s in z01_sites],
                y=[s["site"] for s in z01_sites],
                orientation="h",
                marker=dict(color="#DC2626"),
                text=[f"${s['rev']}M ({s['role']})" for s in z01_sites],
                textposition="inside",
                insidetextfont=dict(color="#FFFFFF", size=11, family="Plus Jakarta Sans", weight="bold"),
                hovertemplate="<b>%{y}</b><br>Revenue at Risk: $%{x}M<br>Alternate Qualified: None<extra></extra>"
            ))

            st.markdown("""
            <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 10px; padding: 12px 18px 4px 18px; margin-top: 10px; margin-bottom: 2px;">
                <div style="font-size: 14.5px; font-weight: 800; color: #0A2540;">Dependent Enterprise Revenue Clustered in Zone Z01 Flood Plain ($M)</div>
                <div style="font-size: 12px; color: #64748B;">Site-by-site revenue impact across five sole-source nodes residing in the East Delta basin.</div>
            </div>
            """, unsafe_allow_html=True)

            fig_z01.update_layout(
                title=None,
                height=220,
                margin=dict(l=15, r=15, t=10, b=20),
                xaxis=dict(range=[0, 1750], showgrid=True, gridcolor="#F1F5F9", title="Annual Dependent Turnover ($M)"),
                yaxis=dict(showgrid=False, autorange="reversed"),
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                font=dict(family="Plus Jakarta Sans", size=11, color="#334155")
            )
            st.plotly_chart(fig_z01, use_container_width=True)

        if not df_flood.empty:
            with st.expander("Inspect Raw Facility Registry & Flood Basin Metrics", expanded=False):
                flood_display = df_flood[[
                    "Entity ID", "Entity", "Facility ID", "Facility zone (lookup)", "Network tier",
                    "Components exposed", "Products reached", "Revenue dependent (USD m)",
                    "Supplier risk score", "Qualified alternate in network?"
                ]].copy()
                st.dataframe(flood_display, use_container_width=True)

        st.markdown("<div style='font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #64748B; margin: 20px 0 10px 0;'>Strategic Action Checklist — Zone Z01 Risk Mitigation</div>", unsafe_allow_html=True)
        
        c_act1, c_act2, c_act3 = st.columns(3)
        with c_act1:
            st.markdown("""
            <div class="action-card">
                <span class="pill pill-blue"><span class="pill-dot"></span> Action 1: Physical Audit</span>
                <h4 style="margin: 6px 0 2px 0; font-size: 14px; font-weight: 700; color: #0A2540;">Inspect Flood Defenses</h4>
                <p style="font-size: 12px; color: #64748B; margin: 4px 0 0 0; line-height: 1.5;">
                    Dispatch independent civil engineering auditors to IonPeak (SITE-074) and Jade (SITE-081) to verify flood barrier crest heights and emergency generator fuel autonomy.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with c_act2:
            st.markdown("""
            <div class="action-card">
                <span class="pill pill-blue"><span class="pill-dot"></span> Action 2: Buffer Verification</span>
                <h4 style="margin: 6px 0 2px 0; font-size: 14px; font-weight: 700; color: #0A2540;">Forward Buffer Pull</h4>
                <p style="font-size: 12px; color: #64748B; margin: 4px 0 0 0; line-height: 1.5;">
                    Conduct physical cycle-counts of finished dies and bare boards in warehouses outside Zone Z01. Authorize emergency pull order to extend inventory cover to 30 days.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with c_act3:
            st.markdown("""
            <div class="action-card">
                <span class="pill pill-blue"><span class="pill-dot"></span> Action 3: Sourcing Sprint</span>
                <h4 style="margin: 6px 0 2px 0; font-size: 14px; font-weight: 700; color: #0A2540;">Parallel Qualification</h4>
                <p style="font-size: 12px; color: #64748B; margin: 4px 0 0 0; line-height: 1.5;">
                    Issue expedited sample purchase orders to candidate PCB and power assembly fabricators in non-flood regions to initiate 12-week PPAP qualification sprint.
                </p>
            </div>
            """, unsafe_allow_html=True)

    # 3. FALSE-POSITIVE & EXCLUDED ENTITIES QUARANTINE
    with a_tab3:
        st.markdown("<div style='font-size: 15px; font-weight: 700; color: #0A2540; margin-bottom: 4px;'>Automated False-Positive Quarantine Log</div>", unsafe_allow_html=True)
        st.caption("Automated exclusion logic preventing alert inflation caused by corporate name confusion and obsolete agreements.")

        if not df_excluded.empty:
            st.dataframe(df_excluded, use_container_width=True)
            
        st.markdown("""
        <div class="action-card" style="margin-top: 14px;">
            <div style="font-size: 12px; text-transform: uppercase; font-weight: 700; color: #64748B; margin-bottom: 8px;">Automated Deduplication & False Alarm Mitigation Rules:</div>
            <ul style="font-size: 13px; color: #334155; line-height: 1.6; margin: 0; padding-left: 20px;">
                <li><strong>Delta Consumer Plastics (ORG-857):</strong> Filtered. Shares name prefix with Delta Capacitor Works (ORG-922) but manufactures retail packaging. Event EV-009 safely quarantined.</li>
                <li><strong>EV-002 Trade Bulletin:</strong> Republication of official authority bulletin EV-001. Suppressed via Source Family ID <code>WX-0923</code> to eliminate artificial alert inflation.</li>
                <li><strong>Apex Micro Systems (ORG-999):</strong> Obsolete 2023 development agreement; confirmed inactive in active serial production.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

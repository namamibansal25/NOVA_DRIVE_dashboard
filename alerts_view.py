"""
NovaDrive Technologies | Real-Time Event Audit Log & Threat Triage Module
Real-time monitoring of operational disruptions, deduplication controls, and false-alarm suppression.
"""

import streamlit as st
import pandas as pd

def render_alerts_view(df_events, df_flood, df_excluded, df_scorecard, df_evid):
    """
    Renders an uncluttered, action-oriented real-time event audit log,
    false-positive quarantine, and flood exposure assessment.
    """
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
        <div>
            <h3 style="margin: 0; font-size: 16px; font-weight: 600; color: #0A2540;">Real-Time Event Audit Log & Threat Triage</h3>
            <p style="margin: 2px 0 0 0; color: #64748B; font-size: 12.5px;">
                Continuous event monitoring with automated false-positive suppression and deduplication.
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
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
            <div>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                    <span class="pill pill-red"><span class="pill-dot"></span> Active Flood Advisory</span>
                    <strong style="color: #991B1B; font-size: 13.5px;">Event EV-001: East Delta Flood Warning (Zone Z01 Basin)</strong>
                </div>
                <div style="font-size: 12.5px; color: #334155; line-height: 1.5; margin-top: 4px;">
                    Regional authority bulletin confirmed rising water levels across Zone Z01. While plant dikes currently hold, <strong>5 interconnected facilities</strong> are located in this basin.<br>
                    <strong>Exposed Counterparties:</strong> IonPeak Semi (SITE-074), Jade Printed (SITE-081), Orion Ceramics (SITE-116), Umber SiC (SITE-158), Verdant Gases (SITE-165).
                </div>
            </div>
            <div style="text-align: right; min-width: 140px;">
                <div style="font-size: 10px; text-transform: uppercase; font-weight: 600; color: #64748B;">Total Portfolio Exposure</div>
                <div style="font-size: 22px; font-weight: 700; color: #991B1B;">$1,560M</div>
                <div style="font-size: 11px; color: #64748B;">100% Active Revenue</div>
            </div>
        </div>
        <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid #FEE2E2; font-size: 12px; color: #7F1D1D; display: flex; justify-content: space-between; align-items: center;">
            <div><strong>Qualified Alternate in Network:</strong> None. Outage at IonPeak or Jade halts vehicle inverter assembly globally.</div>
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

            # Styling classes
            if "HIGH" in prio or "CRITICAL" in prio:
                card_cls = "action-card-critical"
                pill_cls = "pill-red"
            elif "DUPLICATE" in prio or "INFORMATIONAL" in prio:
                card_cls = "action-card"
                pill_cls = "pill-gray"
            else:
                card_cls = "action-card-warning"
                pill_cls = "pill-amber"

            st.markdown(f"""
            <div class="{card_cls}">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                    <div>
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                            <span class="pill {pill_cls}"><span class="pill-dot"></span> {prio}</span>
                            <span style="font-size: 11px; color: #64748B; font-weight: 600;">ID: {ev_id}</span>
                            <span style="color: #CBD5E1;">|</span>
                            <span style="font-size: 11px; color: #64748B;">FAMILY: <code>{src_fam}</code></span>
                        </div>
                        <h4 style="margin: 0; font-size: 14px; font-weight: 600; color: #0A2540;">{title}</h4>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 11.5px; font-weight: 600; color: #0A2540;">Products: {prods_aff}</span><br>
                        <span style="font-size: 11px; color: #64748B;">Components: {comps_aff}</span>
                    </div>
                </div>
                <p style="margin: 8px 0 6px 0; font-size: 12px; color: #334155; line-height: 1.5;">{detail}</p>
                <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 6px 10px; border-radius: 4px; margin-top: 6px; font-size: 11.5px; color: #1E293B;">
                    <strong>Match Assessment:</strong> {match_res}
                </div>
                <div style="margin-top: 8px; font-size: 12px; color: #0A2540;">
                    <strong>Action Required:</strong> {action}
                </div>
                <div style="margin-top: 3px; font-size: 11px; color: #64748B;">
                    <strong>Deduplication Control:</strong> {dup_ctrl}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 2. Z01 FLOOD-WATCH EXPOSURE MAP
    with a_tab2:
        st.markdown("<div style='font-size: 13px; font-weight: 600; color: #0A2540; margin-bottom: 4px;'>Zone Z01 East Delta Facility Exposure Assessment</div>", unsafe_allow_html=True)
        st.caption("Site-by-site inventory identifying unmitigated sole-source vulnerabilities in the flood plain.")

        if not df_flood.empty:
            flood_display = df_flood[[
                "Entity ID", "Entity", "Facility ID", "Facility zone (lookup)", "Network tier",
                "Components exposed", "Products reached", "Revenue dependent (USD m)",
                "Supplier risk score", "Qualified alternate in network?"
            ]].copy()
            
            st.dataframe(flood_display, use_container_width=True)

        st.markdown("<div style='font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #64748B; margin: 16px 0 8px 0;'>Strategic Action Checklist — Zone Z01 Risk Mitigation</div>", unsafe_allow_html=True)
        
        c_act1, c_act2, c_act3 = st.columns(3)
        with c_act1:
            st.markdown("""
            <div class="action-card">
                <span class="pill pill-blue"><span class="pill-dot"></span> Action 1: Physical Audit</span>
                <h4 style="margin: 6px 0 2px 0; font-size: 13.5px; color: #0A2540;">Inspect Facility Defenses</h4>
                <p style="font-size: 11.5px; color: #64748B; margin: 4px 0 0 0; line-height: 1.45;">
                    Dispatch independent civil engineering auditors to IonPeak (SITE-074) and Jade (SITE-081) to verify flood barrier crest heights and emergency generator fuel autonomy.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with c_act2:
            st.markdown("""
            <div class="action-card">
                <span class="pill pill-blue"><span class="pill-dot"></span> Action 2: Buffer Verification</span>
                <h4 style="margin: 6px 0 2px 0; font-size: 13.5px; color: #0A2540;">Forward Buffer Pull</h4>
                <p style="font-size: 11.5px; color: #64748B; margin: 4px 0 0 0; line-height: 1.45;">
                    Conduct physical cycle-counts of finished dies and bare boards located in warehouses outside Zone Z01. Authorize emergency pull order to extend inventory cover to 30 days.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with c_act3:
            st.markdown("""
            <div class="action-card">
                <span class="pill pill-blue"><span class="pill-dot"></span> Action 3: Sourcing Sprint</span>
                <h4 style="margin: 6px 0 2px 0; font-size: 13.5px; color: #0A2540;">Parallel Qualification</h4>
                <p style="font-size: 11.5px; color: #64748B; margin: 4px 0 0 0; line-height: 1.45;">
                    Issue expedited sample purchase orders to candidate PCB and power assembly fabricators in non-flood regions to initiate 12-week PPAP qualification sprint.
                </p>
            </div>
            """, unsafe_allow_html=True)

    # 3. FALSE-POSITIVE & EXCLUDED ENTITIES QUARANTINE
    with a_tab3:
        st.markdown("<div style='font-size: 13px; font-weight: 600; color: #0A2540; margin-bottom: 4px;'>Automated False-Positive Quarantine Log</div>", unsafe_allow_html=True)
        st.caption("Automated exclusion logic preventing alert inflation caused by corporate name confusion and obsolete agreements.")

        if not df_excluded.empty:
            st.dataframe(df_excluded, use_container_width=True)
            
        st.markdown("""
        <div class="action-card" style="margin-top: 12px;">
            <div style="font-size: 11px; text-transform: uppercase; font-weight: 600; color: #64748B; margin-bottom: 6px;">Automated Deduplication & False Alarm Mitigation Rules:</div>
            <ul style="font-size: 12px; color: #334155; line-height: 1.5; margin: 0; padding-left: 18px;">
                <li><strong>Delta Consumer Plastics (ORG-857):</strong> Filtered. Shares name prefix with Delta Capacitor Works (ORG-922) but manufactures retail packaging. Event EV-009 safely quarantined.</li>
                <li><strong>EV-002 Trade Bulletin:</strong> Republication of official authority bulletin EV-001. Suppressed via Source Family ID <code>WX-0923</code> to eliminate artificial alert inflation.</li>
                <li><strong>Apex Micro Systems (ORG-999):</strong> Obsolete 2023 development agreement; confirmed inactive in active serial production.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

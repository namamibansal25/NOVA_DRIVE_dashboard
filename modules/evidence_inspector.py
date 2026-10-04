"""
NovaDrive Technologies | Forensic Evidence Inspector Module
Forensic audit trail inspecting primary disclosures, regulatory filings, and scoring explainability.
"""

import streamlit as st
import pandas as pd

def render_evidence_inspector(selected_entity_id, df_scorecard, df_evid, df_excluded=None, df_flood=None, df_crit=None):
    """
    Renders an uncluttered, high-impact evidence audit dossier for the selected counterparty.
    """
    if not selected_entity_id or selected_entity_id == "Select Entity...":
        return

    entity_match = df_scorecard[df_scorecard["Entity ID"] == selected_entity_id]
    if entity_match.empty:
        st.warning(f"Entity ID {selected_entity_id} not found in the master scorecard.")
        return
        
    rec = entity_match.iloc[0]
    legal_name = rec.get("Legal Name", "Unknown")
    role = rec.get("Network role", rec.get("Entity Type", "Supplier"))
    score = rec.get("Supplier Risk Score", "N/A")
    risk_cat = str(rec.get("Risk Category", "UNSCORED")).upper()
    rev_dep = rec.get("Revenue dependent (USD m)", 0)
    chokepoint_status = str(rec.get("Chokepoint Status", "Standard Node"))
    prods_reached = rec.get("Products reached", "N/A")
    facility_id = rec.get("Primary Facility ID", "N/A")
    facility_zone = rec.get("Facility Zone", rec.get("Registered Zone", "N/A"))
    curr_ratio = rec.get("Current Ratio", "N/A")
    net_debt = rec.get("Net Debt / EBITDA", "N/A")
    timeliness = rec.get("Shipment Timeliness - 3M Avg (%)", "N/A")
    time_change = rec.get("Timeliness Change - Jan To Latest (pp)", "N/A")
    phys_haz = rec.get("Physical Hazard Index", "N/A")

    # Muted pill classes
    if risk_cat == "CRITICAL" or "CHOKEPOINT" in chokepoint_status.upper():
        pill_class = "pill-red"
        card_class = "action-card-critical"
    elif risk_cat == "HIGH" or "COMMON OWNERSHIP" in chokepoint_status.upper():
        pill_class = "pill-amber"
        card_class = "action-card-warning"
    elif risk_cat == "LOW":
        pill_class = "pill-green"
        card_class = "action-card-success"
    else:
        pill_class = "pill-gray"
        card_class = "action-card"

    # Sleek Hero Dossier Banner
    st.markdown(f"""
    <div class="{card_class}" style="margin-top: 10px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 14px;">
            <div>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                    <span class="pill {pill_class}"><span class="pill-dot"></span> {risk_cat} RISK</span>
                    <span style="font-size: 11.5px; color: #64748B; font-weight: 700;">ID: {selected_entity_id}</span>
                    <span style="color: #CBD5E1;">|</span>
                    <span style="font-size: 12.5px; color: #475569; font-weight: 600;">Role: {role}</span>
                </div>
                <h3 style="margin: 0; font-size: 20px; font-weight: 800; color: #0A2540; letter-spacing: -0.02em;">{legal_name}</h3>
                <div style="margin-top: 8px; display: flex; gap: 10px; font-size: 12.5px; color: #475569;">
                    <span>Site: <strong>{facility_id}</strong> (Zone {facility_zone})</span>
                    <span>•</span>
                    <span>Composite Risk Score: <strong>{score} / 100</strong></span>
                    <span>•</span>
                    <span>Products Reached: <strong>{prods_reached}</strong></span>
                </div>
            </div>
            <div style="text-align: right; min-width: 160px;">
                <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: #64748B;">Revenue At Risk</div>
                <div style="font-size: 26px; font-weight: 800; color: #0A2540;">${rev_dep}M</div>
                <div style="font-size: 11px; font-weight: 600; color: #64748B;">Dependent Portfolio Base</div>
            </div>
        </div>
        <div style="margin-top: 12px; padding-top: 10px; border-top: 1px solid #E2E8F0; font-size: 13px; color: #334155;">
            <strong>Chokepoint Diagnosis:</strong> {chokepoint_status}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Clean Two-Tab Split
    d_tab1, d_tab2 = st.tabs(["Primary Evidence Filings & Disclosures", "Operational Health & Physical Site Audit"])

    with d_tab1:
        matched_docs = []
        if not df_evid.empty:
            short_name = legal_name.replace("Ltd.", "").replace("GmbH", "").replace("Inc.", "").strip()
            for _, ev_row in df_evid.iterrows():
                parties = str(ev_row.get("Title / Parties", ""))
                detail = str(ev_row.get("Evidence Detail", ""))
                ev_all = (parties + " " + detail).lower()
                
                if (selected_entity_id.lower() in ev_all) or (short_name.lower() in ev_all):
                    matched_docs.append(ev_row)

        if matched_docs:
            st.markdown(f"<div style='font-size: 12.5px; color: #64748B; margin-bottom: 10px;'>Showing <strong>{len(matched_docs)}</strong> verified regulatory instruments:</div>", unsafe_allow_html=True)
            for idx, doc in enumerate(matched_docs):
                doc_id = doc.get("Evidence ID", f"DOC-{idx+1}")
                doc_date = doc.get("Evidence Date", "Undated")
                doc_type = doc.get("Evidence Type", "Disclosure")
                doc_title = doc.get("Title / Parties", "")
                doc_detail = doc.get("Evidence Detail", "")
                doc_status = doc.get("Record Status", "Current disclosure")

                with st.expander(f"{doc_id} — {doc_title} ({doc_date})", expanded=(idx==0)):
                    c1, c2 = st.columns([1, 3])
                    with c1:
                        st.markdown(f"""
                        <div style="font-size: 12.5px; color: #475569; line-height: 1.6;">
                            <strong>Type:</strong> {doc_type}<br>
                            <strong>Status:</strong> <span class="pill pill-gray">{doc_status}</span><br>
                            <strong>Date:</strong> {doc_date}
                        </div>
                        """, unsafe_allow_html=True)
                    with c2:
                        st.markdown(f"""
                        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; padding: 12px 16px; border-radius: 6px; font-family: monospace; font-size: 12px; line-height: 1.55; color: #1E293B;">
                            {doc_detail}
                        </div>
                        """, unsafe_allow_html=True)

                    # Highlight Specific Caveats Cleanly
                    if "planning allocation" in doc_detail.lower():
                        st.markdown("<div class='tldr-box' style='margin-top: 10px; border-left: 4px solid #D97706;'><span class='tldr-tag'>CAVEAT</span> <strong>Planning Quota Only:</strong> Allocation percentage is an internal planning target, not an enforceable delivery ledger guarantee.</div>", unsafe_allow_html=True)
                    if "pilot line" in doc_detail.lower():
                        st.markdown("<div class='tldr-box' style='margin-top: 10px; border-left: 4px solid #DC2626;'><span class='tldr-tag'>CRITICAL</span> <strong>Unapproved Site:</strong> Secondary facility is an unvalidated pilot line. Volume production requires 16+ weeks of PPAP qualification.</div>", unsafe_allow_html=True)
        else:
            st.caption(f"No documentary records directly matched {selected_entity_id}.")

    with d_tab2:
        m_c1, m_c2, m_c3 = st.columns(3)
        with m_c1:
            st.metric("Current Ratio (Liquidity)", f"{curr_ratio}", help="Benchmark > 1.2. Below 1.0 indicates working capital shortfall.")
        with m_c2:
            st.metric("Net Debt / EBITDA (Leverage)", f"{net_debt}", help="Benchmark < 3.0x. Above 4.0x signals covenant default risk.")
        with m_c3:
            st.metric("3M Delivery Timeliness", f"{timeliness}%" if str(timeliness) != "nan" else "N/A", delta=f"{time_change} pp since Jan" if str(time_change) != "nan" else None)

        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
        
        # Site Flood Check
        is_z01 = (facility_zone == "Z01") or ("Z01" in str(rec.get("Registered Zone", "")))
        if is_z01:
            st.markdown(f"""
            <div class="action-card-critical">
                <span class="pill pill-red"><span class="pill-dot"></span> Active Hazard Match: Zone Z01 Flood Basin</span>
                <p style="font-size: 13px; color: #334155; margin: 6px 0 0 0; line-height: 1.5;">
                    Facility <code>{facility_id}</code> is situated directly in the East Delta flood plain identified in event <strong>EV-001</strong>.<br>
                    <strong>Mitigation Action:</strong> Demand off-site inventory count in days-of-supply cover immediately.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="action-card-success">
                <span class="pill pill-green"><span class="pill-dot"></span> Insulated: Zone {facility_zone}</span>
                <div style="font-size: 13px; color: #475569; margin-top: 4px;">Primary facility is situated outside the active flood plain.</div>
            </div>
            """, unsafe_allow_html=True)

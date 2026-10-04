"""
NovaDrive Technologies | Strategic Case Analysis & Scenario Simulation Module
Strategic case evaluation, interactive disruption simulator, and 30-60-90 day CRO action roadmap.
"""

import streamlit as st
import pandas as pd
try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

def render_case_study_view(df_bus, df_scorecard, df_crit, df_flood, df_alts):
    """
    Renders an uncluttered, action-oriented strategic case walkthrough,
    interactive what-if scenario simulator, and 30-60-90 day CRO action playbook.
    """
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
        <div>
            <h3 style="margin: 0; font-size: 16px; font-weight: 600; color: #0A2540;">Strategic Case Analysis & Disruption Simulation</h3>
            <p style="margin: 2px 0 0 0; color: #64748B; font-size: 12.5px;">
                Board-level resilience evaluation: Evidence-based forensic analysis vs. surface-level compliance.
            </p>
        </div>
        <div>
            <span class="pill pill-navy"><span class="pill-dot"></span> Board Oversight Mode</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    cs_tab1, cs_tab2, cs_tab3, cs_tab4 = st.tabs([
        "Enterprise Exposure Footprint",
        "The 4 Strategic Blindspots Disclosed",
        "Interactive Disruption Simulator",
        "CRO 30-60-90 Day Decision Playbook"
    ])

    # 1. CASE STUDY BACKGROUND & FOOTPRINT
    with cs_tab1:
        st.markdown("<div style='font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #64748B; margin-bottom: 8px;'>NovaDrive Operating Portfolio ($1,560M Turnover Base)</div>", unsafe_allow_html=True)
        
        p1_c, p2_c, p3_c = st.columns(3)
        with p1_c:
            st.markdown("""
            <div class="action-card">
                <span class="pill pill-blue"><span class="pill-dot"></span> Platform P1</span>
                <h4 style="margin: 6px 0 2px 0; font-size: 14.5px; color: #0A2540;">DriveCore Inverter</h4>
                <div style="font-size: 20px; font-weight: 700; color: #0066CC;">$624M / yr</div>
                <div style="font-size: 11.5px; color: #64748B; margin-top: 4px; line-height: 1.45;">
                    Volume: 2,000 units / week<br>
                    Footprint: Harbor Works (60%), Plateau (40%)<br>
                    Core Node: M10 Standard Power Assembly
                </div>
            </div>
            """, unsafe_allow_html=True)

        with p2_c:
            st.markdown("""
            <div class="action-card">
                <span class="pill pill-blue"><span class="pill-dot"></span> Platform P2</span>
                <h4 style="margin: 6px 0 2px 0; font-size: 14.5px; color: #0A2540;">ChargeBridge Power</h4>
                <div style="font-size: 20px; font-weight: 700; color: #0066CC;">$520M / yr</div>
                <div style="font-size: 11.5px; color: #64748B; margin-top: 4px; line-height: 1.45;">
                    Volume: 1,000 units / week<br>
                    Footprint: Harbor Works (30%), Coastal (70%)<br>
                    Core Node: M20 High-Voltage Assembly
                </div>
            </div>
            """, unsafe_allow_html=True)

        with p3_c:
            st.markdown("""
            <div class="action-card">
                <span class="pill pill-blue"><span class="pill-dot"></span> Platform P3</span>
                <h4 style="margin: 6px 0 2px 0; font-size: 14.5px; color: #0A2540;">StoreLink Storage</h4>
                <div style="font-size: 20px; font-weight: 700; color: #0066CC;">$416M / yr</div>
                <div style="font-size: 11.5px; color: #64748B; margin-top: 4px; line-height: 1.45;">
                    Volume: 800 units / week<br>
                    Footprint: Plateau Works (100%)<br>
                    Core Node: M10 Power Assembly & S10 Sensors
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="tldr-box" style="margin-top: 10px;">
            <span class="tldr-tag">CORE DILEMMA</span>
            Legacy ERP risk monitoring evaluated Tier-1 direct suppliers independently (Aster scored 52/100, Boreal scored 48/100) and reported an active dual-sourcing hedge.<br>
            Forensic multi-tier audit reveals that <strong>both are 100% owned by CommonSpan Holdings</strong>, and 100% of their SiC power dies come from a single facility (IonPeak) located in an active flood basin.
        </div>
        """, unsafe_allow_html=True)

    # 2. THE 4 STRATEGIC BLINDSPOTS REVEALED
    with cs_tab2:
        st.markdown("<div style='font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #64748B; margin-bottom: 8px;'>Four Structural Blindspots Disclosed by Primary Evidence</div>", unsafe_allow_html=True)

        b_c1, b_c2 = st.columns(2)
        with b_c1:
            st.markdown("""
            <div class="action-card-critical">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <span class="pill pill-red"><span class="pill-dot"></span> Blindspot 1</span>
                    <span style="font-size: 11px; font-weight: 600; color: #991B1B;">$1,144M Exposed</span>
                </div>
                <h4 style="margin: 4px 0 2px 0; font-size: 14px; color: #0A2540;">The Dual-Sourcing Illusion (CommonSpan)</h4>
                <p style="font-size: 12px; color: #334155; margin: 4px 0 0 0; line-height: 1.5;">
                    Aster (60%) and Boreal (40%) were assumed to be competing suppliers. Regulatory filing <code>DOC-075</code> proves they are wholly owned subsidiaries of CommonSpan Holdings under shared treasury and cross-default covenants.
                </p>
                <div style="margin-top: 6px; font-size: 11.5px; color: #7F1D1D;">
                    <strong>CRO Verdict:</strong> Zero dual-sourcing protection exists in reality.
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="action-card-critical">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <span class="pill pill-red"><span class="pill-dot"></span> Blindspot 2</span>
                    <span style="font-size: 11px; font-weight: 600; color: #991B1B;">$1,560M Exposed</span>
                </div>
                <h4 style="margin: 4px 0 2px 0; font-size: 14px; color: #0A2540;">The Upstream Chokepoint Triad</h4>
                <p style="font-size: 12px; color: #334155; margin: 4px 0 0 0; line-height: 1.5;">
                    Three sub-tier suppliers control 100% of NovaDrive's production line: <strong>IonPeak</strong> (sole SiC die source), <strong>Jade</strong> (sole bare PCB maker), and <strong>Meridian</strong> (sole BOPP capacitor film maker under debt watch <code>EV-003</code>).
                </p>
                <div style="margin-top: 6px; font-size: 11.5px; color: #7F1D1D;">
                    <strong>CRO Verdict:</strong> Single points of failure sit completely invisible to Tier-1 procurement.
                </div>
            </div>
            """, unsafe_allow_html=True)

        with b_c2:
            st.markdown("""
            <div class="action-card-warning">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <span class="pill pill-amber"><span class="pill-dot"></span> Blindspot 3</span>
                    <span style="font-size: 11px; font-weight: 600; color: #B45309;">5 Clustered Sites</span>
                </div>
                <h4 style="margin: 4px 0 2px 0; font-size: 14px; color: #0A2540;">Zone Z01 Flood Plain Concentration</h4>
                <p style="font-size: 12px; color: #334155; margin: 4px 0 0 0; line-height: 1.5;">
                    Tier-1 facilities are geographically dispersed, but Tier-2 and Tier-3 suppliers (IonPeak, Jade, Orion, Umber, Verdant) are all situated inside the East Delta 100-year flood basin (Zone Z01, Event <code>EV-001</code>).
                </p>
                <div style="margin-top: 6px; font-size: 11.5px; color: #92400E;">
                    <strong>CRO Verdict:</strong> A regional localized flood event halts 100% of NovaDrive global revenue.
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="action-card-warning">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <span class="pill pill-amber"><span class="pill-dot"></span> Blindspot 4</span>
                    <span style="font-size: 11px; font-weight: 600; color: #B45309;">12-16 Weeks Runway</span>
                </div>
                <h4 style="margin: 4px 0 2px 0; font-size: 14px; color: #0A2540;">The Alternate Qualification Lead-Time Trap</h4>
                <p style="font-size: 12px; color: #334155; margin: 4px 0 0 0; line-height: 1.5;">
                    Management believed volume could quickly pivot to market alternates (Semikron Danfoss, Vincotech). High-power automotive inverters require thermal cycling, dyno qualification, and safety certification taking 12 to 16 weeks minimum.
                </p>
                <div style="margin-top: 6px; font-size: 11.5px; color: #92400E;">
                    <strong>CRO Verdict:</strong> Reactive switching during an outage is impossible; warm qualification is mandatory.
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 3. INTERACTIVE WHAT-IF SCENARIO STRESS SIMULATOR
    with cs_tab3:
        st.markdown("<div style='font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #64748B; margin-bottom: 8px;'>Supply Chain Stress-Testing Simulator</div>", unsafe_allow_html=True)

        sim_col1, sim_col2 = st.columns([1, 2])
        with sim_col1:
            scenario = st.selectbox(
                "Disruption Scenario:",
                [
                    "Scenario 1: Zone Z01 100-Year Flood Outage (8-Week Full Halt)",
                    "Scenario 2: Meridian Dielectrics Debt Covenant Default (EV-003)",
                    "Scenario 3: CommonSpan Holdings Financial Restructuring",
                    "Scenario 4: Dual Disruption (Z01 Flood + CommonSpan Freeze)"
                ]
            )

            buffer_days = st.slider("Finished Goods Buffer Inventory (Days):", 5, 45, 14, step=5)
            tier1_buffer = st.slider("Tier-1 Sub-Assembly Buffer (Days):", 5, 30, 10, step=5)

        with sim_col2:
            if "Scenario 1" in scenario:
                disrupted_nodes = "IonPeak, Jade, Orion, Umber, Verdant (Zone Z01)"
                total_rev_impact = 1560
                plants_down = ["Harbor Works (100% halted)", "Plateau Works (100% halted)", "Coastal Works (100% halted)"]
                gross_weekly_loss = 30.0
                runway_days = buffer_days + tier1_buffer
                net_loss_weeks = max(0, 8 - (runway_days / 7.0))
                net_financial_loss = round(net_loss_weeks * gross_weekly_loss, 1)

            elif "Scenario 2" in scenario:
                disrupted_nodes = "Meridian Dielectrics (Tier-3 BOPP Film)"
                total_rev_impact = 624
                plants_down = ["Harbor Works (P1 line)", "Plateau Works (P1 line)"]
                gross_weekly_loss = 12.0
                runway_days = buffer_days + tier1_buffer + 14
                net_loss_weeks = max(0, 12 - (runway_days / 7.0))
                net_financial_loss = round(net_loss_weeks * gross_weekly_loss, 1)

            elif "Scenario 3" in scenario:
                disrupted_nodes = "Aster Power & Boreal Power (CommonSpan)"
                total_rev_impact = 1144
                plants_down = ["Harbor Works (100% halted)", "Plateau Works (60% halted)", "Coastal Works (70% halted)"]
                gross_weekly_loss = 22.0
                runway_days = buffer_days
                net_loss_weeks = max(0, 6 - (runway_days / 7.0))
                net_financial_loss = round(net_loss_weeks * gross_weekly_loss, 1)

            else:
                disrupted_nodes = "All Core Power & Inverter Tiers"
                total_rev_impact = 1560
                plants_down = ["Harbor Works (Halted)", "Plateau Works (Halted)", "Coastal Works (Halted)"]
                gross_weekly_loss = 30.0
                runway_days = buffer_days
                net_loss_weeks = max(0, 10 - (runway_days / 7.0))
                net_financial_loss = round(net_loss_weeks * gross_weekly_loss, 1)

            # Impact Metrics
            s_m1, s_m2, s_m3 = st.columns(3)
            s_m1.metric("Revenue Exposed", f"${total_rev_impact}M", "Annual Base")
            s_m2.metric("Runway Until Stoppage", f"{runway_days} Days", f"{round(runway_days/7, 1)} Weeks Cover")
            s_m3.metric("Projected Net Revenue Loss", f"${net_financial_loss}M", f"{round(net_loss_weeks, 1)} Weeks Lost", delta_color="inverse")

            st.markdown(f"""
            <div style="font-size: 11.5px; color: #334155; margin-top: 6px;">
                <strong>Disrupted Nodes:</strong> <code>{disrupted_nodes}</code> | 
                <strong>Sites Affected:</strong> {', '.join(plants_down)}
            </div>
            """, unsafe_allow_html=True)

            if HAS_PLOTLY:
                weeks = [f"W{i}" for i in range(1, 13)]
                loss_data = [gross_weekly_loss if i*7 > runway_days else 0 for i in range(1, 13)]
                
                fig_sim = go.Figure()
                fig_sim.add_trace(go.Bar(x=weeks, y=loss_data, marker_color="#DC2626"))
                fig_sim.update_layout(
                    title=dict(
                        text="<b>Weekly Net Revenue Loss Profile ($M)</b>",
                        font=dict(size=12, color="#0A2540", family="Inter, sans-serif")
                    ),
                    height=180,
                    margin=dict(l=15, r=15, t=25, b=15),
                    yaxis_title="USD ($M)",
                    plot_bgcolor="#FFFFFF",
                    paper_bgcolor="#FFFFFF",
                    font=dict(family="Inter, sans-serif", size=10, color="#475569")
                )
                st.plotly_chart(fig_sim, use_container_width=True)

    # 4. CRO 30-60-90 DAY DECISION PLAYBOOK
    with cs_tab4:
        st.markdown("<div style='font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #64748B; margin-bottom: 8px;'>Chief Risk Officer (CRO) Strategic Action Roadmap</div>", unsafe_allow_html=True)

        pb1, pb2, pb3 = st.columns(3)
        with pb1:
            st.markdown("""
            <div class="action-card" style="border-top: 3px solid #D97706; height: 100%;">
                <span class="pill pill-amber"><span class="pill-dot"></span> Phase 1: Day 1 - 30</span>
                <h4 style="margin: 6px 0 4px 0; font-size: 13.5px; color: #0A2540;">Containment & Verification</h4>
                <ul style="font-size: 12px; color: #334155; padding-left: 16px; margin: 0; line-height: 1.5;">
                    <li><strong>Z01 Site Defense Audit:</strong> Dispatch civil engineers to IonPeak SITE-074 and Jade SITE-081 to inspect dykes and backup power.</li>
                    <li><strong>CommonSpan Ring-Fencing:</strong> Require CommonSpan Holdings to provide audited ring-fenced bank guarantees for Aster and Boreal.</li>
                    <li><strong>Forward Buffer Expansion:</strong> Pull safety stock into regional hubs to increase buffer from 14 to 30 days for M10 & M20.</li>
                    <li><strong>Meridian Audit (EV-003):</strong> Audit film capacitor stock cover at Delta Capacitor Works (target: 60 days).</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with pb2:
            st.markdown("""
            <div class="action-card" style="border-top: 3px solid #0066CC; height: 100%;">
                <span class="pill pill-blue"><span class="pill-dot"></span> Phase 2: Day 31 - 60</span>
                <h4 style="margin: 6px 0 4px 0; font-size: 13.5px; color: #0A2540;">Alternate Qualification</h4>
                <ul style="font-size: 12px; color: #334155; padding-left: 16px; margin: 0; line-height: 1.5;">
                    <li><strong>Procure Sample Lots:</strong> Order qualification lots from Semikron Danfoss and Vincotech for M10/M20 dyno tests.</li>
                    <li><strong>Independent Die Route:</strong> Require module alternates to disclose third-party SiC wafer and die supply lines.</li>
                    <li><strong>Qualify PCB Second Source:</strong> Initiate prototype qualification with an independent PCB supplier outside flood zone Z01 for C10 & B10.</li>
                    <li><strong>BOPP Dual-Sourcing:</strong> Authorize Delta Capacitor Works to approve secondary dielectric film sources.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with pb3:
            st.markdown("""
            <div class="action-card" style="border-top: 3px solid #16A34A; height: 100%;">
                <span class="pill pill-green"><span class="pill-dot"></span> Phase 3: Day 61 - 90</span>
                <h4 style="margin: 6px 0 4px 0; font-size: 13.5px; color: #0A2540;">Structural Decoupling</h4>
                <ul style="font-size: 12px; color: #334155; padding-left: 16px; margin: 0; line-height: 1.5;">
                    <li><strong>Rebalance Sourcing:</strong> Re-allocate M10 volume: 50% Aster, 30% New Independent Qualified Source, 20% Boreal.</li>
                    <li><strong>Die Supply Reservation:</strong> Establish a direct consignment die contract or wafer reservation with an external foundry.</li>
                    <li><strong>Automated Evidence Feed:</strong> Formalize automated ingestion of regulatory filings and shipping records into this platform.</li>
                    <li><strong>Board Presentation:</strong> Present final multi-tier resilience audit to the Audit & Risk Committee.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

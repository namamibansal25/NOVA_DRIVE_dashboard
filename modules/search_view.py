"""
NovaDrive Technologies | Supplier Qualification Directory & MCDA Engine
Multi-criteria decision analysis (MCDA), dynamic weight tuning, and upstream dependency checking.
"""

import streamlit as st
import pandas as pd
try:
    import plotly.graph_objects as go
    import plotly.express as px
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

def render_alternate_search(df_alts, df_comp, df_rules=None):
    """
    Renders an uncluttered, action-oriented supplier qualification directory,
    executive 2x2 decision quadrant, and upstream dependency audit.
    """
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <div>
            <h3 style="margin: 0; font-size: 18px; font-weight: 700; color: #0A2540;">Supplier Qualification Directory & Sourcing Decision Engine</h3>
            <p style="margin: 3px 0 0 0; color: #64748B; font-size: 13px;">
                Multi-criteria decision analysis (MCDA) screening alternates across technical fit, re-qualification runway, and upstream die independence.
            </p>
        </div>
        <div>
            <span class="pill pill-blue"><span class="pill-dot"></span> MCDA Decision Engine</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if df_alts.empty:
        st.warning("No alternate supplier qualification data loaded.")
        return

    # Slicing Filters
    s_col1, s_col2, s_col3 = st.columns([2, 1, 1])
    
    comp_list = ["All Components & Chokepoints"] + sorted(df_alts["Component"].dropna().unique().tolist())
    selected_comp = s_col1.selectbox("Target Component / Upstream Node:", comp_list, index=0)
    
    band_list = ["All Bands"] + sorted(df_alts["Screening band"].dropna().unique().tolist())
    selected_band = s_col2.selectbox("Fitment Band Filter:", band_list, index=0)
    
    upstream_filter = s_col3.checkbox("Filter: Breaks Upstream Trap", value=False, help="Filter for candidates that decouple from IonPeak / Jade")

    # Dynamic Weight Slider Customization
    with st.expander("Configure MCDA Weighting Strategic Posture", expanded=False):
        st.caption("Adjust weighting priorities (e.g. accelerated qualification sprint vs. conservative design-in).")
        w_c1, w_c2, w_c3 = st.columns(3)
        w_tech = w_c1.slider("Technical Capability (%):", 10, 50, 30, step=5)
        w_app = w_c2.slider("Application Relevance (%):", 10, 40, 20, step=5)
        w_scale = w_c3.slider("Scale & Footprint (%):", 5, 30, 15, step=5)
        
        w_c4, w_c5, w_c6 = st.columns(3)
        w_qual = w_c4.slider("Quality & Qualification Readiness (%):", 5, 30, 15, step=5)
        w_sub = w_c5.slider("Design-In / Substitution Ease (%):", 5, 25, 10, step=5)
        w_comm = w_c6.slider("Commercial Resilience (%):", 5, 25, 10, step=5)

        total_weight = w_tech + w_app + w_scale + w_qual + w_sub + w_comm

    # Filter candidates
    working_df = df_alts.copy()
    if selected_comp != "All Components & Chokepoints":
        working_df = working_df[working_df["Component"] == selected_comp]
    if selected_band != "All Bands":
        working_df = working_df[working_df["Screening band"] == selected_band]

    if upstream_filter and "Addresses shared upstream dependency?" in working_df.columns:
        working_df = working_df[working_df["Addresses shared upstream dependency?"].str.lower().str.contains("yes|breaks|independent", na=False)]

    # Dynamic Recalculation of Weighted Scores
    norm_w = {
        "Technical capability (30%)": w_tech / total_weight,
        "Application relevance (20%)": w_app / total_weight,
        "Scale / footprint (15%)": w_scale / total_weight,
        "Quality / qualification readiness (15%)": w_qual / total_weight,
        "Design-in / substitution ease (10%)": w_sub / total_weight,
        "Commercial / supply resilience (10%)": w_comm / total_weight,
    }

    def calc_dyn_score(row):
        score = 0.0
        for col_name, w in norm_w.items():
            val = pd.to_numeric(row.get(col_name, 0), errors="coerce")
            if pd.isna(val):
                val = 2.0
            score += float(val) * w
        return round(score, 2)

    working_df["Weighted Score (0-5)"] = working_df.apply(calc_dyn_score, axis=1)
    working_df = working_df.sort_values(by="Weighted Score (0-5)", ascending=False)

    # Synthetic estimated lead time for scatter quadrant if not in data
    # High fit candidates usually need 12-16 weeks for PPAP automotive qualification
    def estimate_lead_weeks(row):
        band = str(row.get("Screening band", "")).lower()
        if "strong" in band:
            return 14.0
        elif "qualified" in band:
            return 12.0
        elif "partial" in band:
            return 16.0
        else:
            return 18.0

    working_df["Lead Time (Weeks)"] = working_df.apply(estimate_lead_weeks, axis=1)

    # EXECUTIVE INFOGRAPHIC: Strategic Sourcing Decision Matrix (Fit vs. Lead Time Quadrant)
    if HAS_PLOTLY and not working_df.empty:
        chart_df = working_df.head(10).copy()
        
        fig_quad = px.scatter(
            chart_df,
            x="Lead Time (Weeks)",
            y="Weighted Score (0-5)",
            color="Screening band",
            size=[24]*len(chart_df),
            text="Candidate",
            color_discrete_map={
                "Strong candidate": "#059669",
                "Qualified lead": "#0066CC",
                "Partial / uncertain fit": "#D97706",
                "Weak fit": "#DC2626"
            },
            hover_data={
                "Candidate": True,
                "Component": True,
                "Weighted Score (0-5)": True,
                "Lead Time (Weeks)": True,
                "Addresses shared upstream dependency?": True
            }
        )

        fig_quad.update_traces(
            textposition="top center",
            textfont=dict(family="Plus Jakarta Sans", size=11, color="#0A2540")
        )

        # Strategic Quadrant Shading & Annotations
        fig_quad.add_shape(
            type="rect",
            x0=10, x1=16.5, y0=3.2, y1=5.2,
            fillcolor="rgba(0, 102, 204, 0.05)",
            line=dict(color="#BAE6FD", width=1, dash="dot"),
            layer="below"
        )
        fig_quad.add_annotation(
            x=13.2, y=4.9,
            text="<b>OPTIMAL SPRINT ZONE: High Fit / 12-16 Wk Qualification Runway</b>",
            showarrow=False,
            font=dict(family="Plus Jakarta Sans", size=10.5, color="#0066CC")
        )

        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 10px; padding: 12px 18px 4px 18px; margin-top: 10px; margin-bottom: 2px;">
            <div style="font-size: 14.5px; font-weight: 800; color: #0A2540;">Strategic Sourcing Decision Matrix: Fitment Score vs. Qualification Runway</div>
            <div style="font-size: 12px; color: #64748B;">Quadrant mapping of market alternates evaluating engineering fit against required PPAP dyno test lead time.</div>
        </div>
        """, unsafe_allow_html=True)

        fig_quad.update_layout(
            title=None,
            xaxis=dict(
                title="Estimated Re-qualification Runway (Weeks to PPAP)",
                range=[8, 20],
                showgrid=True,
                gridcolor="#F1F5F9"
            ),
            yaxis=dict(
                title="MCDA Fitment Score (0 to 5.0)",
                range=[1.5, 5.2],
                showgrid=True,
                gridcolor="#F1F5F9"
            ),
            height=320,
            margin=dict(l=15, r=15, t=10, b=25),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            font=dict(family="Plus Jakarta Sans", size=11, color="#334155"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig_quad, use_container_width=True)

    # Clean Candidates Grid
    with st.expander(f"Inspect Candidate Qualification Grid ({len(working_df)} Alternates)", expanded=False):
        disp_cols = [
            "Candidate", "Component", "Screening band", "Weighted Score (0-5)",
            "Evidence confidence", "Node replaced / tier", "Decision status",
            "Addresses shared upstream dependency?"
        ]
        avail_cols = [c for c in disp_cols if c in working_df.columns]
        st.dataframe(working_df[avail_cols], use_container_width=True)

    # Detailed Candidate Technical Dossier
    st.markdown("<div style='font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #64748B; margin: 20px 0 10px 0;'>Candidate Technical Dossier & Upstream Bottleneck Audit</div>", unsafe_allow_html=True)

    candidate_names = working_df["Candidate"].dropna().unique().tolist()
    if candidate_names:
        selected_cand = st.selectbox("Select Candidate for Deep Technical Audit:", candidate_names)
        cand_match = working_df[working_df["Candidate"] == selected_cand]
        if not cand_match.empty:
            cand = cand_match.iloc[0]
            
            c_name = cand.get("Candidate", "Unknown")
            c_comp = cand.get("Component", "")
            c_band = cand.get("Screening band", "Unrated")
            c_score = cand.get("Weighted Score (0-5)", "N/A")
            c_ev_conf = cand.get("Evidence confidence", "Medium")
            c_status = cand.get("Decision status", "Screen only")
            c_assess = cand.get("Evidence-based assessment", "")
            c_gaps = cand.get("Main verification gaps", "")
            c_url = cand.get("Public source URL", "")
            c_summary = cand.get("Public Evidence Summary", "")
            c_upstream = cand.get("Addresses shared upstream dependency?", "Unverified")

            # Candidate Top Summary Cards
            u_col1, u_col2 = st.columns([2, 1])
            with u_col1:
                # Check Upstream dependency trap
                is_trap = "no" in str(c_upstream).lower() or "same" in str(c_upstream).lower() or "die-dependency" in str(c_upstream).lower()
                if is_trap:
                    st.markdown(f"""
                    <div class="action-card-critical">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div>
                                <span class="pill pill-red"><span class="pill-dot"></span> Upstream Dependency Trap</span>
                                <h4 style="margin: 5px 0 0 0; font-size: 15px; font-weight: 700; color: #0A2540;">{c_name} — {c_comp}</h4>
                            </div>
                            <span class="pill pill-gray">Score: {c_score}/5.0</span>
                        </div>
                        <p style="font-size: 12.5px; color: #334155; margin: 8px 0 0 0; line-height: 1.55;">
                            {c_upstream}<br>
                            <strong>CRO Alert:</strong> Sourcing this alternate as a Tier-1 module assembler does <strong>not</strong> mitigate supply risk if IonPeak suffers a flood outage, because this alternate also buys third-party dies!
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="action-card-success">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div>
                                <span class="pill pill-green"><span class="pill-dot"></span> Upstream Decoupling Confirmed</span>
                                <h4 style="margin: 5px 0 0 0; font-size: 15px; font-weight: 700; color: #0A2540;">{c_name} — {c_comp}</h4>
                            </div>
                            <span class="pill pill-green">Score: {c_score}/5.0</span>
                        </div>
                        <p style="font-size: 12.5px; color: #334155; margin: 8px 0 0 0; line-height: 1.55;">
                            {c_upstream}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

            with u_col2:
                st.metric("Qualification Runway", "12 - 16 Weeks", "Active Sprint Required")
                st.caption("Standard bench build, dyno load testing, and PPAP approval cycle.")

            # Evidence & Gaps
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                st.markdown("""
                <div class="action-card">
                    <span class="pill pill-blue"><span class="pill-dot"></span> Primary Technical Evidence</span>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                    <div style="font-size: 12.5px; color: #1E293B; line-height: 1.55; margin-top: 8px;">
                        <strong>Technical Summary:</strong><br>{c_summary}<br><br>
                        <strong>Engineering Assessment:</strong><br>{c_assess}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if c_url and str(c_url).startswith("http"):
                    st.markdown(f"<div style='font-size: 12px; margin-top: 4px;'><a href='{c_url}' target='_blank' style='color: #0066CC; text-decoration: none; font-weight: 600;'>View Manufacturer Technical Documentation -></a></div>", unsafe_allow_html=True)

            with t_col2:
                st.markdown(f"""
                <div class="action-card-warning">
                    <span class="pill pill-amber"><span class="pill-dot"></span> Actionable Verification Gaps</span>
                    <div style="font-size: 12.5px; color: #92400E; line-height: 1.55; margin-top: 8px;">
                        {c_gaps}
                    </div>
                    <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid #FEF3C7; font-size: 12px; color: #92400E; font-weight: 600;">
                        Next Step: Issue sample PO and schedule supplier quality engineering on-site audit.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Radar Chart
            if HAS_PLOTLY:
                categories = [
                    "Technical Capability", "Application Relevance", "Scale & Footprint",
                    "Quality Readiness", "Substitution Ease", "Commercial Resilience"
                ]
                values = [
                    pd.to_numeric(cand.get("Technical capability (30%)", 2), errors="coerce") or 2,
                    pd.to_numeric(cand.get("Application relevance (20%)", 2), errors="coerce") or 2,
                    pd.to_numeric(cand.get("Scale / footprint (15%)", 2), errors="coerce") or 2,
                    pd.to_numeric(cand.get("Quality / qualification readiness (15%)", 2), errors="coerce") or 2,
                    pd.to_numeric(cand.get("Design-in / substitution ease (10%)", 2), errors="coerce") or 2,
                    pd.to_numeric(cand.get("Commercial / supply resilience (10%)", 2), errors="coerce") or 2,
                ]
                
                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(
                    r=values + [values[0]],
                    theta=categories + [categories[0]],
                    fill='toself',
                    fillcolor='rgba(0, 102, 204, 0.12)',
                    line=dict(color='#0066CC', width=2),
                    name=c_name
                ))
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 5], gridcolor="#F1F5F9"),
                        angularaxis=dict(gridcolor="#F1F5F9")
                    ),
                    title=dict(
                        text=f"<b>MCDA Fitment Polygon: {c_name} (Scale 1 to 5)</b>",
                        font=dict(size=13, color="#0A2540", family="Plus Jakarta Sans")
                    ),
                    height=280,
                    margin=dict(l=20, r=20, t=40, b=20),
                    paper_bgcolor="#FFFFFF",
                    font=dict(family="Plus Jakarta Sans", size=10.5, color="#475569")
                )
                st.plotly_chart(fig_radar, use_container_width=True)

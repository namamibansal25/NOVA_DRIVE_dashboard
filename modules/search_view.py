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
    multi-criteria decision analysis (MCDA), and upstream dependency audit.
    """
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
        <div>
            <h3 style="margin: 0; font-size: 16px; font-weight: 600; color: #0A2540;">Supplier Qualification Directory & MCDA Engine</h3>
            <p style="margin: 2px 0 0 0; color: #64748B; font-size: 12.5px;">
                Screen market alternates for direct assembly tiers and critical upstream nodes.
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
    with st.expander("MCDA Criteria Weight Configuration", expanded=False):
        st.caption("Adjust criteria weighting based on strategic posture (e.g. accelerated qualification sprint vs. conservative design-in).")
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

    # Candidate Comparison Visual
    if HAS_PLOTLY and not working_df.empty:
        chart_df = working_df.head(8).copy()
        fig = px.bar(
            chart_df,
            x="Weighted Score (0-5)",
            y="Candidate",
            color="Screening band",
            orientation="h",
            text="Weighted Score (0-5)",
            color_discrete_map={
                "Strong candidate": "#065F46",
                "Qualified lead": "#0066CC",
                "Partial / uncertain fit": "#B45309",
                "Weak fit": "#DC2626"
            },
            category_orders={"Candidate": chart_df["Candidate"].tolist()[::-1]}
        )
        fig.update_layout(
            title=dict(
                text="<b>Top Sourcing Candidates by Weighted Fitment Score (0 - 5.0)</b>",
                font=dict(size=12.5, color="#0A2540", family="Inter, sans-serif")
            ),
            font=dict(family="Inter, sans-serif", color="#475569", size=11),
            height=300,
            margin=dict(l=15, r=15, t=35, b=15),
            xaxis=dict(range=[0, 5.2], showgrid=True, gridcolor="#F1F5F9"),
            yaxis=dict(showgrid=False),
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Clean Candidates Grid
    with st.expander("Candidate Qualification Grid (Summary Table)", expanded=False):
        disp_cols = [
            "Candidate", "Component", "Screening band", "Weighted Score (0-5)",
            "Evidence confidence", "Node replaced / tier", "Decision status",
            "Addresses shared upstream dependency?"
        ]
        avail_cols = [c for c in disp_cols if c in working_df.columns]
        st.dataframe(working_df[avail_cols], use_container_width=True)

    # Detailed Candidate Technical Dossier
    st.markdown("<div style='font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #64748B; margin: 16px 0 8px 0;'>Candidate Technical Dossier & Upstream Bottleneck Audit</div>", unsafe_allow_html=True)

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
                                <h4 style="margin: 4px 0 0 0; font-size: 14.5px; color: #0A2540;">{c_name} — {c_comp}</h4>
                            </div>
                            <span class="pill pill-gray">Score: {c_score}/5.0</span>
                        </div>
                        <p style="font-size: 12px; color: #334155; margin: 8px 0 0 0; line-height: 1.5;">
                            {c_upstream}<br>
                            <strong>CRO Alert:</strong> Sourcing this alternate as a Tier-1 module assembler does <strong>not</strong> mitigate supply risk if IonPeak suffers a flood outage.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="action-card-success">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div>
                                <span class="pill pill-green"><span class="pill-dot"></span> Upstream Decoupling Confirmed</span>
                                <h4 style="margin: 4px 0 0 0; font-size: 14.5px; color: #0A2540;">{c_name} — {c_comp}</h4>
                            </div>
                            <span class="pill pill-green">Score: {c_score}/5.0</span>
                        </div>
                        <p style="font-size: 12px; color: #334155; margin: 8px 0 0 0; line-height: 1.5;">
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
                    <div style="font-size: 12px; color: #1E293B; line-height: 1.5; margin-top: 6px;">
                        <strong>Technical Summary:</strong><br>{c_summary}<br><br>
                        <strong>Engineering Assessment:</strong><br>{c_assess}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if c_url and str(c_url).startswith("http"):
                    st.markdown(f"<div style='font-size: 11.5px; margin-top: 4px;'><a href='{c_url}' target='_blank' style='color: #0066CC; text-decoration: none;'>View Manufacturer Technical Documentation -></a></div>", unsafe_allow_html=True)

            with t_col2:
                st.markdown(f"""
                <div class="action-card-warning">
                    <span class="pill pill-amber"><span class="pill-dot"></span> Actionable Verification Gaps</span>
                    <div style="font-size: 12px; color: #92400E; line-height: 1.5; margin-top: 6px;">
                        {c_gaps}
                    </div>
                    <div style="margin-top: 8px; padding-top: 6px; border-top: 1px solid #FEF3C7; font-size: 11.5px; color: #92400E;">
                        <strong>Next Step:</strong> Issue sample PO and schedule supplier quality engineering on-site audit.
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
                    line=dict(color='#0066CC', width=1.5),
                    name=c_name
                ))
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 5], gridcolor="#F1F5F9"),
                        angularaxis=dict(gridcolor="#F1F5F9")
                    ),
                    title=dict(
                        text=f"<b>MCDA Fitment Polygon: {c_name} (Scale 1 to 5)</b>",
                        font=dict(size=12, color="#0A2540", family="Inter, sans-serif")
                    ),
                    height=260,
                    margin=dict(l=15, r=15, t=35, b=15),
                    paper_bgcolor="#FFFFFF",
                    font=dict(family="Inter, sans-serif", size=10, color="#475569")
                )
                st.plotly_chart(fig_radar, use_container_width=True)

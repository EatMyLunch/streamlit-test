from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from app.services.transformers import melt_lagging


def chart_style(fig, title: str) -> None:
    fig.update_layout(
        title=title,
        height=330,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.04)",
        margin=dict(l=8, r=8, t=52, b=8),
        legend_title=None,
        font=dict(color="#d9e9fb", family="Segoe UI, Calibri, sans-serif"),
        title_font=dict(size=16, color="#eaf4ff"),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(185, 202, 224, 0.2)")


def render_hero(period: str, area_scope: str) -> None:
    st.markdown(
        f"""
        <div class="hero">
            <h1>ULTIMATE OHS Dashboard Mockup</h1>
            <p class="muted" style="margin-top:8px; margin-bottom:0; max-width:920px;">
                Mock data for executive preview, built from the OHS sheet structure: Lagging, Leading, Incidents,
                Findings PICA, and Monitoring Areas. Filters are currently set to <b>{period}</b> and
                area scope <b>{area_scope}</b>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<p class='muted' style='margin-top:8px;'>Generated at {datetime.now().strftime('%d %b %Y %H:%M:%S')}</p>",
        unsafe_allow_html=True,
    )


def render_overview(data: dict[str, pd.DataFrame], period: str) -> None:
    lagging = data["Lagging_Indicators"]
    incidents = data["Incidents"]
    findings = data["Findings_PICA"]
    leading = data["Leading_Indicators"]

    dcm_col = f"DCM_{period}"
    contractor_col = f"Contractor_{period}"

    dcm_total = int(lagging[dcm_col].sum())
    contractor_total = int(lagging[contractor_col].sum())
    open_incidents = int((incidents["Status"] == "Open").sum())
    total_incidents = int(len(incidents))
    open_rate = (open_incidents / total_incidents * 100) if total_incidents else 0
    open_findings = int(findings["Open_Count"].sum())
    close_findings = int(findings["Close_Count"].sum())
    closure_ratio = (close_findings / max(open_findings, 1)) * 100

    if not incidents.empty:
        latest_incident = incidents.sort_values("Date", ascending=False).iloc[0]
        headline = (
            f"Latest event: {latest_incident['Type']} at {latest_incident['Location']} "
            f"({latest_incident['Severity']} severity)."
        )
    else:
        headline = "No incidents recorded in the current filter."

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
            <div class="glass">
                <p class="kpi-title">DCM {period}</p>
                <p class="kpi-value">{dcm_total}</p>
                <p class="kpi-delta">Lagging total</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class="glass">
                <p class="kpi-title">Contractor {period}</p>
                <p class="kpi-value">{contractor_total}</p>
                <p class="kpi-delta">Lagging total</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
            <div class="glass">
                <p class="kpi-title">Open Incidents</p>
                <p class="kpi-value">{open_incidents}</p>
                <p class="kpi-delta">{open_rate:.1f}% of all cases</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"""
            <div class="glass">
                <p class="kpi-title">Open Findings</p>
                <p class="kpi-value">{open_findings}</p>
                <p class="kpi-delta">Closure velocity {closure_ratio:.0f}%</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="insight-band">
            <p class="insight-title">Operational Pulse</p>
            <p class="insight-text">{headline}</p>
            <div class="pill-row">
                <span class="pill">Total incidents: {total_incidents}</span>
                <span class="pill">Findings closed: {close_findings}</span>
                <span class="pill">Open findings: {open_findings}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-title'>Safety Snapshot</div>", unsafe_allow_html=True)
    left, right = st.columns(2)

    with left:
        lagging_period = pd.DataFrame(
            {
                "Metric": lagging["Metric"],
                "DCM": lagging[dcm_col],
                "Contractor": lagging[contractor_col],
            }
        ).melt(id_vars="Metric", var_name="Group", value_name="Count")
        fig_lag = px.bar(
            lagging_period,
            x="Metric",
            y="Count",
            color="Group",
            barmode="group",
            color_discrete_sequence=["#5bc0eb", "#9fd8f3"],
        )
        chart_style(fig_lag, f"Lagging Comparison ({period})")
        st.plotly_chart(fig_lag, use_container_width=True)

    with right:
        if not incidents.empty:
            fig_type = px.pie(
                incidents,
                names="Type",
                color_discrete_sequence=["#5bc0eb", "#8ecae6", "#91c4f2", "#b7d8f7", "#d8ecff", "#7aa8d8"],
                hole=0.48,
            )
            fig_type.update_layout(
                title="Incident Type Composition",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#d9e9fb"),
                legend_title=None,
            )
            st.plotly_chart(fig_type, use_container_width=True)
        else:
            st.info("No incident data to visualize for the selected filters.")

    st.markdown("<div class='section-title'>Operational Signals</div>", unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)

    with s1:
        if not incidents.empty:
            trend = incidents.groupby("Date", as_index=False).size().rename(columns={"size": "Incidents"})
            fig_trend = px.area(
                trend,
                x="Date",
                y="Incidents",
                line_shape="spline",
                color_discrete_sequence=["#5bc0eb"],
            )
            chart_style(fig_trend, "Incident Trend by Day")
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("No trend data available.")

    with s2:
        if not incidents.empty and "Severity" in incidents.columns:
            sev = incidents.groupby(["Type", "Severity"], as_index=False).size().rename(columns={"size": "Count"})
            sev["Severity"] = pd.Categorical(sev["Severity"], categories=["Low", "Medium", "High"], ordered=True)
            sev = sev.sort_values(["Type", "Severity"])
            fig_sev = px.bar(
                sev,
                x="Type",
                y="Count",
                color="Severity",
                barmode="stack",
                color_discrete_map={"Low": "#9fd8f3", "Medium": "#5bc0eb", "High": "#ff7f50"},
            )
            chart_style(fig_sev, "Severity Profile by Type")
            st.plotly_chart(fig_sev, use_container_width=True)
        else:
            st.info("Severity data is not available.")

    with s3:
        leading_focus = leading[["Activity", period]].sort_values(period, ascending=False).head(6)
        fig_lead = px.bar(
            leading_focus,
            x=period,
            y="Activity",
            orientation="h",
            color_discrete_sequence=["#8ecae6"],
        )
        chart_style(fig_lead, f"Top Leading Activities ({period})")
        st.plotly_chart(fig_lead, use_container_width=True)

    st.markdown("<div class='section-title'>Findings and Exposure</div>", unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1:
        findings_long = findings.melt(
            id_vars="Location",
            value_vars=["Open_Count", "Close_Count"],
            var_name="Status",
            value_name="Count",
        )
        fig_findings = px.bar(
            findings_long,
            x="Location",
            y="Count",
            color="Status",
            barmode="group",
            color_discrete_map={"Open_Count": "#91c4f2", "Close_Count": "#5bc0eb"},
        )
        chart_style(fig_findings, "Findings Load by Location")
        st.plotly_chart(fig_findings, use_container_width=True)

    with b2:
        fig_cre = px.scatter(
            findings,
            x="Open_Count",
            y="CRE",
            size="Close_Count",
            color="Location",
            size_max=42,
        )
        chart_style(fig_cre, "CRE Exposure vs Open Findings")
        st.plotly_chart(fig_cre, use_container_width=True)


def render_lagging(df: pd.DataFrame) -> None:
    st.markdown("<div class='section-title'>Lagging Indicators</div>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig_dcm = px.bar(
            melt_lagging(df, "DCM"),
            x="Metric",
            y="Count",
            color="Period",
            barmode="group",
            color_discrete_sequence=["#5bc0eb", "#8ecae6", "#9fd8f3"],
        )
        chart_style(fig_dcm, "DCM YTD/MTD/WTD")
        st.plotly_chart(fig_dcm, use_container_width=True)

    with c2:
        fig_ctr = px.bar(
            melt_lagging(df, "Contractor"),
            x="Metric",
            y="Count",
            color="Period",
            barmode="group",
            color_discrete_sequence=["#5bc0eb", "#8ecae6", "#9fd8f3"],
        )
        chart_style(fig_ctr, "Contractor YTD/MTD/WTD")
        st.plotly_chart(fig_ctr, use_container_width=True)


def render_leading(df: pd.DataFrame, period: str) -> None:
    st.markdown("<div class='section-title'>Leading Indicators</div>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

    left, right = st.columns(2)
    with left:
        leading_long = df.melt(
            id_vars="Activity",
            value_vars=["YTD", "MTD", "WTD"],
            var_name="Period",
            value_name="Count",
        )
        fig = px.bar(
            leading_long,
            x="Activity",
            y="Count",
            color="Period",
            barmode="group",
            color_discrete_sequence=["#5bc0eb", "#8ecae6", "#9fd8f3"],
        )
        chart_style(fig, "Leading Activities by Period")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        focus = df[["Activity", period]].sort_values(period, ascending=False)
        fig_focus = px.bar(
            focus,
            x="Activity",
            y=period,
            color_discrete_sequence=["#8ecae6"],
        )
        chart_style(fig_focus, f"Top Activities ({period})")
        st.plotly_chart(fig_focus, use_container_width=True)


def render_incidents(df: pd.DataFrame) -> None:
    st.markdown("<div class='section-title'>Incidents Register</div>", unsafe_allow_html=True)

    if df.empty:
        st.info("No incidents available for the current filter.")
        return

    incidents = df.copy()
    incidents["Date"] = pd.to_datetime(incidents["Date"])
    incidents["Hour"] = pd.to_datetime(incidents["Time"].str[:5], format="%H:%M", errors="coerce").dt.hour
    incidents["Weekday"] = incidents["Date"].dt.day_name()
    incidents["Weekday"] = pd.Categorical(
        incidents["Weekday"],
        categories=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        ordered=True,
    )

    total_cases = len(incidents)
    open_cases = int((incidents["Status"] == "Open").sum())
    high_cases = int((incidents["Severity"] == "High").sum())
    high_rate = (high_cases / total_cases * 100) if total_cases else 0
    unique_locations = incidents["Location"].nunique()

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(
            f"""
            <div class="glass">
                <p class="kpi-title">Total Incidents</p>
                <p class="kpi-value">{total_cases}</p>
                <p class="kpi-delta">All recorded cases</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            f"""
            <div class="glass">
                <p class="kpi-title">Open Cases</p>
                <p class="kpi-value">{open_cases}</p>
                <p class="kpi-delta">{(open_cases / total_cases * 100):.1f}% backlog</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            f"""
            <div class="glass">
                <p class="kpi-title">High Severity</p>
                <p class="kpi-value">{high_cases}</p>
                <p class="kpi-delta">{high_rate:.1f}% of all incidents</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with k4:
        st.markdown(
            f"""
            <div class="glass">
                <p class="kpi-title">Impacted Locations</p>
                <p class="kpi-value">{unique_locations}</p>
                <p class="kpi-delta">Distinct work areas</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.dataframe(incidents.sort_values(["Date", "Time"], ascending=False), use_container_width=True)

    st.markdown("<div class='section-title'>Incident Mix</div>", unsafe_allow_html=True)
    mix1, mix2, mix3 = st.columns(3)

    with mix1:
        fig_status = px.pie(
            incidents,
            names="Status",
            color="Status",
            hole=0.5,
            color_discrete_map={"Open": "#ff7f50", "Closed": "#5bc0eb"},
        )
        fig_status.update_layout(
            title="Open vs Closed",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#d9e9fb"),
            legend_title=None,
        )
        st.plotly_chart(fig_status, use_container_width=True)

    with mix2:
        sev_type = incidents.groupby(["Type", "Severity"], as_index=False).size().rename(columns={"size": "Count"})
        sev_type["Severity"] = pd.Categorical(
            sev_type["Severity"], categories=["Low", "Medium", "High"], ordered=True
        )
        sev_type = sev_type.sort_values(["Type", "Severity"])
        fig_sev_type = px.bar(
            sev_type,
            x="Type",
            y="Count",
            color="Severity",
            barmode="stack",
            color_discrete_map={"Low": "#9fd8f3", "Medium": "#5bc0eb", "High": "#ff7f50"},
        )
        chart_style(fig_sev_type, "Severity by Incident Type")
        st.plotly_chart(fig_sev_type, use_container_width=True)

    with mix3:
        workforce_type = incidents.groupby(["Workforce", "Type"], as_index=False).size().rename(columns={"size": "Count"})
        fig_workforce = px.bar(
            workforce_type,
            x="Workforce",
            y="Count",
            color="Type",
            barmode="group",
            color_discrete_sequence=["#5bc0eb", "#8ecae6", "#9fd8f3", "#ffb37f", "#7aa8d8", "#b6e3ff"],
        )
        chart_style(fig_workforce, "Type Distribution by Workforce")
        st.plotly_chart(fig_workforce, use_container_width=True)

    st.markdown("<div class='section-title'>Time and Location Signals</div>", unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)

    with t1:
        daily = incidents.groupby("Date", as_index=False).size().rename(columns={"size": "Incidents"})
        fig_daily = px.line(
            daily,
            x="Date",
            y="Incidents",
            markers=True,
            line_shape="spline",
            color_discrete_sequence=["#5bc0eb"],
        )
        chart_style(fig_daily, "Daily Incident Trend")
        st.plotly_chart(fig_daily, use_container_width=True)

    with t2:
        hour_map = incidents.dropna(subset=["Hour"]).copy()
        fig_heat = px.density_heatmap(
            hour_map,
            x="Hour",
            y="Weekday",
            color_continuous_scale=["#1a2536", "#5bc0eb", "#b6e3ff"],
        )
        fig_heat.update_layout(
            title="Incident Timing Heatmap",
            height=330,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.04)",
            margin=dict(l=8, r=8, t=52, b=8),
            font=dict(color="#d9e9fb", family="Segoe UI, Calibri, sans-serif"),
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    with t3:
        top_locations = incidents["Location"].value_counts().reset_index().head(6)
        top_locations.columns = ["Location", "Count"]
        fig_locations = px.bar(
            top_locations,
            x="Count",
            y="Location",
            orientation="h",
            color_discrete_sequence=["#8ecae6"],
        )
        chart_style(fig_locations, "Top Incident Locations")
        st.plotly_chart(fig_locations, use_container_width=True)

    st.markdown("<div class='section-title'>Root Cause Breakdown</div>", unsafe_allow_html=True)
    cause = incidents["Cause"].value_counts().reset_index()
    cause.columns = ["Cause", "Count"]
    fig_cause = px.bar(
        cause,
        x="Cause",
        y="Count",
        color="Count",
        color_continuous_scale=["#9fd8f3", "#5bc0eb", "#126782"],
    )
    chart_style(fig_cause, "Primary Causes")
    st.plotly_chart(fig_cause, use_container_width=True)


def render_findings(df: pd.DataFrame) -> None:
    st.markdown("<div class='section-title'>Findings PICA</div>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

    left, right = st.columns(2)
    with left:
        findings_long = df.melt(
            id_vars="Location",
            value_vars=["Open_Count", "Close_Count"],
            var_name="Status",
            value_name="Count",
        )
        fig = px.bar(
            findings_long,
            x="Location",
            y="Count",
            color="Status",
            barmode="group",
            color_discrete_sequence=["#91c4f2", "#5bc0eb"],
        )
        chart_style(fig, "Open vs Closed Findings")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig_cre = px.bar(df, x="Location", y="CRE", color_discrete_sequence=["#8ecae6"])
        chart_style(fig_cre, "Critical Risk Elements (CRE)")
        st.plotly_chart(fig_cre, use_container_width=True)


def render_areas(df: pd.DataFrame) -> None:
    st.markdown("<div class='section-title'>Monitoring Areas</div>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

    counts = df["Group"].value_counts().reset_index()
    counts.columns = ["Group", "Count"]
    fig = px.bar(counts, x="Group", y="Count", color="Group", color_discrete_sequence=["#5bc0eb", "#8ecae6"])
    chart_style(fig, "Area Group Distribution")
    st.plotly_chart(fig, use_container_width=True)

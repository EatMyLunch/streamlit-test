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

    dcm_col = f"DCM_{period}"
    contractor_col = f"Contractor_{period}"

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
            <div class="glass">
                <p class="kpi-title">DCM {period}</p>
                <p class="kpi-value">{int(lagging[dcm_col].sum())}</p>
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
                <p class="kpi-value">{int(lagging[contractor_col].sum())}</p>
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
                <p class="kpi-value">{int((incidents['Status'] == 'Open').sum())}</p>
                <p class="kpi-delta">Incident register</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"""
            <div class="glass">
                <p class="kpi-title">Open Findings</p>
                <p class="kpi-value">{int(findings['Open_Count'].sum())}</p>
                <p class="kpi-delta">PICA tracking</p>
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
        fig_type = px.pie(
            incidents,
            names="Type",
            color_discrete_sequence=["#5bc0eb", "#8ecae6", "#91c4f2", "#b7d8f7", "#d8ecff", "#7aa8d8"],
        )
        fig_type.update_layout(
            title="Incident Type Composition",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#d9e9fb"),
            legend_title=None,
        )
        st.plotly_chart(fig_type, use_container_width=True)


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
    st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True)

    left, right = st.columns(2)
    with left:
        fig_status = px.pie(
            df,
            names="Status",
            color_discrete_sequence=["#5bc0eb", "#b6e3ff"],
        )
        fig_status.update_layout(title="Open vs Closed", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#d9e9fb"))
        st.plotly_chart(fig_status, use_container_width=True)

    with right:
        cause = df["Cause"].value_counts().reset_index()
        cause.columns = ["Cause", "Count"]
        fig_cause = px.bar(cause, x="Cause", y="Count", color_discrete_sequence=["#8ecae6"])
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

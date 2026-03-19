import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="OHS Safety Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
)


st.markdown(
    """
    <style>
        :root {
            --brand: #0f4c81;
            --brand-soft: #e8f0f7;
            --text-main: #1f2d3d;
            --text-soft: #617083;
            --card-border: #d9e2ec;
        }

        .stApp {
            background:
                radial-gradient(circle at 5% 0%, #f7fbff 0%, #f7fbff 35%, #f2f6fa 100%);
            color: var(--text-main);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f6f9fc 0%, #eef3f9 100%);
            border-right: 1px solid var(--card-border);
        }

        [data-testid="stSidebar"] .stRadio label {
            font-weight: 600;
            color: var(--text-main);
        }

        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
            background: #ffffff;
            border: 1px solid var(--card-border);
            border-radius: 8px;
            padding: 8px 10px;
            margin-bottom: 6px;
            transition: all 0.15s ease-in-out;
        }

        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
            border-color: var(--brand);
            box-shadow: 0 1px 6px rgba(15, 76, 129, 0.14);
        }

        .title-card {
            background: #ffffff;
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 12px 16px;
            margin-bottom: 12px;
        }

        .metric-card {
            background: #ffffff;
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 4px 10px;
        }

        .section-caption {
            color: var(--text-soft);
            margin-top: -4px;
            margin-bottom: 14px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data() -> dict[str, pd.DataFrame]:
    lagging = pd.DataFrame(
        [
            ["Fatality", 0, 0, 0, 0, 0, 0],
            ["LTI", 3, 0, 0, 6, 2, 0],
            ["MTC", 4, 1, 0, 5, 1, 0],
            ["FAC", 7, 2, 1, 13, 4, 1],
            ["Fire Case", 1, 0, 0, 1, 0, 0],
            ["PD", 2, 1, 0, 3, 1, 0],
        ],
        columns=[
            "Metric",
            "DCM_YTD",
            "DCM_MTD",
            "DCM_WTD",
            "Contractor_YTD",
            "Contractor_MTD",
            "Contractor_WTD",
        ],
    )

    leading = pd.DataFrame(
        [
            ["Unsafe Action TTA", 544, 302, 50],
            ["Safety Talk", 186, 44, 12],
            ["Toolbox Meeting", 230, 68, 18],
            ["Safety Patrol", 141, 33, 10],
            ["Inspection", 94, 22, 6],
            ["Behavior Observation", 210, 57, 16],
        ],
        columns=["Activity", "YTD", "MTD", "WTD"],
    )

    incidents = pd.DataFrame(
        [
            ["2026-03-09", "23:03 WIT", "Saepul", "IPAL Sriwijaya", "FAC", "Pinch point", "Closed"],
            ["2026-03-10", "08:15 WIT", "Rahman", "Jetty N3", "Nearmiss NM", "Slip hazard", "Open"],
            ["2026-03-11", "14:30 WIT", "Dedi", "Workshop", "MTC", "Hot surface", "Closed"],
            ["2026-03-12", "10:00 WIT", "Arif", "Jetty Selatan", "FAC", "Hand tool contact", "Open"],
            ["2026-03-13", "16:40 WIT", "Bimo", "TPST Karo", "Fire Case", "Electrical short", "Closed"],
            ["2026-03-14", "06:20 WIT", "Sandi", "IPAL", "PD", "Dust exposure", "Closed"],
        ],
        columns=["Date", "Time", "Name", "Location", "Type", "Cause", "Status"],
    )
    incidents["Date"] = pd.to_datetime(incidents["Date"])

    findings = pd.DataFrame(
        [
            ["Jetty N1", 8, 100, 6],
            ["Jetty N2", 6, 78, 5],
            ["Jetty Selatan", 12, 65, 8],
            ["Workshop", 4, 52, 4],
            ["IPAL", 9, 70, 7],
            ["TPST Karo", 5, 47, 3],
        ],
        columns=["Location", "Open_Count", "Close_Count", "CRE"],
    )

    areas = pd.DataFrame(
        [
            ["Utara", "Jetty Utara"],
            ["Utara", "Jetty N1"],
            ["Utara", "Jetty N2"],
            ["Selatan", "Jetty Selatan"],
            ["Selatan", "Workshop"],
            ["Selatan", "IPAL"],
            ["Selatan", "TPST Karo"],
        ],
        columns=["Group", "Description"],
    )

    return {
        "Lagging_Indicators": lagging,
        "Leading_Indicators": leading,
        "Incidents": incidents,
        "Findings_PICA": findings,
        "Monitoring_Areas": areas,
    }


def melt_lagging_by_period(df: pd.DataFrame, owner: str) -> pd.DataFrame:
    cols = [f"{owner}_YTD", f"{owner}_MTD", f"{owner}_WTD"]
    melted = df[["Metric", *cols]].melt(
        id_vars="Metric",
        value_vars=cols,
        var_name="Period",
        value_name="Count",
    )
    melted["Period"] = melted["Period"].str.replace(f"{owner}_", "", regex=False)
    return melted


def show_header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="title-card">
            <h3 style="margin:0; color:#0f4c81;">{title}</h3>
            <p class="section-caption">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_login() -> None:
    st.markdown("## OHS Safety Dashboard")
    st.caption("Login placeholder: replace with your real authentication flow later.")

    with st.form("login_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Username", placeholder="ohs.admin")
        with col2:
            password = st.text_input("Password", type="password", placeholder="********")

        submitted = st.form_submit_button("Sign In", use_container_width=False)
        if submitted:
            if username and password:
                st.session_state.logged_in = True
                st.session_state.user_name = username
                st.success("Login success (placeholder mode).")
                st.rerun()
            st.error("Please input username and password.")


def render_lagging(df: pd.DataFrame) -> None:
    show_header("Lagging Indicators", "Incident counts by severity and workforce group.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total DCM YTD", int(df["DCM_YTD"].sum()))
    c2.metric("Total Contractor YTD", int(df["Contractor_YTD"].sum()))
    c3.metric("Total DCM WTD", int(df["DCM_WTD"].sum()))
    c4.metric("Total Contractor WTD", int(df["Contractor_WTD"].sum()))

    st.dataframe(df, use_container_width=True)

    left, right = st.columns(2)
    with left:
        dcm_long = melt_lagging_by_period(df, "DCM")
        fig_dcm = px.bar(
            dcm_long,
            x="Metric",
            y="Count",
            color="Period",
            barmode="group",
            title="DCM: YTD vs MTD vs WTD",
            color_discrete_sequence=["#0f4c81", "#2f6ea2", "#82a7c8"],
        )
        fig_dcm.update_layout(legend_title=None)
        st.plotly_chart(fig_dcm, use_container_width=True)

    with right:
        contractor_long = melt_lagging_by_period(df, "Contractor")
        fig_ctr = px.bar(
            contractor_long,
            x="Metric",
            y="Count",
            color="Period",
            barmode="group",
            title="Contractor: YTD vs MTD vs WTD",
            color_discrete_sequence=["#0f4c81", "#2f6ea2", "#82a7c8"],
        )
        fig_ctr.update_layout(legend_title=None)
        st.plotly_chart(fig_ctr, use_container_width=True)


def render_leading(df: pd.DataFrame) -> None:
    show_header("Leading Indicators", "Proactive safety activity tracking.")

    c1, c2, c3 = st.columns(3)
    c1.metric("YTD Total", int(df["YTD"].sum()))
    c2.metric("MTD Total", int(df["MTD"].sum()))
    c3.metric("WTD Total", int(df["WTD"].sum()))

    st.dataframe(df, use_container_width=True)

    long_df = df.melt(
        id_vars="Activity",
        value_vars=["YTD", "MTD", "WTD"],
        var_name="Period",
        value_name="Count",
    )
    fig = px.bar(
        long_df,
        x="Activity",
        y="Count",
        color="Period",
        barmode="group",
        title="Leading Activities by Period",
        color_discrete_sequence=["#0f4c81", "#2f6ea2", "#82a7c8"],
    )
    fig.update_layout(legend_title=None)
    st.plotly_chart(fig, use_container_width=True)


def render_incidents(df: pd.DataFrame) -> None:
    show_header("Incidents", "Detailed incident records and composition.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Cases", len(df))
    c2.metric("Open Cases", int((df["Status"] == "Open").sum()))
    c3.metric("Closed Cases", int((df["Status"] == "Closed").sum()))

    st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True)

    left, right = st.columns(2)
    with left:
        fig_type = px.pie(
            df,
            names="Type",
            title="Incident Type Distribution",
            color_discrete_sequence=["#0f4c81", "#2f6ea2", "#4f89ba", "#77a6cd", "#9cbfda", "#c4d8e9"],
        )
        st.plotly_chart(fig_type, use_container_width=True)

    with right:
        cause_count = df["Cause"].value_counts().reset_index()
        cause_count.columns = ["Cause", "Count"]
        fig_cause = px.bar(
            cause_count,
            x="Cause",
            y="Count",
            title="Incident Causes",
            color_discrete_sequence=["#2f6ea2"],
        )
        st.plotly_chart(fig_cause, use_container_width=True)


def render_findings(df: pd.DataFrame) -> None:
    show_header("Findings & PICA", "Open/closed finding counts and CRE by location.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Open Findings", int(df["Open_Count"].sum()))
    c2.metric("Closed Findings", int(df["Close_Count"].sum()))
    c3.metric("Avg CRE", round(float(df["CRE"].mean()), 2))

    st.dataframe(df, use_container_width=True)

    left, right = st.columns(2)
    with left:
        findings_long = df.melt(
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
            title="Open vs Closed Findings by Location",
            color_discrete_sequence=["#c77852", "#0f4c81"],
        )
        fig_findings.update_layout(legend_title=None)
        st.plotly_chart(fig_findings, use_container_width=True)

    with right:
        fig_cre = px.bar(
            df,
            x="Location",
            y="CRE",
            title="CRE Distribution by Location",
            color_discrete_sequence=["#2f6ea2"],
        )
        st.plotly_chart(fig_cre, use_container_width=True)


def render_areas(df: pd.DataFrame) -> None:
    show_header("Monitoring Areas", "Grouping used for area-level monitoring views.")

    c1, c2 = st.columns(2)
    c1.metric("Groups", int(df["Group"].nunique()))
    c2.metric("Monitored Areas", int(len(df)))

    st.dataframe(df, use_container_width=True)

    group_counts = df["Group"].value_counts().reset_index()
    group_counts.columns = ["Group", "Count"]
    fig_group = px.bar(
        group_counts,
        x="Group",
        y="Count",
        title="Areas per Group",
        color="Group",
        color_discrete_sequence=["#0f4c81", "#6b8faa"],
    )
    st.plotly_chart(fig_group, use_container_width=True)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if not st.session_state.logged_in:
    render_login()
    st.stop()


data = load_data()

with st.sidebar:
    st.markdown("### OHS Dashboard")
    st.caption(f"User: {st.session_state.get('user_name', 'user')}")
    selected_page = st.radio(
        "Navigate",
        ["Lagging", "Leading", "Incidents", "Findings", "Areas"],
        label_visibility="collapsed",
    )

    st.divider()
    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()


st.title("OHS Safety Dashboard")
st.caption("Weekly monitoring view. Data shown below is sample data based on your sheet structure.")


if selected_page == "Lagging":
    render_lagging(data["Lagging_Indicators"])
elif selected_page == "Leading":
    render_leading(data["Leading_Indicators"])
elif selected_page == "Incidents":
    render_incidents(data["Incidents"])
elif selected_page == "Findings":
    render_findings(data["Findings_PICA"])
else:
    render_areas(data["Monitoring_Areas"])

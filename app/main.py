import streamlit as st
from streamlit_option_menu import option_menu

from app.data.mock_data import load_mock_sheet_tabs
from app.services.transformers import filter_areas, filter_incident_status
from app.theme import inject_global_css
from app.views.pages import (
    render_areas,
    render_findings,
    render_hero,
    render_incidents,
    render_lagging,
    render_leading,
    render_overview,
)


def setup_page() -> None:
    st.set_page_config(
        page_title="Ultimate OHS Dashboard Mockup",
        page_icon=":helmet_with_white_cross:",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def run_app() -> None:
    setup_page()
    inject_global_css()

    data = load_mock_sheet_tabs()

    with st.sidebar:
        st.markdown("## Ultimate OHS")
        st.caption("Mockup mode")

        selected_page = option_menu(
            menu_title=None,
            options=["Overview", "Lagging", "Leading", "Incidents", "Findings", "Areas"],
            icons=["speedometer2", "exclamation-triangle", "activity", "clipboard-data", "check2-square", "geo-alt"],
            default_index=0,
            styles={
                "container": {"padding": "0", "background-color": "transparent"},
                "icon": {"color": "#9fd8f3", "font-size": "16px"},
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "5px 0",
                    "border-radius": "10px",
                    "color": "#d8e8fb",
                    "padding": "8px 12px",
                },
                "nav-link-selected": {
                    "background-color": "rgba(91, 192, 235, 0.24)",
                    "color": "#f3f9ff",
                },
            },
        )

        st.divider()
        period = st.selectbox("Period", ["YTD", "MTD", "WTD"], index=0)
        area_scope = st.selectbox("Area Group", ["All", "Utara", "Selatan"], index=0)
        incident_status = st.selectbox("Incident Status", ["All", "Open", "Closed"], index=0)

    filtered = filter_areas(data, area_scope)
    filtered["Incidents"] = filter_incident_status(filtered["Incidents"], incident_status)

    render_hero(period, area_scope)

    if selected_page == "Overview":
        render_overview(filtered, period)
    elif selected_page == "Lagging":
        render_lagging(filtered["Lagging_Indicators"])
    elif selected_page == "Leading":
        render_leading(filtered["Leading_Indicators"], period)
    elif selected_page == "Incidents":
        render_incidents(filtered["Incidents"])
    elif selected_page == "Findings":
        render_findings(filtered["Findings_PICA"])
    else:
        render_areas(filtered["Monitoring_Areas"])

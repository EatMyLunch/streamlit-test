import streamlit as st
from streamlit_option_menu import option_menu

from app.data.mock_data import load_mock_sheet_tabs as load_sheet_tabs
from app.content import APP_TITLE, NAV_LABELS, SIDEBAR_SUBTITLE, SIDEBAR_TITLE
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
        page_title=APP_TITLE,
        page_icon=":helmet_with_white_cross:",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def run_app() -> None:
    setup_page()
    inject_global_css()

    data = load_sheet_tabs()
    period = "YTD"
    area_scope = "All"
    incident_status = "All"

    with st.sidebar:
        st.markdown(
            f"""
            <div class="sidebar-brand">
                <p class="sidebar-brand__title">{SIDEBAR_TITLE}</p>
                <p class="sidebar-brand__subtitle">{SIDEBAR_SUBTITLE}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        selected_page = option_menu(
            menu_title=None,
            options=NAV_LABELS,
            icons=["speedometer2", "exclamation-triangle", "activity", "clipboard-data", "check2-square", "geo-alt"],
            default_index=0,
            styles={
                "container": {
                    "padding": "8px",
                    "background-color": "rgba(255, 255, 255, 0.03)",
                    "border": "1px solid rgba(173, 216, 255, 0.16)",
                    "border-radius": "14px",
                },
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

    filtered = filter_areas(data, area_scope)
    filtered["Incidents"] = filter_incident_status(filtered["Incidents"], incident_status)

    render_hero(period, area_scope)

    if selected_page == "Executive Overview":
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

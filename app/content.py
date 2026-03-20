"""Centralized user-facing copy for the dashboard UI."""

APP_TITLE = "Ultimate OHS Performance Dashboard"
SIDEBAR_TITLE = "Ultimate OHS"
SIDEBAR_SUBTITLE = "Operational reporting"

NAV_LABELS = ["Executive Overview", "Lagging", "Leading", "Incidents", "Findings", "Areas"]

HERO_TITLE = "ULTIMATE OHS Performance Dashboard"
HERO_BODY = (
    "Executive operational view built from enterprise OHS reporting domains: "
    "Lagging Indicators, Leading Indicators, Incident Management, Findings & PICA, "
    "and Monitoring Areas. Current filter context: period {period} and area scope {area_scope}."
)
GENERATED_LABEL = "Data refresh"

SECTION_TITLES = {
    "snapshot": "Safety Performance Snapshot",
    "signals": "Operational Signals",
    "findings_exposure": "Findings and Risk Exposure",
    "lagging": "Lagging Indicators",
    "leading": "Leading Indicators",
    "incidents": "Incident Register",
    "incident_mix": "Incident Mix",
    "time_location": "Time and Location Signals",
    "root_cause": "Root Cause Breakdown",
    "findings": "Findings and PICA",
    "areas": "Monitoring Areas",
}

MESSAGES = {
    "no_incident_headline": "No incidents are currently logged for the selected filter context.",
    "no_incident_chart": "No incident records are available for the current filter selection.",
    "no_trend": "No incident trend data is available for the selected period.",
    "no_severity": "Severity classification data is unavailable in the selected records.",
    "no_incidents_page": "No incidents are available for the current filter selection.",
}

KPI_META = {
    "lagging_total": "Lagging indicator total",
    "all_recorded_cases": "All recorded cases",
    "distinct_work_areas": "Distinct work areas",
}

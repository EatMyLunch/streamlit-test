from datetime import datetime

import pandas as pd
import streamlit as st


LAGGING_METRICS = ["Fatality", "LTI", "MTC", "FAC", "Fire Case", "PD"]


@st.cache_data
def load_mock_sheet_tabs() -> dict[str, pd.DataFrame]:
    current_year = datetime.now().year

    incidents_raw = pd.DataFrame(
        [
            [f"{current_year}-03-02", "07:10 WIT", "Saepul", "Jetty Utara", "FAC", "Pinch point", "Closed", "Low", "DCM"],
            [f"{current_year}-03-03", "10:20 WIT", "Rahman", "Jetty N3", "Nearmiss NM", "Slip hazard", "Open", "Medium", "Contractor"],
            [f"{current_year}-03-03", "14:20 WIT", "Dedi", "Workshop", "MTC", "Hot surface", "Closed", "Medium", "DCM"],
            [f"{current_year}-03-04", "18:40 WIT", "Arif", "Jetty Selatan", "FAC", "Hand tool contact", "Open", "Low", "Contractor"],
            [f"{current_year}-03-05", "05:15 WIT", "Bimo", "TPST Karo", "Fire Case", "Electrical short", "Closed", "High", "DCM"],
            [f"{current_year}-03-06", "06:20 WIT", "Sandi", "IPAL", "PD", "Dust exposure", "Closed", "Medium", "Contractor"],
            [f"{current_year}-03-07", "11:40 WIT", "Rian", "Jetty N1", "FAC", "Dropped material", "Open", "Medium", "DCM"],
            [f"{current_year}-03-08", "09:55 WIT", "Galih", "Jetty N2", "Nearmiss NM", "Vehicle blind spot", "Closed", "Low", "Contractor"],
            [f"{current_year}-03-09", "23:03 WIT", "Bayu", "IPAL Sriwijaya", "FAC", "Pinch point", "Closed", "Low", "DCM"],
            [f"{current_year}-03-10", "08:15 WIT", "Rafi", "Jetty N3", "LTI", "Improper lifting", "Open", "High", "Contractor"],
            [f"{current_year}-03-10", "16:50 WIT", "Teguh", "Workshop", "MTC", "Sharp edge", "Closed", "Medium", "DCM"],
            [f"{current_year}-03-11", "10:00 WIT", "Ari", "Jetty Selatan", "FAC", "Falling object", "Closed", "Low", "Contractor"],
            [f"{current_year}-03-11", "20:35 WIT", "Hendra", "Jetty Utara", "PD", "Fume inhalation", "Closed", "Medium", "DCM"],
            [f"{current_year}-03-12", "13:10 WIT", "Yusuf", "Workshop", "LTI", "Hand trapped", "Open", "High", "DCM"],
            [f"{current_year}-03-12", "07:35 WIT", "Imam", "IPAL", "FAC", "Minor cut", "Closed", "Low", "Contractor"],
            [f"{current_year}-03-13", "12:25 WIT", "Slamet", "Jetty N2", "FAC", "Struck by object", "Open", "Medium", "Contractor"],
            [f"{current_year}-03-14", "06:40 WIT", "Jaka", "Jetty Utara", "PD", "Chemical splash", "Open", "High", "DCM"],
            [f"{current_year}-03-14", "15:10 WIT", "Rizky", "Workshop", "Nearmiss NM", "Unsafe access", "Closed", "Low", "Contractor"],
        ],
        columns=["Date", "Time", "Name", "Location", "Type", "Cause", "Status", "Severity", "Workforce"],
    )
    incidents_raw["Date"] = pd.to_datetime(incidents_raw["Date"])

    lagging = build_lagging_from_incidents(incidents_raw)

    leading = pd.DataFrame(
        [
            ["Unsafe Action TTA", 544, 302, 50],
            ["Safety Talk", 186, 44, 12],
            ["Toolbox Meeting", 230, 68, 18],
            ["Safety Patrol", 141, 33, 10],
            ["Inspection", 94, 22, 6],
            ["Behavior Observation", 210, 57, 16],
            ["PPE Compliance Check", 156, 41, 11],
        ],
        columns=["Activity", "YTD", "MTD", "WTD"],
    )

    findings = pd.DataFrame(
        [
            ["Jetty Utara", 8, 100, 6],
            ["Jetty N1", 6, 78, 5],
            ["Jetty N2", 5, 70, 4],
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

    incidents = incidents_raw[["Date", "Time", "Name", "Location", "Type", "Cause", "Status", "Severity", "Workforce"]].copy()

    return {
        "Lagging_Indicators": lagging,
        "Leading_Indicators": leading,
        "Incidents": incidents,
        "Findings_PICA": findings,
        "Monitoring_Areas": areas,
    }


def build_lagging_from_incidents(incidents_raw: pd.DataFrame) -> pd.DataFrame:
    now = datetime.now()
    ytd_start = datetime(now.year, 1, 1)
    mtd_start = datetime(now.year, now.month, 1)
    wtd_start = now - pd.to_timedelta(now.weekday(), unit="D")
    wtd_start = datetime(wtd_start.year, wtd_start.month, wtd_start.day)

    periods = {
        "YTD": ytd_start,
        "MTD": mtd_start,
        "WTD": wtd_start,
    }

    rows: list[list[object]] = []

    for metric in LAGGING_METRICS:
        row: list[object] = [metric]
        for workforce in ["DCM", "Contractor"]:
            worker_df = incidents_raw[(incidents_raw["Workforce"] == workforce) & (incidents_raw["Type"] == metric)]
            for _, period_start in periods.items():
                row.append(int((worker_df["Date"] >= period_start).sum()))
        rows.append(row)

    return pd.DataFrame(
        rows,
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

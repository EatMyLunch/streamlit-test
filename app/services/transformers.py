import pandas as pd


def filter_areas(
    data: dict[str, pd.DataFrame],
    area_scope: str,
) -> dict[str, pd.DataFrame]:
    filtered = {k: v.copy() for k, v in data.items()}

    if area_scope == "All":
        return filtered

    area_list = filtered["Monitoring_Areas"].loc[
        filtered["Monitoring_Areas"]["Group"] == area_scope,
        "Description",
    ]

    filtered["Incidents"] = filtered["Incidents"][filtered["Incidents"]["Location"].isin(area_list)]
    filtered["Findings_PICA"] = filtered["Findings_PICA"][filtered["Findings_PICA"]["Location"].isin(area_list)]
    filtered["Monitoring_Areas"] = filtered["Monitoring_Areas"][filtered["Monitoring_Areas"]["Group"] == area_scope]

    return filtered


def filter_incident_status(incidents: pd.DataFrame, status: str) -> pd.DataFrame:
    if status == "All":
        return incidents
    return incidents[incidents["Status"] == status]


def melt_lagging(df: pd.DataFrame, owner: str) -> pd.DataFrame:
    cols = [f"{owner}_YTD", f"{owner}_MTD", f"{owner}_WTD"]
    out = df[["Metric", *cols]].melt(
        id_vars="Metric",
        value_vars=cols,
        var_name="Period",
        value_name="Count",
    )
    out["Period"] = out["Period"].str.replace(f"{owner}_", "", regex=False)
    return out

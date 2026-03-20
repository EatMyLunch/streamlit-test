# Ultimate OHS Dashboard Mockup

This repository contains a Streamlit mockup for an Occupational Health and Safety (OHS) dashboard.
It uses only OHS-related sample data aligned with the provided Google Sheet structure:

1. Lagging_Indicators
2. Leading_Indicators
3. Incidents
4. Findings_PICA
5. Monitoring_Areas

The current app is designed for UI and flow validation before integrating real production data.

## Project Structure

```text
streamlit_app.py
app/
   main.py                  # App orchestration and sidebar navigation
   theme.py                 # Global CSS theme and glassmorphism styles
   data/
      mock_data.py           # OHS-only mock datasets and lagging calculations
   services/
      transformers.py        # Filtering and dataframe transformations
   views/
      pages.py               # Page renderers and chart sections
```

## Run Locally

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Run Streamlit

```bash
streamlit run streamlit_app.py
```

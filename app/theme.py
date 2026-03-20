import streamlit as st


def inject_global_css() -> None:
    st.markdown(
        """
        <style>
            :root {
                --bg-1: #0d1b2a;
                --bg-2: #1b263b;
                --panel: rgba(255, 255, 255, 0.08);
                --panel-strong: rgba(255, 255, 255, 0.12);
                --panel-border: rgba(173, 216, 255, 0.26);
                --text-main: #ecf4ff;
                --text-soft: #b9cae0;
                --accent: #5bc0eb;
                --accent-soft: #9fd8f3;
                --risk: #ff8a65;
                --focus: #6ee7c8;
            }

            .stApp {
                font-family: "Segoe UI", "Calibri", sans-serif;
                color: var(--text-main);
                background:
                    radial-gradient(800px 420px at 8% -8%, rgba(91, 192, 235, 0.24), rgba(91, 192, 235, 0) 70%),
                    radial-gradient(900px 500px at 96% 0%, rgba(159, 216, 243, 0.2), rgba(159, 216, 243, 0) 75%),
                    linear-gradient(140deg, var(--bg-1) 0%, var(--bg-2) 100%);
            }

            .main .block-container {
                padding-top: 1.4rem;
                padding-bottom: 2rem;
            }

            [data-testid="stHorizontalBlock"] {
                gap: 1rem;
            }

            [data-testid="stDataFrame"] {
                padding-top: 0.35rem;
                padding-bottom: 1rem;
            }

            .stPlotlyChart {
                padding-top: 0.3rem;
                padding-bottom: 0.7rem;
            }

            [data-testid="stAlert"] {
                margin-top: 0.3rem;
                margin-bottom: 0.9rem;
            }

            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, rgba(13, 27, 42, 0.95), rgba(27, 38, 59, 0.95));
                border-right: 1px solid rgba(173, 216, 255, 0.2);
            }

            [data-testid="stSidebar"] > div:first-child {
                padding-top: 1.1rem;
            }

            .sidebar-brand {
                background: linear-gradient(130deg, rgba(91, 192, 235, 0.18), rgba(159, 216, 243, 0.08));
                border: 1px solid rgba(173, 216, 255, 0.28);
                border-radius: 14px;
                padding: 12px 14px;
                margin-bottom: 12px;
                box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.03);
            }

            .sidebar-brand__title {
                margin: 0;
                font-size: 1.03rem;
                font-weight: 700;
                color: #f1f8ff;
            }

            .sidebar-brand__subtitle {
                margin: 3px 0 0 0;
                font-size: 0.83rem;
                color: #a9c3da;
            }

            .glass {
                background: var(--panel);
                border: 1px solid var(--panel-border);
                border-radius: 16px;
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                box-shadow: 0 14px 28px rgba(0, 10, 30, 0.3);
                padding: 16px 18px;
            }

            .kpi-card {
                position: relative;
                overflow: hidden;
                background:
                    linear-gradient(160deg, rgba(13, 28, 45, 0.86), rgba(19, 38, 60, 0.72)),
                    radial-gradient(280px 160px at 100% 0%, rgba(91, 192, 235, 0.22), rgba(91, 192, 235, 0));
                border: 1px solid rgba(173, 216, 255, 0.34);
                border-radius: 16px;
                padding: 13px 14px 14px 14px;
                box-shadow: 0 14px 28px rgba(0, 10, 30, 0.34);
                min-height: 126px;
                transition: border-color 0.2s ease, transform 0.2s ease;
            }

            .kpi-card:hover {
                border-color: rgba(173, 216, 255, 0.62);
                transform: translateY(-1px);
            }

            .kpi-card::after {
                content: "";
                position: absolute;
                left: 0;
                top: 0;
                width: 100%;
                height: 3px;
                background: linear-gradient(90deg, rgba(91, 192, 235, 0.95), rgba(159, 216, 243, 0.7));
            }

            .kpi-card__head {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 6px;
            }

            .kpi-card__label {
                color: #bed2e8;
                font-size: 0.76rem;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                font-weight: 700;
            }

            .kpi-card__icon {
                width: 30px;
                height: 30px;
                border-radius: 9px;
                border: 1px solid rgba(173, 216, 255, 0.34);
                background: rgba(10, 25, 40, 0.72);
                color: #d7e9fb;
                font-size: 0.73rem;
                font-weight: 700;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .kpi-card__value {
                color: #f2f8ff;
                font-size: 1.8rem;
                line-height: 1.15;
                font-weight: 720;
                margin: 2px 0 4px 0;
            }

            .kpi-card__meta {
                color: #9fd8f3;
                font-size: 0.84rem;
                margin: 0;
            }

            .kpi-card--risk::after {
                background: linear-gradient(90deg, rgba(255, 138, 101, 0.95), rgba(255, 200, 159, 0.72));
            }

            .kpi-card--risk .kpi-card__meta {
                color: #ffc4b0;
            }

            .kpi-card--focus::after {
                background: linear-gradient(90deg, rgba(110, 231, 200, 0.95), rgba(166, 244, 226, 0.72));
            }

            .kpi-card--focus .kpi-card__meta {
                color: #b8f3e4;
            }

            .hero {
                background: linear-gradient(120deg, rgba(91, 192, 235, 0.18), rgba(255, 255, 255, 0.05));
                border: 1px solid var(--panel-border);
                border-radius: 20px;
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                padding: 24px;
                margin-bottom: 0.6rem;
                box-shadow: 0 20px 34px rgba(0, 10, 30, 0.35);
            }

            .hero h1 {
                margin: 0;
                font-size: 2rem;
                font-weight: 700;
                color: #f4f9ff;
            }

            .muted {
                color: var(--text-soft);
                font-size: 0.93rem;
            }

            .section-title {
                color: #f0f7ff;
                font-size: 1.02rem;
                font-weight: 700;
                margin: 1.15rem 0 0.55rem 0;
                padding-top: 0.1rem;
            }

            .kpi-title {
                color: var(--text-soft);
                font-size: 0.85rem;
                margin: 0;
            }

            .kpi-value {
                color: #f2f8ff;
                font-size: 1.6rem;
                font-weight: 700;
                margin: 5px 0;
            }

            .kpi-delta {
                color: var(--accent-soft);
                font-size: 0.88rem;
                margin: 0;
            }

            .insight-band {
                margin-top: 12px;
                margin-bottom: 8px;
                background:
                    linear-gradient(115deg, rgba(91, 192, 235, 0.2), rgba(255, 255, 255, 0.05)),
                    radial-gradient(600px 120px at 80% 10%, rgba(159, 216, 243, 0.18), rgba(159, 216, 243, 0));
                border: 1px solid rgba(173, 216, 255, 0.32);
                border-radius: 18px;
                padding: 14px 16px;
            }

            .insight-title {
                margin: 0;
                color: #f4f9ff;
                font-size: 0.78rem;
                letter-spacing: 0.11em;
                text-transform: uppercase;
                font-weight: 700;
            }

            .insight-text {
                margin: 4px 0 0 0;
                color: #d7e9fb;
                font-size: 0.95rem;
            }

            .pill-row {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-top: 10px;
            }

            .pill {
                background: rgba(10, 29, 48, 0.52);
                border: 1px solid rgba(173, 216, 255, 0.24);
                border-radius: 999px;
                color: #d8ebfb;
                font-size: 0.8rem;
                padding: 4px 10px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

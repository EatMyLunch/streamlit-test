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
            }

            .stApp {
                font-family: "Segoe UI", "Calibri", sans-serif;
                color: var(--text-main);
                background:
                    radial-gradient(800px 420px at 8% -8%, rgba(91, 192, 235, 0.24), rgba(91, 192, 235, 0) 70%),
                    radial-gradient(900px 500px at 96% 0%, rgba(159, 216, 243, 0.2), rgba(159, 216, 243, 0) 75%),
                    linear-gradient(140deg, var(--bg-1) 0%, var(--bg-2) 100%);
            }

            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, rgba(13, 27, 42, 0.95), rgba(27, 38, 59, 0.95));
                border-right: 1px solid rgba(173, 216, 255, 0.2);
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

            .hero {
                background: linear-gradient(120deg, rgba(91, 192, 235, 0.18), rgba(255, 255, 255, 0.05));
                border: 1px solid var(--panel-border);
                border-radius: 20px;
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                padding: 24px;
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
                margin: 12px 0 8px 0;
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
        </style>
        """,
        unsafe_allow_html=True,
    )

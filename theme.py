import streamlit as st

def apply_theme():

    st.markdown("""
    <style>

    :root {
        --sc-primary: #2563eb;
        --sc-primary-soft: #e0ecff;
        --sc-primary-dark: #1e40af;
        --sc-bg: #f4f5fb;
        --sc-card-bg: #ffffff;
        --sc-border-subtle: #e5e7eb;
        --sc-text-main: #111827;
        --sc-text-muted: #6b7280;
        --sc-radius-lg: 16px;
        --sc-radius-md: 10px;
        --sc-shadow-soft: 0 18px 45px rgba(15, 23, 42, 0.06);
    }

    /* ---------- GLOBAL / LAYOUT ---------- */
    html, body, [class*="css"] {
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
                     sans-serif !important;
    }

    .stApp {
        background: radial-gradient(circle at top left, #eef2ff 0, #f9fafb 35%, #f3f4f6 100%);
    }

    .main .block-container {
        padding-top: 2.25rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* ---------- SIDEBAR ---------- */
    section[data-testid="stSidebar"] {
        background: var(--sc-card-bg);
        border-right: 1px solid var(--sc-border-subtle);
        box-shadow: 2px 0 18px rgba(15, 23, 42, 0.06);
    }

    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 1.25rem;
        padding-bottom: 1.5rem;
    }

    /* Sidebar nav buttons & links */
    section[data-testid="stSidebar"] button,
    section[data-testid="stSidebar"] a {
        border-radius: 999px !important;
        padding: 0.45rem 0.85rem !important;
        font-size: 0.9rem !important;
        color: var(--sc-text-main) !important;
        transition: background-color 0.16s ease, color 0.16s ease, transform 0.16s ease;
    }

    section[data-testid="stSidebar"] button:hover,
    section[data-testid="stSidebar"] a:hover {
        background: rgba(37, 99, 235, 0.06) !important;
        transform: translateX(2px);
    }

    /* ---------- HEADINGS & TEXT ---------- */
    h1, h2, h3, h4 {
        color: var(--sc-text-main);
        letter-spacing: -0.02em;
    }

    h1 {
        font-size: 1.9rem;
    }

    h2 {
        font-size: 1.4rem;
    }

    p, label, span, li {
        color: var(--sc-text-muted);
        font-size: 0.95rem;
    }

    /* ---------- FORMS: INPUTS & SELECTS ---------- */
    input, textarea, select {
        background: #ffffff !important;
        color: var(--sc-text-main) !important;
        border-radius: 0.6rem !important;
        border: 1px solid var(--sc-border-subtle) !important;
        padding: 0.4rem 0.7rem !important;
        box-shadow: none !important;
        transition: border-color 0.16s ease, box-shadow 0.16s ease, background-color 0.16s ease;
    }

    input:focus-visible, textarea:focus-visible, select:focus-visible {
        outline: none !important;
        border-color: var(--sc-primary) !important;
        box-shadow: 0 0 0 1px rgba(37, 99, 235, 0.25) !important;
        background-color: #f9fbff !important;
    }

    /* Streamlit-specific input wrappers */
    [data-testid="stSelectbox"] > div,
    [data-testid="stMultiSelect"] > div,
    [data-testid="stNumberInput"] > div {
        border-radius: 0.7rem !important;
        border: 1px solid var(--sc-border-subtle) !important;
        padding: 0.1rem 0.4rem !important;
        background: #ffffff !important;
        transition: border-color 0.16s ease, box-shadow 0.16s ease, background-color 0.16s ease;
    }

    [data-testid="stSelectbox"] > div:focus-within,
    [data-testid="stMultiSelect"] > div:focus-within,
    [data-testid="stNumberInput"] > div:focus-within {
        border-color: var(--sc-primary) !important;
        box-shadow: 0 0 0 1px rgba(37, 99, 235, 0.25) !important;
        background: #f9fbff !important;
    }

    /* ---------- BUTTONS ---------- */
    .stButton > button,
    .stDownloadButton > button {
        background: linear-gradient(135deg, var(--sc-primary), var(--sc-primary-dark)) !important;
        color: #ffffff !important;
        border-radius: 999px !important;
        border: none !important;
        height: 44px;
        padding: 0 1.35rem;
        font-weight: 600;
        font-size: 0.95rem;
        letter-spacing: 0.01em;
        box-shadow: 0 12px 25px rgba(37, 99, 235, 0.35);
        transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        transform: translateY(-1px) scale(1.01);
        box-shadow: 0 16px 40px rgba(37, 99, 235, 0.5);
        filter: brightness(1.02);
    }

    .stButton > button:active,
    .stDownloadButton > button:active {
        transform: translateY(0);
        box-shadow: 0 8px 18px rgba(15, 23, 42, 0.3);
    }

    .stButton > button:focus-visible {
        outline: 2px solid rgba(191, 219, 254, 0.9) !important;
        outline-offset: 3px !important;
    }

    /* ---------- METRIC CARDS ---------- */
    div[data-testid="metric-container"] {
        border-radius: var(--sc-radius-lg);
        padding: 1.1rem 1.25rem;
        background: linear-gradient(145deg, #ffffff, #f9fafb);
        border: 1px solid rgba(148, 163, 184, 0.26);
        box-shadow: var(--sc-shadow-soft);
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    }

    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 22px 55px rgba(15, 23, 42, 0.15);
        border-color: rgba(37, 99, 235, 0.45);
    }

    div[data-testid="metric-container"] > label {
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #9ca3af;
    }

    /* ---------- DATAFRAMES & TABLES ---------- */
    [data-testid="stDataFrame"] {
        background: var(--sc-card-bg);
        border-radius: var(--sc-radius-md);
        box-shadow: var(--sc-shadow-soft);
        padding: 0.5rem 0.75rem;
        border: 1px solid rgba(148, 163, 184, 0.25);
    }

    [data-testid="stDataFrame"] table {
        border-collapse: collapse;
        width: 100%;
        font-size: 0.88rem;
    }

    [data-testid="stDataFrame"] thead tr {
        background: #f3f4f6;
    }

    [data-testid="stDataFrame"] th,
    [data-testid="stDataFrame"] td {
        border-bottom: 1px solid #e5e7eb;
        padding: 0.4rem 0.6rem;
    }

    [data-testid="stDataFrame"] tbody tr:hover {
        background: #f9fafb;
    }

    /* ---------- MISC / SMALL DETAILS ---------- */
    hr {
        border-color: rgba(148, 163, 184, 0.35);
    }

    /* Hide default Streamlit footer & menu for a cleaner app view */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    </style>
    """, unsafe_allow_html=True)
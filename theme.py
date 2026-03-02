import streamlit as st

def apply_theme():

    st.markdown("""
    <style>

    /* ---------- MAIN BACKGROUND ---------- */
    .stApp {
        background-color: #f5f7fb;
    }

    /* ---------- SIDEBAR ---------- */
    section[data-testid="stSidebar"] {
        background-color: white;
        border-right:1px solid #e5e7eb;
    }

    /* ---------- BUTTON FIX ---------- */
    .stButton button {
        background-color:#2563eb !important;
        color:white !important;
        border-radius:10px;
        height:45px;
        font-weight:600;
        border:none;
        transition:0.3s;
    }

    .stButton button:hover {
        background-color:#1e40af !important;
        transform:scale(1.05);
    }

    /* ---------- INPUT BOX ---------- */
    input, textarea, select {
        background:white !important;
        color:black !important;
        border-radius:8px !important;
    }

    /* ---------- METRIC CARDS ---------- */
    div[data-testid="metric-container"] {
        background:white;
        padding:18px;
        border-radius:14px;
        box-shadow:0 4px 15px rgba(0,0,0,0.08);
    }

    /* ---------- DATAFRAME ---------- */
    [data-testid="stDataFrame"] {
        background:white;
        border-radius:10px;
    }

    /* ---------- TEXT COLOR ---------- */
    h1,h2,h3,h4,p,label {
        color:#111827;
    }

    </style>
    """, unsafe_allow_html=True)
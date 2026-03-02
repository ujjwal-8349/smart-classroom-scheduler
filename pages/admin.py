import streamlit as st
import pandas as pd
import plotly.express as px
from database import create_connection

st.set_page_config(layout="wide")

st.title("📊 Admin Dashboard")

# ---------- TOP CARDS ----------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Classrooms", 45, "+2")
col2.metric("Active Faculty", 128, "+5")
col3.metric("Total Subjects", 89, "+12")
col4.metric("Active Schedules", 23, "+3")

st.divider()

# ---------- GRAPH DATA ----------
def get_weekly_utilization():

    conn = create_connection()
    cursor = conn.cursor()

    days = ["Monday","Tuesday","Wednesday","Thursday","Friday"]

    result = []

    for day in days:

        cursor.execute(
            "SELECT COUNT(*) FROM timetable WHERE day=?",
            (day,)
        )

        booked = cursor.fetchone()[0]

        total_slots = 5 * 5   # rooms × slots (adjust later)

        utilization = (booked / total_slots) * 100 if total_slots else 0

        result.append((day[:3], utilization))

    conn.close()
    return result
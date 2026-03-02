import streamlit as st
import pandas as pd
import plotly.express as px
from auth_guard import check_login
check_login("Admin")
from theme import apply_theme
apply_theme()

from database import (
    get_faculty_count,
    get_classroom_count,
    get_student_count,
    get_attendance_summary,
    get_faculty_by_department,
    get_classroom_types
)

st.markdown("""
<h1 style='text-align:center;
color:#00C2FF;
text-shadow:0px 0px 20px #00C2FF;'>
SMART CLASSROOM ANALYTICS
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align:center;
color:#2563eb;
font-weight:700;'>
🏫 SMART CLASSROOM & TIMETABLE SCHEDULER
</h1>
<hr>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
background:linear-gradient(90deg,#2563eb,#06b6d4);
padding:25px;
border-radius:15px;
color:white;
text-align:center;
box-shadow:0px 4px 20px rgba(0,0,0,0.1);
">
<h1>🏫 Smart Classroom & Timetable Scheduler</h1>
<p>AI Powered Academic Management System</p>
</div>
<br>
""", unsafe_allow_html=True)



st.set_page_config(layout="wide")

st.title("📊 Admin Dashboard")
st.write("Welcome to Smart Classroom Admin Panel")

# ---------- PREMIUM ANIMATED METRIC CARDS ----------

import time

col1, col2, col3, col4 = st.columns(4)

faculty = get_faculty_count()
students = get_student_count()
rooms = get_classroom_count()
schedules = len(get_attendance_summary())


def premium_metric(column, title, value, icon, color):

    placeholder = column.empty()

    for i in range(value + 1):

        placeholder.markdown(f"""
        <div style="
            background:white;
            padding:20px;
            border-radius:15px;
            box-shadow:0 4px 15px rgba(0,0,0,0.08);
            text-align:center;
            border-top:5px solid {color};
        ">
            <h4>{icon} {title}</h4>
            <h1 style="color:{color};">{i}</h1>
        </div>
        """, unsafe_allow_html=True)

        time.sleep(0.015)


premium_metric(col1, "Faculty", faculty, "👨‍🏫", "#2563eb")
premium_metric(col2, "Students", students, "🎓", "#16a34a")
premium_metric(col3, "Classrooms", rooms, "🏫", "#f59e0b")
premium_metric(col4, "Schedules", schedules, "📅", "#db2777")


st.divider()
st.subheader("📊 Attendance Overview")

# Attendance

# attendance = get_attendance_summary()

# if attendance:

#     subjects = []
#     percentage = []

#     for sub, total, present in attendance:
#         percent = (present / total) * 100 if total else 0
#         subjects.append(sub)
#         percentage.append(percent)

#     df = pd.DataFrame({
#         "Subject": subjects,
#         "Attendance %": percentage
#     })

#     fig = px.bar(
#         df,
#         x="Subject",
#         y="Attendance %",
#         title="Overall Attendance Percentage"
#     )

#     st.plotly_chart(fig, use_container_width=True)

# else:
#     st.info("No attendance data available")
    
# ---------- PREMIUM ANIMATED METRIC CARDS ----------

st.markdown("""
<hr style="border:1px solid #e5e7eb;">
<h3 style="color:#2563eb;">📊 Analytics Overview</h3>
""", unsafe_allow_html=True)

# -------- FACULTY GRAPH --------
faculty_data = get_faculty_by_department()

if faculty_data and len(faculty_data) > 0:
    df_faculty = pd.DataFrame(
        faculty_data,
        columns=["Department", "Faculty Count"]
    )

    fig1 = px.bar(
        df_faculty,
        x="Department",
        y="Faculty Count",
        title="Faculty Distribution by Department"
    )

    st.plotly_chart(fig1, use_container_width=True)


# -------- CLASSROOM GRAPH --------
classroom_data = get_classroom_types()

if classroom_data and len(classroom_data) > 0:
    df_classroom = pd.DataFrame(
        classroom_data,
        columns=["Type", "Count"]
    )

    fig2 = px.pie(
        df_classroom,
        names="Type",
        values="Count",
        title="Classroom Type Distribution"
    )

    st.plotly_chart(fig2, use_container_width=True)



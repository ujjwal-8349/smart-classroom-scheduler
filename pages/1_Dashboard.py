import streamlit as st
import pandas as pd
import plotly.express as px
from auth_guard import check_login
check_login("Admin")

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


st.set_page_config(layout="wide")

st.title("📊 Admin Dashboard")
st.write("Welcome to Smart Classroom Admin Panel")

# ---------- METRIC CARDS ----------
import time
import random

col1, col2, col3, col4 = st.columns(4)

faculty = get_faculty_count()
students = get_student_count()
rooms = get_classroom_count()

def animated_metric(col, label, value):

    placeholder = col.empty()

    for i in range(value + 1):
        placeholder.metric(
            label,
            i,
            delta=f"+{random.randint(1,5)}"
        )
        time.sleep(0.02)

animated_metric(col1, "👨‍🏫 Faculty", faculty)
animated_metric(col2, "👨‍🎓 Students", students)
animated_metric(col3, "🏫 Classrooms", rooms)
animated_metric(col4, "📅 Schedules", len(get_attendance_summary()))


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



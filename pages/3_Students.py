import streamlit as st
import pandas as pd
import plotly.express as px

from database import (
    add_student,
    get_student_timetable,
    get_student_attendance_percentage,
)
from auth_guard import check_login
from theme import apply_theme

check_login(["Admin", "Faculty", "Student"])
apply_theme()

st.title("👨‍🎓 Students")

# ================= ADMIN VIEW =================
if st.session_state.get("role") == "Admin":

    st.subheader("Add Student")

    with st.form("student_form"):

        name = st.text_input("Student Name")
        department = st.text_input("Department")

        submit = st.form_submit_button("Add Student")

    if submit:

        username = name.lower().replace(" ", "")
        password = "stu123"

        add_student(name, department)

        st.success(
            f"Student Added ✅ Login ID: {username} | Password: {password}"
        )

# ================= STUDENT VIEW =================
elif st.session_state.get("role") == "Student":

    username = st.session_state.get("username")
    department = st.session_state.get("department")

    # -------- My Timetable --------
    st.subheader("📅 My Timetable")

    timetable_data = get_student_timetable(department)

    if timetable_data:
        for row in timetable_data:
            st.write(row)
    else:
        st.info("No timetable data for your department.")

    # -------- My Attendance --------
    st.divider()
    st.subheader("📊 My Attendance")

    attendance = get_student_attendance_percentage(username)

    if attendance:

        subjects = [a[0] for a in attendance]
        percent = [a[1] for a in attendance]

        df = pd.DataFrame({
            "Subject": subjects,
            "Attendance %": percent,
        })

        fig = px.bar(
            df,
            x="Subject",
            y="Attendance %",
            title="My Attendance Percentage",
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No attendance data available.")

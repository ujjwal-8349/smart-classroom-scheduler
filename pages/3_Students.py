import streamlit as st
import pandas as pd
import plotly.express as px
from database import (
    add_student,
    get_student_timetable,
    get_low_attendance
)
from auth_guard import check_login
check_login()
from theme import apply_theme
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

    st.subheader("📅 My Timetable")

    data = get_student_timetable(
        st.session_state.get("department")
    )

    for row in data:
        st.write(row)

    # -------- Attendance Alert --------
    st.divider()
    st.subheader("⚠️ Attendance Alerts")

    low = get_low_attendance(username)

    if low:
        for sub, percent in low:
            st.warning(
                f"{sub} attendance low ({percent:.1f}%)"
            )
    else:
        st.success("✅ Attendance Safe")

else:
    st.warning("Login again")
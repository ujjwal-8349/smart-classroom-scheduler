import streamlit as st
import pandas as pd
import plotly.express as px
from database import (
    add_student,
    get_student_timetable,
    get_low_attendance
)
from auth_guard import check_login
check_login(["Admin","Faculty","Student"])
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
    import plotly.express as px
from database import get_student_attendance_percentage

st.divider()
st.subheader("📊 My Attendance")

username = st.session_state.get("username")

attendance = get_student_attendance_percentage(username)

if attendance:

    subjects = [a[0] for a in attendance]
    percent = [a[1] for a in attendance]

    import pandas as pd

    df = pd.DataFrame({
        "Subject": subjects,
        "Attendance %": percent
    })

    fig = px.bar(
        df,
        x="Subject",
        y="Attendance %",
        title="My Attendance Percentage"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("No attendance data available")
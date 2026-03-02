import streamlit as st
from database import (
    mark_attendance,
    get_students,
    get_subject_names
)
from auth_guard import check_login
check_login(["Admin","Faculty"])

import streamlit as st

if st.session_state.get("role") != "Faculty":
    st.warning("Only Faculty Allowed ❌")
    st.stop()

st.title("📋 Mark Attendance")

students = get_students()
subjects = get_subject_names()

student = st.selectbox("Select Student", students)
subject = st.selectbox("Select Subject", subjects)

status = st.radio(
    "Attendance Status",
    ["Present", "Absent"]
)

if st.button("Submit Attendance"):

    username = student.lower().replace(" ","")

    mark_attendance(username, subject, status)

    st.success("Attendance Marked ✅")
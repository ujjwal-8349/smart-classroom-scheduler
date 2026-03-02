import streamlit as st
from database import (
    mark_attendance,
    get_students,
    get_subject_names
)

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
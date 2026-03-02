import streamlit as st
from database import add_subject, get_subjects
from database import get_low_attendance

st.title("📘 Subject Management")

with st.form("subject_form"):

    name = st.text_input("Subject Name")
    department = st.text_input("Department")

    subject_type = st.selectbox(
        "Subject Type",
        ["Theory", "Lab"]
    )

    faculty = st.text_input("Faculty Name")

    submit = st.form_submit_button("Add Subject")

if submit:
    add_subject(name, department, subject_type, faculty)
    st.success("Subject Added ✅")

st.divider()

subjects = get_subjects()

for s in subjects:
    st.write(s)
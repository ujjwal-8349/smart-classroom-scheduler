import streamlit as st
from database import add_faculty, get_faculty_count, add_user
from auth_guard import check_login
check_login("Admin")

st.title("👨‍🏫 Faculty Management")

with st.form("faculty_form"):

    name = st.text_input("Faculty Name")
    department = st.text_input("Department")
    subject = st.text_input("Subject")

    submit = st.form_submit_button("Add Faculty")

if submit:

    username = name.lower().replace(" ", "")
    password = "fac123"

    # Faculty table
    add_faculty(name, department, subject)

    # Login table
    add_user(username, password, "Faculty")

    st.success(
        f"Faculty Added ✅\nLogin ID: {username}\nPassword: {password}"
    )


st.divider()

count = get_faculty_count()
st.metric("Total Faculty", count)
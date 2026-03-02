import streamlit as st
import pandas as pd

from database import (
    add_faculty,
    get_faculty_count,
    add_user,
    get_all_faculty,
    delete_faculty,
    update_faculty
)

from auth_guard import check_login
from theme import apply_theme

check_login(["Admin","Faculty"])
apply_theme()

st.title("👨‍🏫 Faculty Management")

# ---------- ADD FACULTY ----------
with st.form("faculty_form"):

    name = st.text_input("Faculty Name")
    department = st.text_input("Department")
    subject = st.text_input("Subject")

    submit = st.form_submit_button("Add Faculty")

if submit:

    username = name.lower().replace(" ", "")
    password = "fac123"

    add_faculty(name, department, subject)
    add_user(username, password, "Faculty")

    st.success(
        f"Faculty Added ✅\nLogin ID: {username}\nPassword: {password}"
    )

# ---------- COUNT ----------
st.divider()
count = get_faculty_count()
st.metric("Total Faculty", count)

# ---------- FACULTY LIST ----------
st.subheader("📋 Faculty List")

faculty_data = get_all_faculty()

df = pd.DataFrame(
    faculty_data,
    columns=["ID","Name","Department","Subject"]
)

for _, row in df.iterrows():

    col1, col2, col3, col4, col5 = st.columns([2,2,2,1,1])

    col1.write(row["Name"])
    col2.write(row["Department"])
    col3.write(row["Subject"])

    if col4.button("✏ Edit", key=f"edit_{row['ID']}"):
        st.session_state.edit_faculty = row["ID"]

    if col5.button("🗑 Delete", key=f"delete_{row['ID']}"):
        delete_faculty(row["ID"])
        st.success("Faculty Deleted ✅")
        st.rerun()

# ---------- EDIT SECTION (OUTSIDE LOOP) ----------
if "edit_faculty" in st.session_state:

    fid = st.session_state.edit_faculty

    st.divider()
    st.subheader("✏ Edit Faculty")

    new_name = st.text_input("New Name")
    new_dept = st.text_input("New Department")
    new_subject = st.text_input("New Subject")

    if st.button("Update Faculty"):

        update_faculty(fid, new_name, new_dept, new_subject)

        del st.session_state.edit_faculty
        st.success("Updated Successfully ✅")
        st.rerun()
import streamlit as st
from database import create_tables, insert_default_users
from auth import login_user

# ---------------- INITIAL SETUP ----------------
create_tables()
insert_default_users()

st.set_page_config(page_title="Smart Classroom Scheduler")

# ---------------- LOGIN PAGE ----------------
st.title("🏫 Smart Classroom & Timetable Scheduler")

with st.form("login_form"):

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    role = st.selectbox(
        "Login As",
        ["Admin", "Faculty", "Student"]
    )

    login_btn = st.form_submit_button("Login")


# ---------------- LOGIN CHECK ----------------
if login_btn:

    user = login_user(username, password, role)

    if user:

        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.session_state["role"] = role

        st.success("Login Successful ✅")

        if role == "Admin":
            st.switch_page("pages/1_Dashboard.py")

        elif role == "Faculty":
            st.switch_page("pages/2_Faculty.py")

        elif role == "Student":
            st.switch_page("pages/3_Students.py")

        else:
            st.error("Invalid Username or Password ❌")
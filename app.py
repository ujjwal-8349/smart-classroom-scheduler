import streamlit as st
from database import create_tables, insert_default_users
from auth import login_user
from theme import apply_theme
apply_theme()

st.markdown("""
<h1 style='text-align:center;
color:#2563eb;
font-weight:700;'>
🏫 SMART CLASSROOM & TIMETABLE SCHEDULER
</h1>
<hr>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="text-align:center">
<h2>🎓 Smart Classroom</h2>
<p>AI Scheduler</p>
</div>
<hr>
""", unsafe_allow_html=True)

# # ---------------- INITIAL SETUP ----------------
# create_tables()
# insert_default_users()

# st.set_page_config(
#     page_title="Smart Classroom Scheduler",
#     page_icon="🏫",
#     layout="wide",
#     initial_sidebar_state="expanded"
#     )

# ---------------- LOGIN PAGE ----------------
st.title("🏫 Smart Classroom & Timetable Scheduler")

login_card = st.container()
with login_card:

    st.subheader("Sign in to your dashboard")
    st.caption("Use your assigned credentials to access Smart Classroom features.")

    with st.form("login_form"):

        col_user, col_role = st.columns([2, 1])

        with col_user:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

        with col_role:
            role = st.selectbox(
                "Login As",
                ["Admin", "Faculty", "Student"]
            )

        st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
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


role = st.session_state.get("role")

if role == "Student":
    st.session_state.hide_admin = True
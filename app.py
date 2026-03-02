import streamlit as st
from database import create_tables, insert_default_users
from auth import login_user
st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #f5f7fb;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e6e6e6;
}

/* Cards */
div[data-testid="metric-container"] {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}

/* Buttons */
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    height: 45px;
    font-weight: 600;
}

.stButton>button:hover {
    background-color: #1e40af;
}

/* Headers */
h1, h2, h3 {
    color: #111827;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align:center;
color:#2563eb;
font-weight:700;'>
🏫 SMART CLASSROOM & TIMETABLE SCHEDULER
</h1>
<hr>
""", unsafe_allow_html=True)

# ---------------- INITIAL SETUP ----------------
create_tables()
insert_default_users()

st.set_page_config(
    page_title="Smart Classroom Scheduler",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
    )

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
import streamlit as st

def check_login(required_role=None):

    # not logged in
    if "role" not in st.session_state:
        st.warning("⚠️ Please login first")
        st.switch_page("app.py")

    # role protection
    if required_role:
        if st.session_state["role"] != required_role:
            st.error("🚫 Unauthorized Access")
            st.switch_page("app.py")
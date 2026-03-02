import streamlit as st

def check_login(allowed_roles=None):

    if "role" not in st.session_state:
        st.warning("Please login first")
        st.switch_page("app.py")

    if allowed_roles:

        if isinstance(allowed_roles, str):
            allowed_roles = [allowed_roles]

        if st.session_state.get("role") not in allowed_roles:
            st.error("Unauthorized Access ❌")
            st.stop()
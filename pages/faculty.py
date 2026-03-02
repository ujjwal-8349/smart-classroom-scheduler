import streamlit as st

st.title("Faculty Dashboard")
st.write("Welcome Faculty 👨‍🏫")
from auth_guard import check_login
check_login("Faculty")
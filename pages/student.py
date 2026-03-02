import streamlit as st

st.title("Student Dashboard")
st.write("Welcome Student 🎓")
from auth_guard import check_login
check_login("Faculty")
import streamlit as st
from database import add_classroom, get_classroom_count
from theme import apply_theme
apply_theme()

st.title("🏫 Classroom Management")

with st.form("classroom_form"):

    room = st.text_input("Room Number")

    capacity = st.number_input(
        "Capacity",
        min_value=1,
        step=1
    )

    room_type = st.selectbox(
        "Room Type",
        ["Theory", "Lab"]
    )

    submit = st.form_submit_button("Add Classroom")

if submit:
    add_classroom(room, capacity, room_type)
    st.success("Classroom Added Successfully ✅")

st.divider()

st.subheader("Total Classrooms")

count = get_classroom_count()
st.metric("Classroom Count", count)
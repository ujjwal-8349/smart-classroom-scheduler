import streamlit as st
from database import (
    get_days,
    get_timeslots,
    get_free_classrooms
)
from theme import apply_theme
apply_theme()

st.set_page_config(layout="wide")

st.title("🏫 Live Free Classroom Finder")

st.markdown("Check real-time available classrooms based on timetable")

# ---------- SELECTION ----------
col1, col2 = st.columns(2)

with col1:
    day = st.selectbox("📅 Select Day", get_days())

with col2:
    slot = st.selectbox("⏰ Select Time Slot", get_timeslots())


# ---------- CHECK BUTTON ----------
if st.button("🔍 Check Free Classrooms"):

    rooms = get_free_classrooms(day, slot)

    st.divider()

    if rooms:

        st.success(f"✅ {len(rooms)} Classrooms Available")

        cols = st.columns(4)

        for i, room in enumerate(rooms):

            cols[i % 4].markdown(f"""
            <div style="
                background:#111827;
                padding:15px;
                border-radius:12px;
                border-left:5px solid #22c55e;
                text-align:center;
                margin-bottom:10px;
                font-size:18px;
                ">
                🏫 <b>{room}</b><br>
                <span style="color:#22c55e;">
                Free
                </span>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.error("❌ No Free Classroom Available")
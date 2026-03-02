import streamlit as st
import pandas as pd
import random
import time
from theme import apply_theme
apply_theme()

from database import (
    save_safe_timetable,
    get_subjects,
    get_classrooms_by_type,
    get_timeslots,
    get_days,
    get_timetable,
    clear_timetable
)

st.title("🧠 Smart Timetable Generator")

# ================= AI TIMETABLE GENERATION =================

if st.button("🤖 Generate AI Timetable"):

    with st.spinner("AI analysing academic constraints..."):

        clear_timetable()

        subjects = get_subjects()
        days = get_days()
        slots = get_timeslots()

        faculty_load = {}

        for day in days:

            i = 0

            while i < len(slots):

                slot = slots[i]

                subject = random.choice(subjects)

                subject_name = subject[0]
                department = subject[1]
                subject_type = subject[2]
                faculty = subject[3]

                faculty_load.setdefault(faculty, 0)

                # ---------- Faculty overload protection ----------
                if faculty_load[faculty] > 3:
                    i += 1
                    continue

                rooms = get_classrooms_by_type(subject_type)

                if not rooms:
                    i += 1
                    continue

                room = random.choice(rooms)[0]

                saved = save_safe_timetable(
                    day,
                    slot,
                    subject_name,
                    faculty,
                    room,
                    department
                )

                # ---------- SUCCESS ----------
                if saved:

                    faculty_load[faculty] += 1

                    # ===== LAB CONTINUOUS SLOT =====
                    if subject_type == "Lab" and i + 1 < len(slots):

                        next_slot = slots[i + 1]

                        save_safe_timetable(
                            day,
                            next_slot,
                            subject_name,
                            faculty,
                            room,
                            department
                        )

                        i += 2   # skip next slot

                    else:
                        i += 1

                else:
                    i += 1

        time.sleep(2)

    st.success("✅ AI Generated Optimized Timetable")


# ================= PREMIUM TIMETABLE VIEW =================

st.divider()
selected_day = st.selectbox(
    "📅 Select Day",
    get_days()
)
st.subheader(f"📅 Timetable - {selected_day}")

data = get_timetable()

# Filter by selected day
data = [row for row in data if row[0] == selected_day]

if data:

    df = pd.DataFrame(
        data,
        columns=[
            "Day",
            "Slot",
            "Subject",
            "Faculty",
            "Room",
            "Department"
        ]
    )

    days_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday"
    ]

    slots_order = [
        "9:00-10:00",
        "10:00-11:00",
        "11:00-12:00",
        "1:00-2:00",
        "2:00-3:00"
    ]

    df["Day"] = pd.Categorical(df["Day"], days_order)
    df["Slot"] = pd.Categorical(df["Slot"], slots_order)

    df = df.sort_values(["Slot", "Day"])

    # ---------- CARD GRID ----------
    for slot in slots_order:

        st.markdown(f"### ⏰ {slot}")

        cols = st.columns(len(days_order))

        for idx, day in enumerate(days_order):

            row = df[
                (df["Day"] == day) &
                (df["Slot"] == slot)
            ]

            if not row.empty:

                subject = row.iloc[0]["Subject"]
                faculty = row.iloc[0]["Faculty"]
                room = row.iloc[0]["Room"]

                # Lab Highlight Color
                border = "#22c55e"
                if "lab" in subject.lower():
                    border = "#f59e0b"

                cols[idx].markdown(f"""
                <div style="
                    background:#111827;
                    padding:15px;
                    border-radius:12px;
                    border-left:6px solid {border};
                    text-align:center;
                    box-shadow:0px 4px 12px rgba(0,0,0,0.4);
                ">
                <b>{subject}</b><br>
                👨‍🏫 {faculty}<br>
                🏫 {room}
                </div>
                """, unsafe_allow_html=True)

            else:
                cols[idx].markdown("""
                <div style="
                    background:#1f2937;
                    padding:15px;
                    border-radius:12px;
                    text-align:center;
                    opacity:0.6;
                ">
                Free
                </div>
                """, unsafe_allow_html=True)

else:
    st.info("Generate timetable first ✅")
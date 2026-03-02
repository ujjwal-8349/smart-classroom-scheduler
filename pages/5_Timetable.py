import streamlit as st
import pandas as pd
from database import get_timetable
from auth_guard import check_login
from theme import apply_theme

# ---------- LOGIN ----------
check_login(["Admin","Faculty","Student"])

# ---------- THEME ----------
apply_theme()

st.title("📅 Weekly Timetable")

# ---------- FETCH DATA ----------
data = get_timetable()

days = ["Monday","Tuesday","Wednesday","Thursday","Friday"]

slots = [
    "9:00-10:00",
    "10:00-11:00",
    "11:00-12:00",
    "1:00-2:00",
    "2:00-3:00"
]

# ---------- EMPTY TABLE ----------
table = pd.DataFrame("", index=days, columns=slots)

# ---------- FILL DATA ----------
for day, slot, subject, faculty, room in data:

    table.loc[day, slot] = (
        f"{subject}\n"
        f"{faculty}\n"
        f"{room}"
    )

# ---------- DISPLAY ----------
st.dataframe(
    table,
    use_container_width=True,
    height=450
)
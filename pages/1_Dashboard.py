import streamlit as st
import pandas as pd
import plotly.express as px
from auth_guard import check_login
from theme import apply_theme
from database import (
    get_faculty_count,
    get_classroom_count,
    get_student_count,
    get_attendance_summary,
    get_faculty_by_department,
    get_classroom_types,
)

st.set_page_config(layout="wide")
check_login(["Admin", "Faculty", "Student"])
apply_theme()

# ---------- HERO HEADER ----------
st.markdown(
    """
    <div style="
        padding: 1.4rem 1.6rem;
        border-radius: 1.2rem;
        background: radial-gradient(circle at top left, #dbeafe 0, #eff6ff 42%, #ffffff 100%);
        border: 1px solid rgba(148, 163, 184, 0.35);
        box-shadow: 0 18px 55px rgba(15, 23, 42, 0.12);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1.5rem;
        margin-bottom: 1.8rem;
    ">
      <div style="flex: 1;">
        <div style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.16em; color:#6b7280; margin-bottom: 0.35rem;">
          SMART CLASSROOM · OVERVIEW
        </div>
        <h1 style="margin: 0; font-size: 1.9rem; color:#111827;">
          📊 Admin Analytics Dashboard
        </h1>
        <p style="margin: 0.4rem 0 0; color:#6b7280; font-size: 0.95rem;">
          Monitor classrooms, faculty, and students at a glance with live insights.
        </p>
      </div>
      <div style="
        padding: 0.85rem 1.15rem;
        border-radius: 999px;
        background: rgba(37, 99, 235, 0.06);
        border: 1px solid rgba(129, 140, 248, 0.55);
        font-size: 0.85rem;
        color:#1d4ed8;
        display: flex;
        align-items: center;
        gap: 0.4rem;
        white-space: nowrap;
      ">
        <span>⚡</span><span>Real‑time academic snapshot</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- PREMIUM ANIMATED METRIC CARDS ----------

import time

col1, col2, col3, col4 = st.columns(4)

faculty = get_faculty_count()
students = get_student_count()
rooms = get_classroom_count()
schedules = len(get_attendance_summary())


def premium_metric(column, title, value, icon, color):

    placeholder = column.empty()

    for i in range(value + 1):

        placeholder.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #ffffff, #eff6ff);
            padding: 18px 18px 16px;
            border-radius: 18px;
            box-shadow: 0 16px 40px rgba(15, 23, 42, 0.12);
            text-align:center;
            border-top: 4px solid {color};
            border-inline: 1px solid rgba(148, 163, 184, 0.35);
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position:absolute;
                inset:0;
                background: radial-gradient(circle at top right, rgba(37,99,235,0.12), transparent 58%);
                opacity:0.75;
                pointer-events:none;
            "></div>
            <div style="position:relative; z-index:1;">
              <div style="font-size: 0.9rem; color:#6b7280; margin-bottom: 0.15rem;">
                {icon} <span style="font-weight: 600; color:#111827;">{title}</span>
              </div>
              <div style="font-size: 1.7rem; font-weight: 700; color:{color}; line-height: 1.2;">
                {i}
              </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        time.sleep(0.015)


premium_metric(col1, "Faculty", faculty, "👨‍🏫", "#2563eb")
premium_metric(col2, "Students", students, "🎓", "#16a34a")
premium_metric(col3, "Classrooms", rooms, "🏫", "#f59e0b")
premium_metric(col4, "Schedules", schedules, "📅", "#db2777")

st.markdown("<div style='margin: 1.8rem 0 0.8rem;'></div>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:0.4rem;">
      <h3 style="margin:0; color:#111827; font-size:1.2rem;">📈 Resource & Classroom Analytics</h3>
      <span style="font-size:0.8rem; text-transform:uppercase; letter-spacing:0.16em; color:#9ca3af;">
        OVERVIEW
      </span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr style='border:1px solid rgba(148,163,184,0.35); margin:0.4rem 0 1.1rem;' />", unsafe_allow_html=True)

# -------- FACULTY & CLASSROOM GRAPHS --------
faculty_data = get_faculty_by_department()
classroom_data = get_classroom_types()

col_left, col_right = st.columns(2)

with col_left:
    if faculty_data and len(faculty_data) > 0:
        df_faculty = pd.DataFrame(
            faculty_data,
            columns=["Department", "Faculty Count"],
        )

        fig1 = px.bar(
            df_faculty,
            x="Department",
            y="Faculty Count",
            title="👨‍🏫 Faculty by Department",
            color_discrete_sequence=["#2563eb"],
        )
        fig1.update_layout(
            template="plotly_white",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=60, l=40, r=10, b=40),
            xaxis_title="Department",
            yaxis_title="Faculty Count",
        )

        st.plotly_chart(fig1, use_container_width=True)

with col_right:
    if classroom_data and len(classroom_data) > 0:
        df_classroom = pd.DataFrame(
            classroom_data,
            columns=["Type", "Count"],
        )

        fig2 = px.pie(
            df_classroom,
            names="Type",
            values="Count",
            title="🏫 Classroom Type Distribution",
            hole=0.45,
            color_discrete_sequence=px.colors.sequential.Blues_r,
        )
        fig2.update_layout(
            template="plotly_white",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=60, l=10, r=10, b=20),
            legend_title_text="Room Type",
        )

        st.plotly_chart(fig2, use_container_width=True)

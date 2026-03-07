import streamlit as st
import pandas as pd
from typing import Optional
from database import (
    clear_timetable,
    create_connection,
    get_days,
    get_timeslots,
    get_timetable,
    save_safe_timetable,
)
from auth_guard import check_login
from theme import apply_theme

# ---------- LOGIN ----------
check_login(["Admin","Faculty","Student"])

# ---------- THEME ----------
apply_theme()

st.title("📅 Weekly Timetable")

days = get_days()
slots = get_timeslots()


def _fetch_departments():
    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT department
            FROM subjects
            WHERE department IS NOT NULL AND department <> ''
            ORDER BY department
        """)
        return [r[0] for r in cursor.fetchall()]
    finally:
        if conn:
            conn.close()


def _fetch_subject_rows(department: str):
    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, type, faculty
            FROM subjects
            WHERE department=%s
            ORDER BY id
        """, (department,))
        return cursor.fetchall()  # [(name, type, faculty), ...]
    finally:
        if conn:
            conn.close()


def _fetch_rooms_by_type(room_type: str):
    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT room FROM classrooms WHERE type=%s ORDER BY id",
            (room_type,),
        )
        return [r[0] for r in cursor.fetchall()]
    finally:
        if conn:
            conn.close()


def _fetch_timetable_rows(department: Optional[str]):
    if not department or department == "All":
        return get_timetable()

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT day, slot, subject, faculty, room
            FROM timetable
            WHERE department=%s
        """, (department,))
        return cursor.fetchall()
    finally:
        if conn:
            conn.close()


def _generate_timetable_for_department(department: str) -> int:
    """
    Generates a dense timetable for one department using:
    - `subjects` table: (subject name, subject type, faculty name)
    - `classrooms` table: rooms filtered by type (Theory/Lab)
    Saves rows via `save_safe_timetable` to avoid faculty/room clashes.
    Returns number of rows successfully saved.
    """
    subjects = _fetch_subject_rows(department)
    if not subjects:
        return 0

    theory_rooms = _fetch_rooms_by_type("Theory")
    lab_rooms = _fetch_rooms_by_type("Lab")
    fallback_rooms = theory_rooms + [r for r in lab_rooms if r not in theory_rooms]

    saved = 0
    subject_idx = 0

    for day in days:
        for slot in slots:
            # Try a few candidates to minimize empty slots.
            placed = False
            attempts = min(len(subjects) * 2, 30)

            for _ in range(attempts):
                name, subj_type, faculty = subjects[subject_idx % len(subjects)]
                subject_idx += 1

                candidate_rooms = theory_rooms if subj_type == "Theory" else lab_rooms
                if not candidate_rooms:
                    candidate_rooms = fallback_rooms

                if not candidate_rooms:
                    # No classrooms at all.
                    break

                # Try rooms in a deterministic order to reduce randomness.
                for room in candidate_rooms:
                    if save_safe_timetable(day, slot, name, faculty, room, department):
                        saved += 1
                        placed = True
                        break

                if placed:
                    break

            # If we can't place anything (clashes / no rooms), we leave it empty.
    return saved


def _render_timetable_grid(rows):
    # ---------- EMPTY TABLE ----------
    table = pd.DataFrame("", index=days, columns=slots)

    # ---------- FILL DATA ----------
    for day, slot, subject, faculty, room in rows:
        cell_html = (
            "<div class='tt-card tt-card--filled'>"
            f"<div class='tt-subject'>{subject}</div>"
            f"<div class='tt-meta'><span class='tt-meta-label'>Faculty</span> {faculty}</div>"
            f"<div class='tt-meta'><span class='tt-meta-label'>Room</span> {room}</div>"
            "</div>"
        )
        table.loc[day, slot] = cell_html

    # ---------- MARK FREE SLOTS ----------
    for d in days:
        for s in slots:
            if not str(table.loc[d, s]).strip():
                table.loc[d, s] = (
                    "<div class='tt-card tt-card--free'>"
                    "<div class='tt-free-pill'>Free</div>"
                    "<div class='tt-free-subtext'>No class scheduled</div>"
                    "</div>"
                )

    # ---------- DISPLAY (HTML grid for readability) ----------
    st.markdown(
        """
        <style>
        .timetable-grid table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 8px;
        }
        .timetable-grid th, .timetable-grid td {
            border: none;
            padding: 0;
            vertical-align: top;
            min-width: 140px;
        }
        .timetable-grid th {
            background: linear-gradient(135deg, #eff6ff, #e5e7eb);
            text-align: center;
            padding: 10px 6px;
            font-size: 13px;
            color: #111827;
            border-radius: 12px;
        }
        .timetable-grid td {
            font-size: 13px;
            line-height: 1.3;
        }

        .tt-card {
            border-radius: 14px;
            padding: 10px 11px;
            background: #ffffff;
            border: 1px solid rgba(148, 163, 184, 0.45);
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.10);
            min-height: 82px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .tt-card--filled:hover {
            box-shadow: 0 18px 40px rgba(15, 23, 42, 0.18);
            border-color: rgba(37, 99, 235, 0.65);
        }

        .tt-subject {
            font-weight: 600;
            color: #111827;
            margin-bottom: 4px;
            font-size: 13px;
        }
        .tt-meta {
            font-size: 11px;
            color: #6b7280;
        }
        .tt-meta-label {
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 10px;
            color: #9ca3af;
            margin-right: 4px;
        }

        .tt-card--free {
            background: radial-gradient(circle at top left, #ecfdf5 0, #f9fafb 40%, #ffffff 100%);
            border: 1px dashed rgba(16, 185, 129, 0.75);
            align-items: flex-start;
        }
        .tt-card--free:hover {
            box-shadow: 0 18px 40px rgba(5, 150, 105, 0.25);
        }
        .tt-free-pill {
            display: inline-flex;
            align-items: center;
            padding: 3px 9px;
            border-radius: 999px;
            background: rgba(16, 185, 129, 0.12);
            color: #059669;
            font-size: 11px;
            font-weight: 600;
        }
        .tt-free-subtext {
            margin-top: 4px;
            font-size: 11px;
            color: #6b7280;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<div class='timetable-grid'>{table.to_html(escape=False)}</div>",
        unsafe_allow_html=True,
    )


# ---------- Department filter ----------
departments = _fetch_departments()

default_department = "All"
if st.session_state.get("role") == "Student" and st.session_state.get("department"):
    default_department = st.session_state.get("department")

dept_options = ["All"] + departments if departments else ["All"]
selected_department = st.selectbox(
    "Department",
    dept_options,
    index=dept_options.index(default_department) if default_department in dept_options else 0,
)


# ---------- Admin: generate timetable ----------
if st.session_state.get("role") == "Admin":
    st.divider()
    st.subheader("🛠 Generate Timetable")
    st.caption("Generates a filled timetable using Subjects, Faculty, and Classrooms from the database.")

    col_a, col_b = st.columns([1, 2])
    with col_a:
        regenerate = st.button("Generate / Regenerate")
    with col_b:
        st.write("Tip: add Subjects and Classrooms first to avoid empty cells.")

    if regenerate:
        clear_timetable()

        total_saved = 0
        for dept in departments:
            total_saved += _generate_timetable_for_department(dept)

        st.success(f"Timetable generated ✅ Entries created: {total_saved}")


# ---------- FETCH + DISPLAY ----------
rows = _fetch_timetable_rows(selected_department)
_render_timetable_grid(rows)
import streamlit as st
from database import create_connection


# ---------------- LOGIN FUNCTION ----------------
def login_user(username, password, role):

    conn = create_connection()
    cursor = conn.cursor()

    # Check user credentials
    cursor.execute(
        """
        SELECT * FROM users
        WHERE username=%s AND password=%s AND role=%s
        """,
        (username, password, role)
    )

    user = cursor.fetchone()

    # ---------- STUDENT SESSION ----------
    if user:

        # ✅ SAVE LOGIN SESSION
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.session_state["role"] = role

        # student department
        if role == "Student":
            cursor.execute("""
                SELECT department
                FROM students
                WHERE LOWER(REPLACE(name,' ',''))=%s
            """, (username,))

            dept = cursor.fetchone()

            if dept:
                st.session_state["department"] = dept[0]

    conn.close()

    return user
import psycopg2
import os
from dotenv import load_dotenv

# load .env variables
load_dotenv()

def _close_connection(conn):
    if conn:
        conn.close()

# ---------------- CONNECTION ----------------
def create_connection():

    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        raise Exception("❌ DATABASE_URL not found. Check .env file")

    conn = psycopg2.connect(
        DATABASE_URL,
        sslmode="require"
    )

    return conn

# ---------------- CREATE TABLES ----------------
def create_tables():

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # USERS
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            username TEXT,
            password TEXT,
            role TEXT
        )
        """)

        # FACULTY
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS faculty(
        id SERIAL PRIMARY KEY,
        name TEXT,
        department TEXT,
        subject TEXT
        )
        """)

        # CLASSROOMS
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS classrooms(
            id SERIAL PRIMARY KEY,
            room TEXT,
            capacity INTEGER,
            type TEXT
        )
        """)

        # SUBJECTS
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects(
            id SERIAL PRIMARY KEY,
            name TEXT,
            department TEXT,
            type TEXT,
            faculty TEXT
        )
        """)

        # TIMETABLE
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS timetable(
        id SERIAL PRIMARY KEY,
        day TEXT,
        slot TEXT,
        subject TEXT,
        faculty TEXT,
        room TEXT,
        department TEXT
    )
    """)


        # STUDENTS
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id SERIAL PRIMARY KEY,
        name TEXT,
        department TEXT
    )
    """)
        
        # ATTENDANCE TABLE
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        id SERIAL PRIMARY KEY,
        student TEXT,
        subject TEXT,
        status TEXT
    )
    """)
        
        conn.commit()
    finally:
        _close_connection(conn)


# ---------------- DEFAULT ADMIN ----------------
def insert_default_users():

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=%s",
            ("admin",)
        )

        if not cursor.fetchone():

            cursor.execute(
                """
                INSERT INTO users(username,password,role)
                VALUES(%s,%s,%s)
                """,
                ("admin", "admin123", "Admin")
            )

        conn.commit()
    finally:
        _close_connection(conn)

# ---------------- LOGIN ----------------
def get_user(username, password, role):

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s AND role=%s",
            (username, password, role)
        )

        user = cursor.fetchone()
        return user
    finally:
        _close_connection(conn)


# ---------------- FACULTY ----------------
def add_faculty(name, department, subject):

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Add faculty record
        cursor.execute("""
            INSERT INTO faculty(name, department, subject)
            VALUES(%s,%s,%s)
        """,(name, department, subject))

        # Create login automatically
        username = name.lower().replace(" ", "")
        password = "fac123"

        cursor.execute("""
            INSERT INTO users(username,password,role)
            VALUES(%s,%s,%s)
        """,(username, password, "Faculty"))

        conn.commit()
    finally:
        _close_connection(conn)


def get_faculty_count():

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM faculty")
        count = cursor.fetchone()[0]

        return count
    finally:
        _close_connection(conn)


def get_faculty_by_department():

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT department, COUNT(*)
            FROM faculty
            GROUP BY department
        """)

        data = cursor.fetchall()
        return data
    finally:
        _close_connection(conn)

# New Features
def update_faculty(id, name, department, subject):

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE faculty
            SET name=%s, department=%s, subject=%s
            WHERE id=%s
        """,(name, department, subject, id))

        conn.commit()
    finally:
        _close_connection(conn)


def delete_student(id):

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM students WHERE id=%s",
            (id,)
        )

        conn.commit()
    finally:
        _close_connection(conn)

def update_subject(id, name, department, type, faculty):

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE subjects
            SET name=%s,
                department=%s,
                type=%s,
                faculty=%s
            WHERE id=%s
        """,(name, department, type, faculty, id))

        conn.commit()
    finally:
        _close_connection(conn)

def get_all_faculty():

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, department, subject
            FROM faculty
        """)

        data = cursor.fetchall()
        return data
    finally:
        _close_connection(conn)

def delete_faculty(id):

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM faculty WHERE id=%s",
            (id,)
        )

        conn.commit()
    finally:
        _close_connection(conn)


# ---------------- STUDENTS ----------------
def add_student(name, department):

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # ---------- ADD INTO STUDENTS ----------
        cursor.execute(
            "INSERT INTO students(name, department) VALUES(%s,%s)",
            (name, department)
        )

        # ---------- CREATE LOGIN ----------
        username = name.lower().replace(" ", "")
        password = "stu123"

        cursor.execute(
            "INSERT INTO users(username, password, role) VALUES(%s,%s,%s)",
            (username, password, "Student")
        )

        conn.commit()
    finally:
        _close_connection(conn)


def get_student_count():

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM students")
        count = cursor.fetchone()[0]

        return count
    finally:
        _close_connection(conn)



# ---------------- CLASSROOM ----------------
def add_classroom(room, capacity, room_type):

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO classrooms(room,capacity,type) VALUES(%s,%s,%s)",
            (room, capacity, room_type)
        )

        conn.commit()
    finally:
        _close_connection(conn)


def get_classroom_count():

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM classrooms")
        count = cursor.fetchone()[0]

        return count
    finally:
        _close_connection(conn)


def get_classrooms_by_type(room_type):

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT room FROM classrooms WHERE type=%s",
            (room_type,)
        )

        data = cursor.fetchall()
        return data
    finally:
        _close_connection(conn)


def get_classroom_types():

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT type, COUNT(*)
            FROM classrooms
            GROUP BY type
        """)

        data = cursor.fetchall()
        return data
    finally:
        _close_connection(conn)


# ---------------- SUBJECT ----------------
def add_subject(name, department, subject_type, faculty):

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO subjects(name,department,type,faculty) VALUES(%s,%s,%s,%s)",
            (name, department, subject_type, faculty)
        )

        conn.commit()
    finally:
        _close_connection(conn)


def get_subjects():

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name, department, type, faculty FROM subjects"
        )

        data = cursor.fetchall()
        return data
    finally:
        _close_connection(conn)


# ---------------- TIMETABLE ----------------
def save_timetable(day, slot, subject, room, department):

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO timetable(day,slot,subject,room,department) VALUES(%s,%s,%s,%s,%s)",
            (day, slot, subject, room, department)
        )

        conn.commit()
    finally:
        _close_connection(conn)


def clear_timetable():

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM timetable")

        conn.commit()
    finally:
        _close_connection(conn)


def get_timetable():

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT day, slot, subject, faculty, room
            FROM timetable
            ORDER BY
            CASE day
                WHEN 'Monday' THEN 1
                WHEN 'Tuesday' THEN 2
                WHEN 'Wednesday' THEN 3
                WHEN 'Thursday' THEN 4
                WHEN 'Friday' THEN 5
            END,
            slot
        """)

        data = cursor.fetchall()
        return data
    finally:
        _close_connection(conn)


def get_student_timetable(department):

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT day, slot, subject, room FROM timetable WHERE department=%s",
            (department,)
        )

        data = cursor.fetchall()
        return data
    finally:
        _close_connection(conn)


# ---------------- STATIC DATA ----------------
def get_days():
    return ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


def get_timeslots():
    return [
        "9:00-10:00",
        "10:00-11:00",
        "11:00-12:00",
        "1:00-2:00",
        "2:00-3:00"
    ]

# ---------------- ADD USER ----------------
def add_user(username, password, role):

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users(username,password,role) VALUES(%s,%s,%s)",
            (username, password, role)
        )

        conn.commit()
    finally:
        _close_connection(conn)

# ---------------- ATTENDANCE ----------------
def mark_attendance(student, subject, status):

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO attendance(student,subject,status)
            VALUES(%s,%s,%s)
        """, (student, subject, status))

        conn.commit()
    finally:
        _close_connection(conn)

    

def get_attendance(student):

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT subject,
            COUNT(*) as total,
            SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END)
            FROM attendance
            WHERE student=%s
            GROUP BY subject
        """, (student,))

        data = cursor.fetchall()
        return data
    finally:
        _close_connection(conn)


# ---------------- ATTENDANCE ANALYTICS ----------------
def get_attendance_summary():

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT subject,
            COUNT(*) as total,
            SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END)
            FROM attendance
            GROUP BY subject
        """)

        data = cursor.fetchall()
        return data
    finally:
        _close_connection(conn)

# ---------------- CLASH DETECTION ----------------
def is_slot_available(day, slot, faculty, room):

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Faculty clash
        cursor.execute("""
            SELECT * FROM timetable
            WHERE day=%s AND slot=%s AND faculty=%s
        """, (day, slot, faculty))

        faculty_busy = cursor.fetchone()

        # Room clash
        cursor.execute("""
            SELECT * FROM timetable
            WHERE day=%s AND slot=%s AND room=%s
        """, (day, slot, room))

        room_busy = cursor.fetchone()

        if faculty_busy or room_busy:
            return False

        return True
    finally:
        _close_connection(conn)

def optimize_timetable():

    conn = None   # ⭐ fix warning

    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, day, slot, subject, room, department
            FROM timetable
        """)

        data = cursor.fetchall()

        import random
        random.shuffle(data)

        cursor.execute("DELETE FROM timetable")

        for row in data:
            cursor.execute("""
                INSERT INTO timetable(day,slot,subject,room,department)
                VALUES(%s,%s,%s,%s,%s)
            """,(row[1],row[2],row[3],row[4],row[5]))

        conn.commit()

    finally:
        if conn:
            conn.close()


# ---------------- SAFE TIMETABLE SAVE ----------------

def save_safe_timetable(day, slot, subject, faculty, room, department):

    if is_slot_available(day, slot, faculty, room):

        conn = None
        try:
            conn = create_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO timetable
                (day,slot,subject,faculty,room,department)
                VALUES(%s,%s,%s,%s,%s,%s)
            """,(day,slot,subject,faculty,room,department))

            conn.commit()
        finally:
            _close_connection(conn)

        return True

    return False


def get_students():

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM students")

        data = cursor.fetchall()
        return [s[0] for s in data]
    finally:
        _close_connection(conn)

def get_subject_names():

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM subjects")

        data = cursor.fetchall()
        return [s[0] for s in data]
    finally:
        _close_connection(conn)

def get_free_classrooms(day, slot):

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # occupied rooms
        cursor.execute("""
            SELECT room FROM timetable
            WHERE day=%s AND slot=%s
        """,(day,slot))

        occupied = {r[0] for r in cursor.fetchall()}

        # all rooms
        cursor.execute("SELECT room FROM classrooms")

        all_rooms = [r[0] for r in cursor.fetchall()]

        free_rooms = [room for room in all_rooms if room not in occupied]
        return free_rooms
    finally:
        _close_connection(conn)

def get_low_attendance(student):

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT subject,
            COUNT(*) as total,
            SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END)
            FROM attendance
            WHERE student=%s
            GROUP BY subject
        """,(student,))

        data = cursor.fetchall()

        low_subjects = []

        for sub, total, present in data:
            percent = (present / total) * 100 if total else 0

            if percent < 75:
                low_subjects.append((sub, percent))

        return low_subjects
    finally:
        _close_connection(conn)


def update_timetable(id, subject, faculty, room):

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE timetable
            SET subject=%s, faculty=%s, room=%s
            WHERE id=%s
        """, (subject, faculty, room, id))

        conn.commit()
    finally:
        _close_connection(conn)


def get_student_attendance_percentage(student):

    conn = None
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT subject,
            COUNT(*) AS total,
            SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END)
            FROM attendance
            WHERE student=%s
            GROUP BY subject
        """, (student,))

        data = cursor.fetchall()

        result = []

        for sub, total, present in data:
            percent = (present / total) * 100 if total else 0
            result.append((sub, percent))

        return result
    finally:
        _close_connection(conn)


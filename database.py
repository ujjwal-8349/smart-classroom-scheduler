import psycopg2
import os
from dotenv import load_dotenv

# load .env variables
load_dotenv()

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
    conn.close()


# ---------------- DEFAULT ADMIN ----------------
def insert_default_users():

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
    conn.close()

# ---------------- LOGIN ----------------
def get_user(username, password, role):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s AND role=?",
        (username, password, role)
    )

    user = cursor.fetchone()
    conn.close()

    return user


# ---------------- FACULTY ----------------
def add_faculty(name, department, subject):

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
    conn.close()


def get_faculty_count():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM faculty")
    count = cursor.fetchone()[0]

    conn.close()
    return count


def get_faculty_by_department():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT department, COUNT(*)
        FROM faculty
        GROUP BY department
    """)

    data = cursor.fetchall()
    conn.close()
    return data

# ---------------- STUDENTS ----------------
def add_student(name, department):

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
    conn.close()


def get_student_count():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]

    conn.close()
    return count



# ---------------- CLASSROOM ----------------
def add_classroom(room, capacity, room_type):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO classrooms(room,capacity,type) VALUES(%s,%s,%s)",
        (room, capacity, room_type)
    )

    conn.commit()
    conn.close()


def get_classroom_count():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM classrooms")
    count = cursor.fetchone()[0]

    conn.close()
    return count


def get_classrooms_by_type(room_type):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT room FROM classrooms WHERE type=?",
        (room_type,)
    )

    data = cursor.fetchall()
    conn.close()
    return data


def get_classroom_types():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT type, COUNT(*)
        FROM classrooms
        GROUP BY type
    """)

    data = cursor.fetchall()
    conn.close()
    return data


# ---------------- SUBJECT ----------------
def add_subject(name, department, subject_type, faculty):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO subjects(name,department,type,faculty) VALUES(%s,%s,%s,%s)",
        (name, department, subject_type, faculty)
    )

    conn.commit()
    conn.close()


def get_subjects():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name, department, type, faculty FROM subjects"
    )

    data = cursor.fetchall()
    conn.close()
    return data


# ---------------- TIMETABLE ----------------
def save_timetable(day, slot, subject, room, department):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO timetable(day,slot,subject,room,department) VALUES(%s,%s,%s,%s,%s)",
        (day, slot, subject, room, department)
    )

    conn.commit()
    conn.close()


def clear_timetable():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM timetable")

    conn.commit()
    conn.close()


def get_timetable():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT day, slot, subject, faculty, room, department FROM timetable"
    )

    data = cursor.fetchall()
    conn.close()
    return data


def get_student_timetable(department):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT day, slot, subject, room FROM timetable WHERE department=?",
        (department,)
    )

    data = cursor.fetchall()
    conn.close()
    return data


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

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users(username,password,role) VALUES(%s,%s,%s)",
        (username, password, role)
    )

    conn.commit()
    conn.close()

# ---------------- ATTENDANCE ----------------
def mark_attendance(student, subject, status):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance(
            id SERIAL PRIMARY KEY,
            student TEXT,
            subject TEXT,
            status TEXT
        )
    """)

    cursor.execute(
        "INSERT INTO attendance(student,subject,status) VALUES(%s,%s,%s)"
        (student, subject, status)
    )

    conn.commit()
    conn.close()


def get_attendance(student):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT subject,
        COUNT(*) as total,
        SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END)
        FROM attendance
        WHERE student=?
        GROUP BY subject
    """, (student,))

    data = cursor.fetchall()
    conn.close()

    return data


# ---------------- ATTENDANCE ANALYTICS ----------------
def get_attendance_summary():

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
    conn.close()

    return data

def get_student_count():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")

    count = cursor.fetchone()[0]
    conn.close()

    return count

# ---------------- CLASH DETECTION ----------------
def is_slot_available(day, slot, faculty, room):

    conn = create_connection()
    cursor = conn.cursor()

    # Faculty clash
    cursor.execute("""
        SELECT * FROM timetable
        WHERE day=? AND slot=? AND faculty=?
    """, (day, slot, faculty))

    faculty_busy = cursor.fetchone()

    # Room clash
    cursor.execute("""
        SELECT * FROM timetable
        WHERE day=? AND slot=? AND room=?
    """, (day, slot, room))

    room_busy = cursor.fetchone()

    conn.close()

    if faculty_busy or room_busy:
        return False

    return True

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

        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO timetable
            (day,slot,subject,faculty,room,department)
            VALUES(%s,%s,%s,%s,%s,%s)
        """,(day,slot,subject,faculty,room,department))

        conn.commit()
        conn.close()

        return True

    return False


def get_students():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM students")

    data = cursor.fetchall()
    conn.close()

    return [s[0] for s in data]

def get_subject_names():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM subjects")

    data = cursor.fetchall()
    conn.close()

    return [s[0] for s in data]

def get_free_classrooms(day, slot):

    conn = create_connection()
    cursor = conn.cursor()

    # occupied rooms
    cursor.execute("""
        SELECT room FROM timetable
        WHERE day=? AND slot=?
    """,(day,slot))

    occupied = [r[0] for r in cursor.fetchall()]

    # all rooms
    cursor.execute("SELECT room FROM classrooms")

    all_rooms = [r[0] for r in cursor.fetchall()]

    conn.close()

    free_rooms = [
        room for room in all_rooms
        if room not in occupied
    ]

    return free_rooms

def get_low_attendance(student):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT subject,
        COUNT(*) as total,
        SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END)
        FROM attendance
        WHERE student=?
        GROUP BY subject
    """,(student,))

    data = cursor.fetchall()
    conn.close()

    low_subjects = []

    for sub, total, present in data:
        percent = (present / total) * 100 if total else 0

        if percent < 75:
            low_subjects.append((sub, percent))

    return low_subjects


def update_timetable(id, subject, faculty, room):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE timetable
        SET subject=?, faculty=?, room=?
        WHERE id=?
    """, (subject, faculty, room, id))

    conn.commit()
    conn.close()


def get_free_classrooms(day, slot):

    conn = create_connection()
    cursor = conn.cursor()

    # All rooms
    cursor.execute("SELECT room FROM classrooms")
    all_rooms = {r[0] for r in cursor.fetchall()}

    # Busy rooms
    cursor.execute("""
        SELECT room FROM timetable
        WHERE day=? AND slot=?
    """, (day, slot))

    busy_rooms = {r[0] for r in cursor.fetchall()}

    conn.close()

    # Free = All - Busy
    free_rooms = list(all_rooms - busy_rooms)

    return free_rooms



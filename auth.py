import bcrypt
from database import create_connection


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password, stored_password):
    try:
        return bcrypt.checkpw(password.encode(), stored_password.encode())
    except:
        return password == stored_password


def login_user(username, password, role):

    conn = None

    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, username, password, role
            FROM users
            WHERE username=%s AND role=%s
            """,
            (username, role)
        )

        user = cursor.fetchone()

        if not user:
            return None

        user_id, db_username, stored_password, db_role = user

        if not verify_password(password, stored_password):
            return None

        if stored_password and not stored_password.startswith("$2"):
            new_hash = hash_password(password)

            cursor.execute(
                "UPDATE users SET password=%s WHERE id=%s",
                (new_hash, user_id)
            )
            conn.commit()

        return user

    except Exception as e:
        print("Login error:", e)
        return None

    finally:
        if conn:
            conn.close()
import sqlite3
import os
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash

def get_connection():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(Config.DATABASE_PATH), exist_ok=True)
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    conn = get_connection()
    with open(schema_path, 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("[DB] Database initialized.")

# ── User Auth ─────────────────────────────────────────────────────────────────
def create_user(name, email, password, phone=None, age=None, dob=None, height=None, weight=None):
    conn = get_connection()
    try:
        pw_hash = generate_password_hash(password)
        conn.execute("""
            INSERT INTO users (name, email, password_hash, phone, age, dob, height, weight)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, email, pw_hash, phone, age, dob, height, weight))
        conn.commit()
        return True, "Account created successfully"
    except sqlite3.IntegrityError:
        return False, "Email already registered"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def get_user_by_email(email):
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def get_user_by_id(user_id):
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def verify_user(email, password):
    user = get_user_by_email(email)
    if user and check_password_hash(user['password_hash'], password):
        return user
    return None

# ── Sessions ──────────────────────────────────────────────────────────────────
def save_session(session_id, exercise_type, total_reps, correct_reps, duration_seconds, user_id=None):
    accuracy = (correct_reps / total_reps * 100) if total_reps > 0 else 0
    conn = get_connection()
    try:
        conn.execute("""
            INSERT OR REPLACE INTO sessions 
            (session_id, user_id, exercise_type, total_reps, correct_reps, accuracy, duration_seconds, ended_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (session_id, user_id, exercise_type, total_reps, correct_reps, accuracy, duration_seconds))
        conn.commit()
    finally:
        conn.close()

def get_session_history(limit=20, user_id=None):
    conn = get_connection()
    try:
        if user_id:
            rows = conn.execute("""
                SELECT session_id, exercise_type, total_reps, correct_reps, accuracy, 
                       duration_seconds, started_at, ended_at
                FROM sessions WHERE user_id = ? ORDER BY started_at DESC LIMIT ?
            """, (user_id, limit)).fetchall()
        else:
            rows = conn.execute("""
                SELECT session_id, exercise_type, total_reps, correct_reps, accuracy, 
                       duration_seconds, started_at, ended_at
                FROM sessions ORDER BY started_at DESC LIMIT ?
            """, (limit,)).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def log_rep(session_id, rep_number, is_correct, peak_angle):
    conn = get_connection()
    try:
        conn.execute("""
            INSERT INTO rep_events (session_id, rep_number, is_correct, peak_angle)
            VALUES (?, ?, ?, ?)
        """, (session_id, rep_number, is_correct, peak_angle))
        conn.commit()
    finally:
        conn.close()

def get_stats(user_id=None):
    conn = get_connection()
    try:
        if user_id:
            row = conn.execute("""
                SELECT COUNT(*) as total_sessions,
                       COALESCE(SUM(total_reps), 0) as total_reps,
                       COALESCE(AVG(accuracy), 0) as avg_accuracy
                FROM sessions WHERE user_id = ? AND ended_at IS NOT NULL
            """, (user_id,)).fetchone()
        else:
            row = conn.execute("""
                SELECT COUNT(*) as total_sessions,
                       COALESCE(SUM(total_reps), 0) as total_reps,
                       COALESCE(AVG(accuracy), 0) as avg_accuracy
                FROM sessions WHERE ended_at IS NOT NULL
            """).fetchone()
        return dict(row) if row else {}
    finally:
        conn.close()

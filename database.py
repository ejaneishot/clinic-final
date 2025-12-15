import pymysql
from tkinter import messagebox

# --- CONFIGURATION ---
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '13245',  # <--- CHECK PASSWORD
    'database': 'clinicappointmentsystem',
    'cursorclass': pymysql.cursors.DictCursor,
    'autocommit': True
}

def get_conn():
    try:
        return pymysql.connect(**DB_CONFIG)
    except Exception as e:
        messagebox.showerror("DB Connection Error", str(e))
        return None

def fetch_all(sql, params=()):
    conn = get_conn()
    if not conn: return []
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
    finally:
        conn.close()

def execute_query(sql, params=()):
    conn = get_conn()
    if not conn: return False
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.lastrowid if sql.strip().upper().startswith("INSERT") else True
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return False
    finally:
        conn.close()

# --- SMART LOGIC: Get Only Free Staff ---
def get_available_staff(date, time):
    """
    Returns a list of staff members who are NOT booked at the given date/time.
    """
    sql = """
        SELECT * FROM staff 
        WHERE staffID NOT IN (
            SELECT staffID FROM appointment 
            WHERE appointmentDate = %s 
            AND appointmentTime = %s 
            AND appointmentStatus != 'Cancelled'
            AND staffID IS NOT NULL
        )
    """
    return fetch_all(sql, (date, time))

def is_slot_available(room_id, date, time):
    sql = "SELECT * FROM appointment WHERE roomNumber=%s AND appointmentDate=%s AND appointmentTime=%s AND appointmentStatus!='Cancelled'"
    if len(fetch_all(sql, (room_id, date, time))) > 0: return False
    return True

def set_room_status(room_id, status):
    execute_query("UPDATE room SET roomStatus=%s WHERE roomNumber=%s", (status, room_id))
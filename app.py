import os
import sqlite3
from datetime import datetime

try:
    import mysql.connector
except Exception:
    mysql = None


def get_connection():
    db_type = os.getenv("DB_TYPE", "sqlite").lower()

    if db_type == "mysql":
        if mysql is None:
            raise RuntimeError("mysql-connector-python is not installed.")
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "medical_db"),
            port=int(os.getenv("DB_PORT", "3306")),
        )

    db_path = os.getenv("SQLITE_DB_PATH", "demo_medical.db")
    return sqlite3.connect(db_path)


def is_sqlite(conn):
    return isinstance(conn, sqlite3.Connection)


def placeholder(conn):
    return "?" if is_sqlite(conn) else "%s"


def print_table(headers, rows):
    if not rows:
        print("\nNo results found.\n")
        return

    widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, value in enumerate(row):
            widths[i] = max(widths[i], len("" if value is None else str(value)))

    line = "+-" + "-+-".join("-" * w for w in widths) + "-+"

    print()
    print(line)
    print("| " + " | ".join(str(headers[i]).ljust(widths[i]) for i in range(len(headers))) + " |")
    print(line)

    for row in rows:
        print("| " + " | ".join(
            ("" if row[i] is None else str(row[i])).ljust(widths[i]) for i in range(len(headers))
        ) + " |")

    print(line)
    print()


def run_query(conn, query, params=None):
    cur = conn.cursor()
    cur.execute(query, params or ())
    rows = cur.fetchall()
    cur.close()
    return rows


def feature_1(conn):
    doctor_id = input("Enter doctor ID: ").strip()
    p = placeholder(conn)
    query = f"""
        SELECT
            a.appointment_id,
            DATE(a.appointment_day) AS appointment_date,
            TIME(a.appointment_day) AS appointment_time,
            COALESCE(pat.patient_firstname, 'Unknown') AS first_name,
            COALESCE(pat.patient_lastname, 'Unknown') AS last_name
        FROM Appointment a
        JOIN Patient pat ON a.patient_id = pat.patient_id
        WHERE a.doctor_id = {p}
          AND a.appointment_day >= CURRENT_TIMESTAMP
        ORDER BY a.appointment_day;
    """
    rows = run_query(conn, query, (doctor_id,))
    print_table(
        ["Appointment ID", "Date", "Time", "Patient First Name", "Patient Last Name"],
        rows
    )


def feature_2(conn):
    patient_id = input("Enter patient ID: ").strip()
    p = placeholder(conn)
    query = f"""
        SELECT
            a.appointment_id,
            DATE(a.appointment_day) AS appointment_date,
            TIME(a.appointment_day) AS appointment_time,
            d.doctor_firstname,
            d.doctor_lastname,
            d.specialty
        FROM Appointment a
        JOIN Doctor d ON a.doctor_id = d.doctor_id
        WHERE a.patient_id = {p}
          AND a.appointment_day >= CURRENT_TIMESTAMP
        ORDER BY a.appointment_day;
    """
    rows = run_query(conn, query, (patient_id,))
    print_table(
        ["Appointment ID", "Date", "Time", "Doctor First Name", "Doctor Last Name", "Specialty"],
        rows
    )


def feature_3(conn):
    query = """
        SELECT
            COALESCE(p.patient_firstname, 'Unknown') AS first_name,
            COALESCE(p.patient_lastname, 'Unknown') AS last_name,
            p.gender,
            mh.diagnosis_date,
            CASE
                WHEN mh.is_chronic = 1 THEN 'Chronic'
                WHEN mh.is_chronic = 0 THEN 'Not Chronic'
                ELSE 'Unknown'
            END AS medical_history
        FROM Patient p
        LEFT JOIN MedicalHistory mh
            ON p.patient_id = mh.patient_id
        ORDER BY p.patient_lastname, p.patient_firstname;
    """
    rows = run_query(conn, query)
    print_table(
        ["First Name", "Last Name", "Gender", "Diagnosis Date", "Medical History"],
        rows
    )


def feature_4(conn):
    doctor_id = input("Enter doctor ID: ").strip()
    start_date = input("Enter start date (YYYY-MM-DD): ").strip()
    end_date = input("Enter end date (YYYY-MM-DD): ").strip()
    p = placeholder(conn)
    query = f"""
        SELECT
            available_date,
            start_time,
            end_time
        FROM DoctorAvailability
        WHERE doctor_id = {p}
          AND available_date BETWEEN {p} AND {p}
        ORDER BY available_date, start_time;
    """
    rows = run_query(conn, query, (doctor_id, start_date, end_date))
    print_table(
        ["Available Date", "Start Time", "End Time"],
        rows
    )


def feature_5(conn):
    specialty = input("Enter specialty: ").strip()
    p = placeholder(conn)
    query = f"""
        SELECT
            doctor_id,
            doctor_firstname,
            doctor_lastname,
            specialty,
            license_number
        FROM Doctor
        WHERE LOWER(specialty) = LOWER({p})
        ORDER BY doctor_lastname, doctor_firstname;
    """
    rows = run_query(conn, query, (specialty,))
    print_table(
        ["Doctor ID", "First Name", "Last Name", "Specialty", "License Number"],
        rows
    )


def print_menu():
    print("=" * 65)
    print(" Medical Appointment Management System ".center(65, "="))
    print("=" * 65)
    print("1. Upcoming appointments and patient names for a given doctor")
    print("2. Upcoming appointments, doctor names, and specialty for a given patient")
    print("3. Patients' names, genders, and medical history")
    print("4. Doctor availability within a date range")
    print("5. All doctors with a certain specialty")
    print("0. Exit")
    print("=" * 65)


def main():
    try:
        conn = get_connection()
    except Exception as e:
        print(f"Connection error: {e}")
        return

    try:
        while True:
            print_menu()
            choice = input("Choose an option: ").strip()

            if choice == "1":
                feature_1(conn)
            elif choice == "2":
                feature_2(conn)
            elif choice == "3":
                feature_3(conn)
            elif choice == "4":
                feature_4(conn)
            elif choice == "5":
                feature_5(conn)
            elif choice == "0":
                break
            else:
                print("Invalid option. Please try again.\n")
    finally:
        conn.close()


if __name__ == "__main__":
    main()

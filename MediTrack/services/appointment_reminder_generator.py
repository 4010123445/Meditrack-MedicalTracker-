from datetime import datetime, timedelta
from database.db_manager import DatabaseManager


def generate_appointment_reminders(minutes_before=30):
    db = DatabaseManager()
    appts = db.fetch_all(
        """
        SELECT a.id, a.patient_id, p.name AS patient_name,
               a.doctor_name, a.appointment_date, a.location
        FROM appointments a
        JOIN patients p ON p.id = a.patient_id
        WHERE a.appointment_date >= NOW()
        ORDER BY a.appointment_date ASC;
        """
    )

    created = 0
    skipped = 0

    for a in appts:
        appt_dt = a["appointment_date"]
        if isinstance(appt_dt, str):
            appt_dt = datetime.strptime(appt_dt[:19], "%Y-%m-%d %H:%M:%S")

        trigger_dt = appt_dt - timedelta(minutes=minutes_before)
        trigger_str = trigger_dt.strftime("%Y-%m-%d %H:%M:%S")

        message = f"Appointment with {a['doctor_name']} at {a['location']} in {minutes_before} minutes."
        exists = db.fetch_all(
            "SELECT id FROM reminders WHERE source_appointment_id=%s LIMIT 1;",
            (a["id"],)
        )
        if exists:
            skipped += 1
            continue

        db.execute(
            """
            INSERT INTO reminders (type, message, trigger_time, patient_id, is_sent, source_appointment_id)
            VALUES (%s, %s, %s, %s, 0, %s);
            """,
            ("Appointment", message, trigger_str, a["patient_id"], a["id"])
        )
        created += 1

    return created, skipped

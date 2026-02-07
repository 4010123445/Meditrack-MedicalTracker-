import threading
import time
from datetime import datetime
from tkinter import messagebox

from database.db_manager import DatabaseManager
from tts.voice_alert import speak_async



class ReminderService:
    def __init__(self, root, interval_seconds=5):
        self.root = root
        self.db = DatabaseManager()
        self.interval = interval_seconds
        self._running = True

        print("[ReminderService] started ✅ (nagging module loaded)")

        self.worker = threading.Thread(target=self._loop, daemon=True)
        self.worker.start()

    def stop(self):
        self._running = False

    def _loop(self):
        while self._running:
            try:
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[ReminderService] tick at {now_str}")
                due = self.db.fetch_all(
                    """
                    SELECT id, type, message, trigger_time
                    FROM reminders
                    WHERE is_sent = 0
                      AND trigger_time <= %s
                    ORDER BY trigger_time ASC;
                    """,
                    (now_str,)
                )

                print(f"[ReminderService] due found = {len(due)}")
                for r in due:
                    msg = f"{r['type']}: {r['message']}"
                    rid = r["id"]

                    print(f"[ReminderService] FIRING id={rid} -> {msg} (trigger={r['trigger_time']})")
                    self.db.execute(
                        "UPDATE reminders SET is_sent=1, sent_at=%s WHERE id=%s;",
                        (now_str, rid)
                    )

                    self.root.after(0, lambda m=msg: self._alert(m))

            except Exception as e:
                print("[ReminderService] ERROR:", repr(e))

            time.sleep(self.interval)

    def _alert(self, msg: str):
        messagebox.showinfo("MediTrack Reminder", msg)
        speak_async(msg)


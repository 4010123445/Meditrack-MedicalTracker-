import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
from database.db_manager import DatabaseManager


class ReminderUI(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("MediTrack - Reminders (CRUD)")
        self.geometry("1150x650")
        self.resizable(False, False)
        self.configure(bg="#f0f8ff")

        self.db = DatabaseManager()
        self.selected_id = None
        self.patient_map = {}  

        # Header
        header = tk.Frame(self, bg="#9b59b6", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="🔔 Reminders Management", font=("Arial", 16, "bold"), bg="#9b59b6", fg="white").pack(pady=12)
        
        # Main content frame
        content = tk.Frame(self, bg="#f0f8ff")
        content.pack(fill="both", expand=True, padx=12, pady=12)
        
        # Form frame
        form_label = tk.Frame(content, bg="#f0f8ff")
        form_label.pack(fill="x", pady=(0, 10))
        tk.Label(form_label, text="Reminder Information", font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#004d99").pack(anchor="w")
        
        form = tk.Frame(content, bg="white", relief="solid", bd=1)
        form.pack(fill="x", padx=0, pady=(0, 12))
        form.configure(highlightthickness=1, highlightbackground="#ccddff")

        # Form fields
        fields_frame = tk.Frame(form, bg="white")
        fields_frame.pack(fill="both", expand=True, padx=12, pady=12)

        # Row 1
        tk.Label(fields_frame, text="Patient", font=("Arial", 10), bg="white", fg="#333333").grid(row=0, column=0, sticky="w", pady=8)
        self.patient_var = tk.StringVar()
        patient_combo = ttk.Combobox(fields_frame, textvariable=self.patient_var, width=28, state="readonly", font=("Arial", 10))
        patient_combo.grid(row=0, column=1, sticky="ew", padx=(10, 20), pady=8)
        self.patient_combo = patient_combo

        tk.Label(fields_frame, text="Type", font=("Arial", 10), bg="white", fg="#333333").grid(row=0, column=2, sticky="w", pady=8)
        self.type_var = tk.StringVar()
        type_combo = ttk.Combobox(fields_frame,
            textvariable=self.type_var,
            values=["Medication", "Appointment", "General"],
            width=22, state="readonly", font=("Arial", 10))
        type_combo.grid(row=0, column=3, sticky="ew", padx=(10, 0), pady=8)
        self.type_combo = type_combo

        # Row 2
        tk.Label(fields_frame, text="Date", font=("Arial", 10), bg="white", fg="#333333").grid(row=1, column=0, sticky="w", pady=8)
        self.date_picker = DateEntry(fields_frame, width=14, background="#9b59b6", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd", font=("Arial", 10))
        self.date_picker.grid(row=1, column=1, sticky="w", padx=(10, 20), pady=8)

        tk.Label(fields_frame, text="Time", font=("Arial", 10), bg="white", fg="#333333").grid(row=1, column=2, sticky="w", pady=8)
        time_frame = tk.Frame(fields_frame, bg="white")
        time_frame.grid(row=1, column=3, sticky="ew", padx=(10, 0), pady=8)
        self.hour_var = tk.StringVar(value="12")
        self.minute_var = tk.StringVar(value="00")
        hour_box = ttk.Spinbox(time_frame, from_=0, to=23, width=3, textvariable=self.hour_var, format="%02.0f", font=("Arial", 10))
        hour_box.pack(side="left")
        tk.Label(time_frame, text=":", font=("Arial", 10), bg="white", fg="#333333").pack(side="left", padx=5)
        minute_box = ttk.Spinbox(time_frame, from_=0, to=59, width=3, textvariable=self.minute_var, format="%02.0f", font=("Arial", 10))
        minute_box.pack(side="left")

        # Row 3
        tk.Label(fields_frame, text="Message", font=("Arial", 10), bg="white", fg="#333333").grid(row=2, column=0, sticky="nw", pady=8)
        self.msg_entry = tk.Entry(fields_frame, font=("Arial", 10), bg="white", relief="solid", bd=1)
        self.msg_entry.grid(row=2, column=1, columnspan=3, sticky="ew", padx=(10, 0), pady=8)

        fields_frame.columnconfigure(1, weight=1)
        fields_frame.columnconfigure(3, weight=1)

        # Buttons frame
        btns = tk.Frame(form, bg="#f5f5f5", relief="solid", bd=1)
        btns.pack(fill="x", padx=12, pady=(0, 12), side="bottom")
        btns.configure(highlightthickness=0)

        btn_configs = [
            ("Add", self.add_reminder, "#00aa66"),
            ("Update", self.update_reminder, "#0084ff"),
            ("Delete", self.delete_reminder, "#ff6b35"),
            ("Clear", self.clear_form, "#999999"),
            ("Refresh", self.refresh_all, "#0066cc"),
            ("Reset Sent Flags", self.reset_sent, "#cc6600"),
            ("← Back", self.destroy, "#666666")
        ]
        
        for text, cmd, color in btn_configs:
            btn = tk.Button(btns, text=text, command=cmd, font=("Arial", 10, "bold"), 
                           bg=color, fg="white", padx=10, pady=8, relief="flat", cursor="hand2",
                           activebackground=color, activeforeground="white", border=0)
            btn.pack(side="left", padx=4, pady=10)
        
        # Table section
        table_label = tk.Frame(content, bg="#f0f8ff")
        table_label.pack(fill="x", pady=(12, 10))
        tk.Label(table_label, text="Reminders List", font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#004d99").pack(anchor="w")
        
        table_bg = tk.Frame(content, bg="white", relief="solid", bd=1)
        table_bg.pack(fill="both", expand=True)
        table_bg.configure(highlightthickness=1, highlightbackground="#ccddff")

        cols = ("id", "patient", "type", "message", "trigger_time", "is_sent")
        self.tree = ttk.Treeview(table_bg, columns=cols, show="headings", height=12)

        for c, h in [
            ("id", "ID"),
            ("patient", "Patient"),
            ("type", "Type"),
            ("message", "Message"),
            ("trigger_time", "Trigger Time"),
            ("is_sent", "Sent?"),
        ]:
            self.tree.heading(c, text=h)

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("patient", width=200)
        self.tree.column("type", width=100, anchor="center")
        self.tree.column("message", width=350)
        self.tree.column("trigger_time", width=150, anchor="center")
        self.tree.column("is_sent", width=60, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        sb = ttk.Scrollbar(table_bg, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.after(50, self.safe_refresh)

    
    def refresh_all(self):
        self.load_patients_dropdown()
        self.load_reminders()

    def load_patients_dropdown(self):
        self.patient_map.clear()
        rows = self.db.fetch_all("SELECT id, name FROM patients ORDER BY name ASC;")

        display = []
        for r in rows:
            key = f'{r["id"]} - {r["name"]}'
            self.patient_map[key] = r["id"]
            display.append(key)

        self.patient_combo["values"] = display
        if display and not self.patient_var.get():
            self.patient_var.set(display[0])

    def load_reminders(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = self.db.fetch_all(
            """
            SELECT r.id, r.patient_id, p.name AS patient_name,
                   r.type, r.message, r.trigger_time, r.is_sent
            FROM reminders r
            JOIN patients p ON p.id = r.patient_id
            ORDER BY r.trigger_time DESC;
            """
        )

        for r in rows:
            patient_display = f'{r["patient_id"]} - {r["patient_name"]}'
            self.tree.insert("", "end", values=(
                r["id"], patient_display, r["type"], r["message"], str(r["trigger_time"]), r["is_sent"]
            ))

    def clear_form(self):
        self.selected_id = None
        self.type_var.set("")
        self.date_picker.set_date(datetime.now().date())
        self.hour_var.set("12")
        self.minute_var.set("00")
        self.msg_entry.delete(0, "end")
        self.tree.selection_remove(self.tree.selection())

    def _valid_datetime(self, s: str) -> bool:
        try:
            datetime.strptime(s.strip(), "%Y-%m-%d %H:%M")
            return True
        except ValueError:
            return False

    def validate_inputs(self) -> bool:
        if not self.patient_var.get().strip():
            messagebox.showwarning("Validation", "Please select a patient.")
            return False
        if not self.type_var.get().strip():
            messagebox.showwarning("Validation", "Select a reminder type.")
            return False
        if not self.msg_entry.get().strip():
            messagebox.showwarning("Validation", "Message is required.")
            return False
        return True

    def on_select(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        v = self.tree.item(sel[0], "values")
        self.selected_id = int(v[0])
        self.patient_var.set(v[1])
        self.type_var.set(v[2])
        
        dt = v[4] if isinstance(v[4], str) else str(v[4])
        date_part, time_part = dt.split(" ")
        hour, minute = time_part.split(":")[:2]

        self.date_picker.set_date(date_part)
        self.hour_var.set(hour)
        self.minute_var.set(minute)

    def safe_refresh(self):
        try:
            self.db.fetch_all("SELECT 1 AS ok;")
            self.refresh_all()
        except Exception as e:
            messagebox.showerror(
                "Database Error 💥",
                f"Can't load reminders right now.\n\n{type(e).__name__}: {e}"
            )

    def add_reminder(self):
        if not self.validate_inputs():
            return

        patient_id = self.patient_map.get(self.patient_var.get())
        date_str = self.date_picker.get_date().strftime("%Y-%m-%d")
        hour = int(self.hour_var.get())
        minute = int(self.minute_var.get())

        trigger = f"{date_str} {hour:02d}:{minute:02d}:00"

        self.db.execute(
            "INSERT INTO reminders (type, message, trigger_time, patient_id, is_sent) VALUES (%s,%s,%s,%s,0);",
            (self.type_var.get().strip(), self.msg_entry.get().strip(), trigger, patient_id)
        )
        messagebox.showinfo("Success", "Reminder added. The computer is now emotionally invested.")
        self.clear_form()
        self.load_reminders()

    def update_reminder(self):
        if self.selected_id is None:
            messagebox.showwarning("Update", "Select a reminder first.")
            return
        if not self.validate_inputs():
            return

        patient_id = self.patient_map.get(self.patient_var.get())
        date_str = self.date_picker.get_date().strftime("%Y-%m-%d")
        hour = int(self.hour_var.get())
        minute = int(self.minute_var.get())

        trigger = f"{date_str} {hour:02d}:{minute:02d}:00"

        self.db.execute(
            "UPDATE reminders SET type=%s, message=%s, trigger_time=%s, patient_id=%s, is_sent=0, sent_at=NULL WHERE id=%s;",
            (self.type_var.get().strip(), self.msg_entry.get().strip(), trigger, patient_id, self.selected_id)
        )
        messagebox.showinfo("Success", "Reminder updated. Time has been bullied into compliance.")
        self.clear_form()
        self.load_reminders()

    def delete_reminder(self):
        if self.selected_id is None:
            messagebox.showwarning("Delete", "Select a reminder first.")
            return
        if not messagebox.askyesno("Confirm", "Delete this reminder? (The app will forget, unlike you.)"):
            return

        self.db.execute("DELETE FROM reminders WHERE id=%s;", (self.selected_id,))
        messagebox.showinfo("Success", "Reminder deleted. One less thing for your future self to ignore.")
        self.clear_form()
        self.load_reminders()

    def reset_sent(self):
        if not messagebox.askyesno("Confirm", "Reset all reminders to NOT SENT? (Demo mode: activated)"):
            return
        self.db.execute("UPDATE reminders SET is_sent=0, sent_at=NULL;")
        messagebox.showinfo("Done", "All reminders reset. The app is ready to nag again.")
        self.load_reminders()

from services.appointment_reminder_generator import generate_appointment_reminders
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry

from database.db_manager import DatabaseManager


class AppointmentUI(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("MediTrack - Appointments (CRUD)")
        self.geometry("1350x850")
        self.resizable(False, False)
        self.configure(bg="#f0f8ff")

        self.db = DatabaseManager()
        self.selected_appt_id = None
        self.patient_map = {}  

        # Header
        header = tk.Frame(self, bg="#ff6b35", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="📅 Appointments Management", font=("Arial", 16, "bold"), bg="#ff6b35", fg="white").pack(pady=12)
        
        # Main content frame
        content = tk.Frame(self, bg="#f0f8ff")
        content.pack(fill="both", expand=True, padx=12, pady=12)
        
        # Form section
        form_label = tk.Frame(content, bg="#f0f8ff")
        form_label.pack(fill="x", pady=(0, 10))
        tk.Label(form_label, text="Appointment Information", font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#004d99").pack(anchor="w")
        
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

        tk.Label(fields_frame, text="Doctor Name", font=("Arial", 10), bg="white", fg="#333333").grid(row=0, column=2, sticky="w", pady=8)
        self.doctor_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.doctor_var, font=("Arial", 10), width=25, bg="white", relief="solid", bd=1).grid(row=0, column=3, sticky="ew", padx=(10, 0), pady=8)

        # Row 2
        tk.Label(fields_frame, text="Date", font=("Arial", 10), bg="white", fg="#333333").grid(row=1, column=0, sticky="w", pady=8)
        self.appt_date_picker = DateEntry(fields_frame, width=14, background="#ff6b35", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd", font=("Arial", 10))
        self.appt_date_picker.grid(row=1, column=1, sticky="w", padx=(10, 20), pady=8)

        tk.Label(fields_frame, text="Time", font=("Arial", 10), bg="white", fg="#333333").grid(row=1, column=2, sticky="w", pady=8)
        time_frame = tk.Frame(fields_frame, bg="white")
        time_frame.grid(row=1, column=3, sticky="ew", padx=(10, 0), pady=8)
        self.appt_hour_var = tk.StringVar(value="12")
        self.appt_minute_var = tk.StringVar(value="00")
        appt_hour_box = ttk.Spinbox(time_frame, from_=0, to=23, width=3, textvariable=self.appt_hour_var, format="%02.0f", font=("Arial", 10))
        appt_hour_box.pack(side="left")
        tk.Label(time_frame, text=":", font=("Arial", 10), bg="white", fg="#333333").pack(side="left", padx=5)
        appt_minute_box = ttk.Spinbox(time_frame, from_=0, to=59, width=3, textvariable=self.appt_minute_var, format="%02.0f", font=("Arial", 10))
        appt_minute_box.pack(side="left")

        # Row 3
        tk.Label(fields_frame, text="Location", font=("Arial", 10), bg="white", fg="#333333").grid(row=2, column=0, sticky="w", pady=8)
        self.location_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.location_var, font=("Arial", 10), width=28, bg="white", relief="solid", bd=1).grid(row=2, column=1, sticky="ew", padx=(10, 20), pady=8)

        tk.Label(fields_frame, text="Notes", font=("Arial", 10), bg="white", fg="#333333").grid(row=2, column=2, sticky="nw", pady=8)
        self.notes_text = tk.Text(fields_frame, width=25, height=3, font=("Arial", 10), bg="white", relief="solid", bd=1)
        self.notes_text.grid(row=2, column=3, sticky="ew", padx=(10, 0), pady=8)

        fields_frame.columnconfigure(1, weight=1)
        fields_frame.columnconfigure(3, weight=1)

        # Buttons frame
        btns = tk.Frame(form, bg="#f5f5f5", relief="solid", bd=1)
        btns.pack(fill="x", padx=12, pady=(0, 12), side="bottom")
        btns.configure(highlightthickness=0)

        btn_configs = [
            ("🔔 Generate Reminders", self.generate_reminders, "#9b59b6"),
            ("Add", self.add_appt, "#00aa66"),
            ("Update", self.update_appt, "#0084ff"),
            ("Delete", self.delete_appt, "#ff6b35"),
            ("Clear", self.clear_form, "#999999"),
            ("Refresh", self.refresh_all, "#0066cc"),
            ("← Back", self.destroy, "#666666")
        ]
        
        for text, cmd, color in btn_configs:
            btn = tk.Button(btns, text=text, command=cmd, font=("Arial", 10, "bold"), 
                           bg=color, fg="white", padx=10, pady=8, relief="flat", cursor="hand2",
                           activebackground=color, activeforeground="white", border=0)
            btn.pack(side="left", padx=4, pady=10)
        
        # Search section
        search_label = tk.Frame(content, bg="#f0f8ff")
        search_label.pack(fill="x", pady=(12, 10))
        tk.Label(search_label, text="Search Appointments", font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#004d99").pack(anchor="w")
        
        search_bg = tk.Frame(content, bg="white", relief="solid", bd=1)
        search_bg.pack(fill="x", padx=0, pady=(0, 12))
        search_bg.configure(highlightthickness=1, highlightbackground="#ccddff")

        search_content = tk.Frame(search_bg, bg="white")
        search_content.pack(fill="both", expand=True, padx=12, pady=10)

        tk.Label(search_content, text="Search by:", font=("Arial", 10), bg="white", fg="#333333").pack(side="left", padx=(0, 10))
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_content, textvariable=self.search_var, font=("Arial", 10), width=40, bg="white", relief="solid", bd=1)
        search_entry.pack(side="left", padx=(0, 15))

        tk.Label(search_content, text="Type:", font=("Arial", 10), bg="white", fg="#333333").pack(side="left", padx=(0, 10))
        
        self.search_type = tk.StringVar(value="patient")
        search_combo = ttk.Combobox(search_content, textvariable=self.search_type, values=["patient", "doctor", "date"], state="readonly", width=15, font=("Arial", 10))
        search_combo.pack(side="left", padx=(0, 15))

        search_btn = tk.Button(search_content, text="🔍 Search", command=self.search_appointments, font=("Arial", 10, "bold"),
                               bg="#0066cc", fg="white", padx=15, pady=6, relief="flat", cursor="hand2",
                               activebackground="#0066cc", activeforeground="white", border=0)
        search_btn.pack(side="left", padx=(0, 10))
        
        reset_btn = tk.Button(search_content, text="Reset", command=self.load_appointments, font=("Arial", 10, "bold"),
                              bg="#999999", fg="white", padx=15, pady=6, relief="flat", cursor="hand2",
                              activebackground="#999999", activeforeground="white", border=0)
        reset_btn.pack(side="left")

        # Table section
        table_label = tk.Frame(content, bg="#f0f8ff")
        table_label.pack(fill="x", pady=(0, 10))
        tk.Label(table_label, text="Appointments List", font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#004d99").pack(anchor="w")
        
        table_bg = tk.Frame(content, bg="white", relief="solid", bd=1)
        table_bg.pack(fill="both", expand=True)
        table_bg.configure(highlightthickness=1, highlightbackground="#ccddff")

        cols = ("id", "patient", "doctor", "datetime", "location", "notes")
        self.tree = ttk.Treeview(table_bg, columns=cols, show="headings", height=15)

        self.tree.heading("id", text="ID")
        self.tree.heading("patient", text="Patient")
        self.tree.heading("doctor", text="Doctor")
        self.tree.heading("datetime", text="Date & Time")
        self.tree.heading("location", text="Location")
        self.tree.heading("notes", text="Notes")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("patient", width=200)
        self.tree.column("doctor", width=150)
        self.tree.column("datetime", width=150, anchor="center")
        self.tree.column("location", width=150)
        self.tree.column("notes", width=200)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        sb = ttk.Scrollbar(table_bg, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.refresh_all()

    
    def refresh_all(self):
        self.load_patients_dropdown()
        self.load_appointments()

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

        if not display:
            messagebox.showwarning("No Patients", "Add a patient first before adding appointments.")

    def load_appointments(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = self.db.fetch_all(
            """
            SELECT a.id, a.patient_id, p.name AS patient_name,
                   a.doctor_name, a.appointment_date, a.location, a.notes
            FROM appointments a
            JOIN patients p ON p.id = a.patient_id
            ORDER BY a.appointment_date DESC;
            """
        )

        for r in rows:
            patient_display = f'{r["patient_id"]} - {r["patient_name"]}'
            dt = r["appointment_date"]
            dt_str = str(dt)   
            notes = (r["notes"] or "").replace("\n", " ")
            self.tree.insert("", "end", values=(r["id"], patient_display, r["doctor_name"], dt_str, r["location"], notes))

    def clear_form(self):
        self.selected_appt_id = None
        self.doctor_var.set("")
        self.appt_date_picker.set_date(datetime.now().date())
        self.appt_hour_var.set("12")
        self.appt_minute_var.set("00")
        self.location_var.set("")
        self.notes_text.delete("1.0", "end")
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
        if not self.doctor_var.get().strip():
            messagebox.showwarning("Validation", "Doctor name is required.")
            return False
        if not self.location_var.get().strip():
            messagebox.showwarning("Validation", "Location is required.")
            return False
        return True

    def on_select(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        v = self.tree.item(sel[0], "values")
        
        self.selected_appt_id = int(v[0])
        self.patient_var.set(v[1])
        self.doctor_var.set(v[2])

        
        dt_str = v[3]
        try:
            if isinstance(dt_str, str):
                if len(dt_str) >= 16:
                    date_part = dt_str[:10]
                    time_part = dt_str[11:16]
                    hour, minute = time_part.split(":")
                    self.appt_date_picker.set_date(date_part)
                    self.appt_hour_var.set(hour.zfill(2))
                    self.appt_minute_var.set(minute.zfill(2))
        except Exception:
            pass

        self.location_var.set(v[4])
        self.notes_text.delete("1.0", "end")
        self.notes_text.insert("1.0", v[5])

    def add_appt(self):
        if not self.validate_inputs():
            return

        patient_id = self.patient_map.get(self.patient_var.get())
        if not patient_id:
            messagebox.showwarning("Validation", "Invalid patient. Click Refresh.")
            return

        notes = self.notes_text.get("1.0", "end").strip() or None
        date_str = self.appt_date_picker.get_date().strftime("%Y-%m-%d")
        hour = int(self.appt_hour_var.get())
        minute = int(self.appt_minute_var.get())
        appt_dt = f"{date_str} {hour:02d}:{minute:02d}:00"

        self.db.execute(
            "INSERT INTO appointments (patient_id, doctor_name, appointment_date, location, notes) VALUES (%s,%s,%s,%s,%s);",
            (patient_id, self.doctor_var.get().strip(), appt_dt, self.location_var.get().strip(), notes)
        )
        messagebox.showinfo("Success", "Appointment added. (The doctor has been notified telepathically.)")
        self.clear_form()
        self.load_appointments()

    def update_appt(self):
        if self.selected_appt_id is None:
            messagebox.showwarning("Update", "Select an appointment first.")
            return
        if not self.validate_inputs():
            return

        patient_id = self.patient_map.get(self.patient_var.get())
        if not patient_id:
            messagebox.showwarning("Validation", "Invalid patient. Click Refresh.")
            return

        notes = self.notes_text.get("1.0", "end").strip() or None
        date_str = self.appt_date_picker.get_date().strftime("%Y-%m-%d")
        hour = int(self.appt_hour_var.get())
        minute = int(self.appt_minute_var.get())
        appt_dt = f"{date_str} {hour:02d}:{minute:02d}:00"

        self.db.execute(
            "UPDATE appointments SET patient_id=%s, doctor_name=%s, appointment_date=%s, location=%s, notes=%s WHERE id=%s;",
            (patient_id, self.doctor_var.get().strip(), appt_dt, self.location_var.get().strip(), notes, self.selected_appt_id)
        )
        messagebox.showinfo("Success", "Appointment updated. Time-travel paperwork filed.")
        self.clear_form()
        self.load_appointments()

    def delete_appt(self):
        if self.selected_appt_id is None:
            messagebox.showwarning("Delete", "Select an appointment first.")
            return
        if not messagebox.askyesno("Confirm", "Delete this appointment? (The doctor may cry.)"):
            return

        self.db.execute("DELETE FROM appointments WHERE id=%s;", (self.selected_appt_id,))
        messagebox.showinfo("Success", "Appointment deleted. The calendar is now slightly less scary.")
        self.clear_form()
        self.load_appointments()

    def generate_reminders(self):
        created, skipped = generate_appointment_reminders(minutes_before=30)
        messagebox.showinfo(
            "Reminder Generation",
            f"Created: {created}\nSkipped (already existed): {skipped}\n\nThe app has become responsible. Weird."
        )

    def search_appointments(self):
        """Search appointments by patient, doctor, or date"""
        search_term = self.search_var.get().strip()
        search_type = self.search_type.get()

        if not search_term:
            messagebox.showwarning("Search", "Please enter a search term.")
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        if search_type == "patient":
            rows = self.db.fetch_all(
                """
                SELECT a.id, a.patient_id, p.name AS patient_name,
                       a.doctor_name, a.appointment_date, a.location, a.notes
                FROM appointments a
                JOIN patients p ON p.id = a.patient_id
                WHERE p.name LIKE %s
                ORDER BY a.appointment_date DESC;
                """,
                (f"%{search_term}%",)
            )
        elif search_type == "doctor":
            rows = self.db.fetch_all(
                """
                SELECT a.id, a.patient_id, p.name AS patient_name,
                       a.doctor_name, a.appointment_date, a.location, a.notes
                FROM appointments a
                JOIN patients p ON p.id = a.patient_id
                WHERE a.doctor_name LIKE %s
                ORDER BY a.appointment_date DESC;
                """,
                (f"%{search_term}%",)
            )
        else:  
            rows = self.db.fetch_all(
                """
                SELECT a.id, a.patient_id, p.name AS patient_name,
                       a.doctor_name, a.appointment_date, a.location, a.notes
                FROM appointments a
                JOIN patients p ON p.id = a.patient_id
                WHERE DATE(a.appointment_date) LIKE %s
                ORDER BY a.appointment_date DESC;
                """,
                (f"%{search_term}%",)
            )

        if not rows:
            messagebox.showinfo("Search Results", f"No appointments found matching '{search_term}'.")
            self.load_appointments()
            return

        for r in rows:
            patient_display = f'{r["patient_id"]} - {r["patient_name"]}'
            dt = r["appointment_date"]
            dt_str = str(dt)
            notes = (r["notes"] or "").replace("\n", " ")
            self.tree.insert("", "end", values=(r["id"], patient_display, r["doctor_name"], dt_str, r["location"], notes))

        messagebox.showinfo("Search Results", f"Found {len(rows)} appointment(s).")

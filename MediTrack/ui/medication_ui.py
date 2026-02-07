import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry

from database.db_manager import DatabaseManager


class MedicationUI(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("MediTrack - Medications (CRUD)")
        self.geometry("1050x620")
        self.resizable(False, False)
        self.configure(bg="#f0f8ff")

        self.db = DatabaseManager()
        self.selected_med_id = None
        self.patient_map = {}
        
        # Header
        header = tk.Frame(self, bg="#0084ff", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="💊 Medications Management", font=("Arial", 16, "bold"), bg="#0084ff", fg="white").pack(pady=12)
        
        # Main content frame
        content = tk.Frame(self, bg="#f0f8ff")
        content.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Form frame
        form_label = tk.Frame(content, bg="#f0f8ff")
        form_label.pack(fill="x", pady=(0, 10))
        tk.Label(form_label, text="Medication Information", font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#004d99").pack(anchor="w")
        
        form = tk.Frame(content, bg="white", relief="solid", bd=1)
        form.pack(fill="x", padx=0, pady=(0, 15))
        form.configure(highlightthickness=1, highlightbackground="#ccddff")

        # Form fields
        fields_frame = tk.Frame(form, bg="white")
        fields_frame.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(fields_frame, text="Patient", font=("Arial", 10), bg="white", fg="#333333").grid(row=0, column=0, sticky="w", pady=8)
        self.patient_var = tk.StringVar()
        patient_combo = ttk.Combobox(fields_frame, textvariable=self.patient_var, width=35, state="readonly", font=("Arial", 10))
        patient_combo.grid(row=0, column=1, sticky="ew", padx=(10, 20), pady=8)
        self.patient_combo = patient_combo

        tk.Label(fields_frame, text="Medication", font=("Arial", 10), bg="white", fg="#333333").grid(row=0, column=2, sticky="w", pady=8)
        self.name_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.name_var, font=("Arial", 10), width=28, bg="white", relief="solid", bd=1).grid(row=0, column=3, sticky="ew", padx=(10, 0), pady=8)

        tk.Label(fields_frame, text="Dosage", font=("Arial", 10), bg="white", fg="#333333").grid(row=1, column=0, sticky="w", pady=8)
        self.dosage_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.dosage_var, font=("Arial", 10), width=15, bg="white", relief="solid", bd=1).grid(row=1, column=1, sticky="ew", padx=(10, 20), pady=8)

        tk.Label(fields_frame, text="Frequency", font=("Arial", 10), bg="white", fg="#333333").grid(row=1, column=2, sticky="w", pady=8)
        self.freq_var = tk.StringVar()
        freq_combo = ttk.Combobox(fields_frame, textvariable=self.freq_var,
            values=["Once a day", "Twice a day", "3 times a day", "Every 6 hours", "Every 8 hours", "Every 12 hours", "As needed"],
            width=25, state="readonly", font=("Arial", 10))
        freq_combo.grid(row=1, column=3, sticky="ew", padx=(10, 0), pady=8)

        tk.Label(fields_frame, text="Start Date", font=("Arial", 10), bg="white", fg="#333333").grid(row=2, column=0, sticky="w", pady=8)
        self.start_date_picker = DateEntry(fields_frame, width=14, background="#0084ff", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd", font=("Arial", 10))
        self.start_date_picker.grid(row=2, column=1, sticky="ew", padx=(10, 20), pady=8)

        tk.Label(fields_frame, text="End Date", font=("Arial", 10), bg="white", fg="#333333").grid(row=2, column=2, sticky="w", pady=8)
        self.end_date_picker = DateEntry(fields_frame, width=14, background="#0084ff", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd", font=("Arial", 10))
        self.end_date_picker.grid(row=2, column=3, sticky="ew", padx=(10, 0), pady=8)

        fields_frame.columnconfigure(1, weight=1)
        fields_frame.columnconfigure(3, weight=1)

        # Buttons frame
        btns = tk.Frame(form, bg="#f5f5f5", relief="solid", bd=1)
        btns.pack(fill="x", padx=15, pady=(0, 15), side="bottom")
        btns.configure(highlightthickness=0)

        btn_colors = {"Add": "#00aa66", "Update": "#0084ff", "Delete": "#ff6b35", "Clear": "#999999", "Refresh": "#0066cc", "← Back": "#666666"}
        
        for text, color in btn_colors.items():
            if text == "← Back":
                cmd = self.destroy
            elif text == "Add":
                cmd = self.add_med
            elif text == "Update":
                cmd = self.update_med
            elif text == "Delete":
                cmd = self.delete_med
            elif text == "Refresh":
                cmd = self.refresh_all
            else:
                cmd = self.clear_form
                
            btn = tk.Button(btns, text=text, command=cmd, font=("Arial", 10, "bold"), 
                           bg=color, fg="white", padx=12, pady=8, relief="flat", cursor="hand2",
                           activebackground=color, activeforeground="white", border=0)
            btn.pack(side="left", padx=5, pady=10)
        
        # Table frame
        table_label = tk.Frame(content, bg="#f0f8ff")
        table_label.pack(fill="x", pady=(15, 10))
        tk.Label(table_label, text="Medication List", font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#004d99").pack(anchor="w")
        
        table_bg = tk.Frame(content, bg="white", relief="solid", bd=1)
        table_bg.pack(fill="both", expand=True)
        table_bg.configure(highlightthickness=1, highlightbackground="#ccddff")

        cols = ("id", "patient", "name", "dosage", "frequency", "start_date", "end_date")
        self.tree = ttk.Treeview(table_bg, columns=cols, show="headings", height=10)

        self.tree.heading("id", text="ID")
        self.tree.heading("patient", text="Patient")
        self.tree.heading("name", text="Medication")
        self.tree.heading("dosage", text="Dosage")
        self.tree.heading("frequency", text="Frequency")
        self.tree.heading("start_date", text="Start Date")
        self.tree.heading("end_date", text="End Date")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("patient", width=200)
        self.tree.column("name", width=150)
        self.tree.column("dosage", width=100)
        self.tree.column("frequency", width=130)
        self.tree.column("start_date", width=100, anchor="center")
        self.tree.column("end_date", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        sb = ttk.Scrollbar(table_bg, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.refresh_all()

    def refresh_all(self):
        self.load_patients_dropdown()
        self.load_meds()

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
            messagebox.showwarning("No Patients", "Add a patient first before adding medications.")

    def load_meds(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = self.db.fetch_all(
            """
            SELECT m.id, m.patient_id, p.name AS patient_name,
                   m.name, m.dosage, m.frequency, m.start_date, m.end_date
            FROM medications m
            JOIN patients p ON p.id = m.patient_id
            ORDER BY m.id DESC;
            """
        )

        for r in rows:
            patient_display = f'{r["patient_id"]} - {r["patient_name"]}'
            self.tree.insert("", "end", values=(
                r["id"], patient_display, r["name"], r["dosage"], r["frequency"], r["start_date"], r["end_date"]
            ))

    def clear_form(self):
        self.selected_med_id = None
        self.name_var.set("")
        self.dosage_var.set("")
        self.freq_var.set("")
        self.start_date_picker.set_date(datetime.now().date())
        self.end_date_picker.set_date(datetime.now().date())
        self.tree.selection_remove(self.tree.selection())

    def validate_inputs(self) -> bool:
        if not self.patient_var.get().strip():
            messagebox.showwarning("Validation", "Please select a patient.")
            return False
        if not self.name_var.get().strip():
            messagebox.showwarning("Validation", "Medication name is required.")
            return False
        if not self.dosage_var.get().strip():
            messagebox.showwarning("Validation", "Dosage is required (e.g., 500mg).")
            return False
        if not self.freq_var.get().strip():
            messagebox.showwarning("Validation", "Frequency is required.")
            return False
        return True

    def on_select(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        v = self.tree.item(sel[0], "values")
        
        self.selected_med_id = int(v[0])
        self.patient_var.set(v[1])
        self.name_var.set(v[2])
        self.dosage_var.set(v[3])
        self.freq_var.set(v[4])
        if v[5] not in ("None", "", None):
            self.start_date_picker.set_date(str(v[5])[:10])
        else:
            self.start_date_picker.set_date(datetime.now().date())
        if v[6] not in ("None", "", None):
            self.end_date_picker.set_date(str(v[6])[:10])
        else:
            self.end_date_picker.set_date(datetime.now().date())

    
    def add_med(self):
        if not self.validate_inputs():
            return

        patient_id = self.patient_map.get(self.patient_var.get())
        if not patient_id:
            messagebox.showwarning("Validation", "Invalid patient. Click Refresh.")
            return

        start = self.start_date_picker.get_date().strftime("%Y-%m-%d")
        end = self.end_date_picker.get_date().strftime("%Y-%m-%d")

        self.db.execute(
            "INSERT INTO medications (patient_id, name, dosage, frequency, start_date, end_date) VALUES (%s,%s,%s,%s,%s,%s);",
            (patient_id, self.name_var.get().strip(), self.dosage_var.get().strip(), self.freq_var.get().strip(), start, end)
        )
        messagebox.showinfo("Success", "Medication added.")
        self.clear_form()
        self.load_meds()

    def update_med(self):
        if self.selected_med_id is None:
            messagebox.showwarning("Update", "Select a medication first.")
            return
        if not self.validate_inputs():
            return

        patient_id = self.patient_map.get(self.patient_var.get())
        if not patient_id:
            messagebox.showwarning("Validation", "Invalid patient. Click Refresh.")
            return

        start = self.start_date_picker.get_date().strftime("%Y-%m-%d")
        end = self.end_date_picker.get_date().strftime("%Y-%m-%d")

        self.db.execute(
            "UPDATE medications SET patient_id=%s, name=%s, dosage=%s, frequency=%s, start_date=%s, end_date=%s WHERE id=%s;",
            (patient_id, self.name_var.get().strip(), self.dosage_var.get().strip(), self.freq_var.get().strip(), start, end, self.selected_med_id)
        )
        messagebox.showinfo("Success", "Medication updated.")
        self.clear_form()
        self.load_meds()

    def delete_med(self):
        if self.selected_med_id is None:
            messagebox.showwarning("Delete", "Select a medication first.")
            return
        if not messagebox.askyesno("Confirm", "Delete this medication?"):
            return

        self.db.execute("DELETE FROM medications WHERE id=%s;", (self.selected_med_id,))
        messagebox.showinfo("Success", "Medication deleted.")
        self.clear_form()
        self.load_meds()

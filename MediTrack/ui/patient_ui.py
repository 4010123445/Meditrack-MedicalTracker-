import tkinter as tk
from tkinter import ttk, messagebox
from database.db_manager import DatabaseManager

from ui.patient_medication_history_ui import PatientMedicationHistoryUI

class PatientUI(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("MediTrack - Patients (CRUD)")
        self.geometry("950x580")
        self.resizable(False, False)
        self.configure(bg="#f0f8ff")

        self.db = DatabaseManager()
        self.selected_patient_id = None

        # Configure style
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 14, "bold"), foreground="#004d99")
        
        # Header
        header = tk.Frame(self, bg="#0066cc", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="👥 Patients Management", font=("Arial", 16, "bold"), bg="#0066cc", fg="white").pack(pady=12)
        
        # Main content frame
        content = tk.Frame(self, bg="#f0f8ff")
        content.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Form frame
        form_label = tk.Frame(content, bg="#f0f8ff")
        form_label.pack(fill="x", pady=(0, 10))
        tk.Label(form_label, text="Patient Information", font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#004d99").pack(anchor="w")
        
        form = tk.Frame(content, bg="white", relief="solid", bd=1)
        form.pack(fill="x", padx=0, pady=(0, 15))
        form.configure(highlightthickness=1, highlightbackground="#ccddff")

        # Form fields
        fields_frame = tk.Frame(form, bg="white")
        fields_frame.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(fields_frame, text="Name", font=("Arial", 10), bg="white", fg="#333333").grid(row=0, column=0, sticky="w", pady=8)
        self.name_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.name_var, font=("Arial", 10), width=35, bg="white", relief="solid", bd=1).grid(row=0, column=1, sticky="ew", padx=(10, 20), pady=8)

        tk.Label(fields_frame, text="Age", font=("Arial", 10), bg="white", fg="#333333").grid(row=0, column=2, sticky="w", pady=8)
        self.age_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.age_var, font=("Arial", 10), width=12, bg="white", relief="solid", bd=1).grid(row=0, column=3, sticky="ew", pady=8)

        tk.Label(fields_frame, text="Gender", font=("Arial", 10), bg="white", fg="#333333").grid(row=1, column=0, sticky="w", pady=8)
        self.gender_var = tk.StringVar()
        gender_combo = ttk.Combobox(fields_frame, textvariable=self.gender_var, values=["Male", "Female", "Other"], state="readonly", width=15, font=("Arial", 10))
        gender_combo.grid(row=1, column=1, sticky="ew", padx=(10, 20), pady=8)

        tk.Label(fields_frame, text="Contact", font=("Arial", 10), bg="white", fg="#333333").grid(row=1, column=2, sticky="w", pady=8)
        self.contact_var = tk.StringVar()
        tk.Entry(fields_frame, textvariable=self.contact_var, font=("Arial", 10), width=25, bg="white", relief="solid", bd=1).grid(row=1, column=3, sticky="ew", pady=8)

        fields_frame.columnconfigure(1, weight=1)
        fields_frame.columnconfigure(3, weight=1)

        # Buttons frame
        btns = tk.Frame(form, bg="#f5f5f5", relief="solid", bd=1)
        btns.pack(fill="x", padx=15, pady=(0, 15), side="bottom")
        btns.configure(highlightthickness=0)

        btn_colors = {"Add": "#00aa66", "Update": "#0084ff", "Delete": "#ff6b35", "Clear": "#999999", "← Back": "#666666"}
        
        for text, color in btn_colors.items():
            if text == "← Back":
                cmd = self.destroy
            elif text == "Add":
                cmd = self.add_patient
            elif text == "Update":
                cmd = self.update_patient
            elif text == "Delete":
                cmd = self.delete_patient
            else:
                cmd = self.clear_form
                
            btn = tk.Button(btns, text=text, command=cmd, font=("Arial", 10, "bold"), 
                           bg=color, fg="white", padx=12, pady=8, relief="flat", cursor="hand2",
                           activebackground=color, activeforeground="white", border=0)
            btn.pack(side="left", padx=5, pady=10)

        # Table frame
        table_label = tk.Frame(content, bg="#f0f8ff")
        table_label.pack(fill="x", pady=(15, 10))
        tk.Label(table_label, text="Patients List", font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#004d99").pack(anchor="w")
        
        table_bg = tk.Frame(content, bg="white", relief="solid", bd=1)
        table_bg.pack(fill="both", expand=True)
        table_bg.configure(highlightthickness=1, highlightbackground="#ccddff")

        self.tree = ttk.Treeview(table_bg, columns=("id", "name", "age", "gender", "contact"), show="headings", height=12)

        for col in ("id", "name", "age", "gender", "contact"):
            self.tree.heading(col, text=col.title())

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=250)
        self.tree.column("age", width=50, anchor="center")
        self.tree.column("gender", width=80, anchor="center")
        self.tree.column("contact", width=150)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.select_patient)
        self.tree.bind("<Double-1>", self.open_medication_history)

        self.load_patients()

    def open_medication_history(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        patient_id = int(values[0])
        patient_name = values[1]

       
        PatientMedicationHistoryUI(self, patient_id, patient_name)

    
    def clear_form(self):
        self.selected_patient_id = None
        self.name_var.set("")
        self.age_var.set("")
        self.gender_var.set("")
        self.contact_var.set("")

    def load_patients(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        rows = self.db.fetch_all("SELECT * FROM patients")
        for r in rows:
            self.tree.insert("", "end", values=(
                r["id"], r["name"], r["age"], r["gender"], r["contact"]
            ))

    def select_patient(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        self.selected_patient_id = values[0]
        self.name_var.set(values[1])
        self.age_var.set(values[2])
        self.gender_var.set(values[3])
        self.contact_var.set(values[4])

    
    def add_patient(self):
        self.db.execute(
            "INSERT INTO patients (name, age, gender, contact) VALUES (%s, %s, %s, %s)",
            (
                self.name_var.get(),
                self.age_var.get() or None,
                self.gender_var.get(),
                self.contact_var.get()
            )
        )
        self.load_patients()
        self.clear_form()

    def update_patient(self):
        if not self.selected_patient_id:
            return

        self.db.execute(
            "UPDATE patients SET name=%s, age=%s, gender=%s, contact=%s WHERE id=%s",
            (
                self.name_var.get(),
                self.age_var.get() or None,
                self.gender_var.get(),
                self.contact_var.get(),
                self.selected_patient_id
            )
        )
        self.load_patients()
        self.clear_form()

    def delete_patient(self):
        if not self.selected_patient_id:
            return

        self.db.execute(
            "DELETE FROM patients WHERE id=%s",
            (self.selected_patient_id,)
        )
        self.load_patients()
        self.clear_form()

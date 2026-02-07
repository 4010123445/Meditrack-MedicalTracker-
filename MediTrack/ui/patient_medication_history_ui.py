import tkinter as tk
from tkinter import ttk
from database.db_manager import DatabaseManager


class PatientMedicationHistoryUI(tk.Toplevel):
    def __init__(self, master, patient_id, patient_name):
        super().__init__(master)
        self.title(f"Medication History - {patient_name}")
        self.geometry("750x480")
        self.resizable(False, False)
        self.configure(bg="#f0f8ff")

        self.db = DatabaseManager()

        # Header
        header = tk.Frame(self, bg="#0084ff", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text=f"💊 Medication History - {patient_name}", font=("Arial", 16, "bold"), bg="#0084ff", fg="white").pack(pady=12)

        # Content frame
        content = tk.Frame(self, bg="#f0f8ff")
        content.pack(fill="both", expand=True, padx=15, pady=15)

        # Table section
        table_label = tk.Frame(content, bg="#f0f8ff")
        table_label.pack(fill="x", pady=(0, 10))
        tk.Label(table_label, text=f"Medications for {patient_name}", font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#004d99").pack(anchor="w")
        
        table_bg = tk.Frame(content, bg="white", relief="solid", bd=1)
        table_bg.pack(fill="both", expand=True)
        table_bg.configure(highlightthickness=1, highlightbackground="#ccddff")

        cols = ("id", "name", "dosage", "frequency", "start_date", "end_date")
        self.tree = ttk.Treeview(table_bg, columns=cols, show="headings", height=14)

        for c in cols:
            self.tree.heading(c, text=c.replace("_", " ").title())
            self.tree.column(c, width=110)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        
        # Button frame
        btn_frame = tk.Frame(content, bg="#f0f8ff")
        btn_frame.pack(fill="x", pady=(12, 0))
        
        back_btn = tk.Button(btn_frame, text="← Back", command=self.destroy, font=("Arial", 11, "bold"),
                            bg="#0084ff", fg="white", padx=20, pady=8, relief="flat", cursor="hand2",
                            activebackground="#0084ff", activeforeground="white", border=0)
        back_btn.pack()

        
        self.load_medications(patient_id)

    def load_medications(self, patient_id):
        rows = self.db.fetch_all(
            """
            SELECT id, name, dosage, frequency, start_date, end_date
            FROM medications
            WHERE patient_id = %s
            ORDER BY id DESC;
            """,
            (patient_id,)
        )

        for r in rows:
            self.tree.insert(
                "",
                "end",
                values=(r["id"], r["name"], r["dosage"], r["frequency"], r["start_date"], r["end_date"])
            )

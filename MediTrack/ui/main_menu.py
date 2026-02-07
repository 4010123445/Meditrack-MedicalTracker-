import tkinter as tk
from tkinter import ttk

from ui.patient_ui import PatientUI
from ui.medication_ui import MedicationUI
from ui.appointment_ui import AppointmentUI
from ui.reminder_ui import ReminderUI


class MainMenu(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("MediTrack - Main Menu")
        self.geometry("500x520")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.hide_menu)
        self.configure(bg="#f0f8ff")
        
        # Configure style
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 28, "bold"), background="#f0f8ff", foreground="#004d99")
        style.configure("Subtitle.TLabel", font=("Arial", 11), background="#f0f8ff", foreground="#666666")
        style.configure("Menu.TButton", font=("Arial", 12, "bold"), padding=[0, 12])
        
        # Header
        header_frame = tk.Frame(self, bg="#0066cc", height=100)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="MediTrack", font=("Arial", 28, "bold"), bg="#0066cc", fg="white").pack(pady=12)
        tk.Label(header_frame, text="Medical Appointment & Medication System", font=("Arial", 10), bg="#0066cc", fg="#e6f2ff").pack(pady=5)
        
        # Module buttons frame
        box = tk.Frame(self, bg="#f0f8ff")
        box.pack(padx=25, pady=25, fill="both", expand=True)
        
        tk.Label(box, text="Modules", font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#004d99").pack(anchor="w", pady=(0, 15))
        
        modules = [
            ("👥 Patients", self.open_patients, "#00aa66"),
            ("💊 Medications", self.open_medications, "#0084ff"),
            ("📅 Appointments", self.open_appointments, "#ff6b35"),
            ("🔔 Reminders", self.open_reminders, "#9b59b6")
        ]
        
        for text, cmd, color in modules:
            btn = tk.Button(box, text=text, command=cmd, font=("Arial", 11, "bold"),
                           bg=color, fg="white", padx=15, pady=12, relief="flat",
                           cursor="hand2", activebackground=color, activeforeground="white",
                           border=0)
            btn.pack(fill="x", pady=8)
        
        # Separator
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=10)
        
        # Footer buttons
        btn_frame = tk.Frame(self, bg="#f0f8ff")
        btn_frame.pack(pady=15, fill="x")
        
        back_btn = tk.Button(btn_frame, text="← Back", command=self.hide_menu, font=("Arial", 11, "bold"),
                            bg="#666666", fg="white", padx=20, pady=8, relief="flat", cursor="hand2",
                            activebackground="#666666", activeforeground="white", border=0)
        back_btn.pack(side="left", padx=8)
        
        exit_btn = tk.Button(btn_frame, text="Exit", command=self.exit_app, font=("Arial", 11, "bold"),
                            bg="#cc0000", fg="white", padx=20, pady=8, relief="flat", cursor="hand2",
                            activebackground="#cc0000", activeforeground="white", border=0)
        exit_btn.pack(side="left", padx=8)

    def open_patients(self):
        PatientUI(self)

    def open_medications(self):
        MedicationUI(self)

    def open_appointments(self):
        AppointmentUI(self)

    def open_reminders(self):
        ReminderUI(self)

    def hide_menu(self):
        self.withdraw()

    def exit_app(self):
        self.master.destroy()

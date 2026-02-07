import tkinter as tk
from tkinter import ttk

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("MediTrack - Medical Reminder System")
        self.root.geometry("600x450")
        self.root.configure(bg="#f0f8ff")
        
        # Configure style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Title.TLabel", font=("Arial", 28, "bold"), background="#f0f8ff", foreground="#004d99")
        style.configure("Subtitle.TLabel", font=("Arial", 12), background="#f0f8ff", foreground="#666666")
        style.configure("TButton", font=("Arial", 11), padding=10)
        
        # Header frame
        header_frame = tk.Frame(root, bg="#0066cc", height=120)
        header_frame.pack(fill="x", pady=0)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="MediTrack", font=("Arial", 32, "bold"), bg="#0066cc", fg="white").pack(pady=15)
        tk.Label(header_frame, text="Medical Appointment & Medication System", font=("Arial", 11), bg="#0066cc", fg="#e6f2ff").pack(pady=5)
        
        # Content frame
        content_frame = tk.Frame(root, bg="#f0f8ff")
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Menu buttons
        button_frame = tk.Frame(content_frame, bg="#f0f8ff")
        button_frame.pack(fill="both", expand=True)
        
        buttons = [
            ("👥 Patients", "#00aa66"),
            ("💊 Medications", "#0084ff"),
            ("📅 Appointments", "#ff6b35"),
            ("🔔 Reminders", "#9b59b6")
        ]
        
        for text, color in buttons:
            btn = tk.Button(button_frame, text=text, font=("Arial", 12, "bold"), 
                           bg=color, fg="white", padx=20, pady=15, 
                           relief="flat", cursor="hand2",
                           activebackground=self.lighten_color(color),
                           activeforeground="white")
            btn.pack(fill="x", pady=10)
        
    @staticmethod
    def lighten_color(hex_color):
        """Lighten a hex color for hover effect"""
        return hex_color  # Simplified - can be enhanced

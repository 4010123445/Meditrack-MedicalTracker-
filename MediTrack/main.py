import tkinter as tk
from ui.main_menu import MainMenu
from services.reminder_service import ReminderService

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    ReminderService(root, interval_seconds=5)

    MainMenu(root)
    root.mainloop()

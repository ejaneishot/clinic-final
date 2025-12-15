import tkinter as tk
from login_view import LoginScreen
from patient_view import PatientScreen
from doctor_view import DoctorScreen
from admin import AdminScreen
from landing_page import ClinicLandingPage 

class ClinicApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clinic System - Full Version")
        self.geometry("1250x800")

        self.current_user_id = None
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # CHANGE THIS LINE below to start with LandingScreen instead of LoginScreen
        self.show_view(ClinicLandingPage)  # <--- 2. CHANGE THIS

    def show_view(self, view_class):
        for widget in self.container.winfo_children():
            widget.destroy()
        # We pass 'self' as the controller so the view can call app.show_view() later
        frame = view_class(self.container, self)
        frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = ClinicApp()
    app.mainloop()
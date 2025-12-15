import tkinter as tk
from tkinter import messagebox, font
import database
import patient_view, doctor_view, admin

class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # --- THEME CONFIGURATION ---
        self.colors = {
            "bg_main": "#F0F2F5",       # Light gray background for the screen
            "card_bg": "#FFFFFF",       # White card
            "primary": "#00A3E0",       # Main Blue
            "primary_hover": "#008CBA", # Darker Blue
            "secondary": "#E1E8ED",     # Light gray for inputs
            "text_dark": "#333333",
            "text_light": "#666666",
            "danger": "#E0245E"
        }
        self.configure(bg=self.colors["bg_main"])

        # Fonts
        self.title_font = ("Helvetica", 20, "bold")
        self.btn_font = ("Helvetica", 11, "bold")
        self.input_font = ("Helvetica", 11)

        # Default Role
        self.role = "patient"

        # --- LAYOUT: CENTERED CARD ---
        self.container = tk.Frame(self, bg=self.colors["bg_main"])
        self.container.pack(fill="both", expand=True)

        # The Card (White Box)
        self.card = tk.Frame(self.container, bg=self.colors["card_bg"], padx=40, pady=40, relief="flat")
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        # --- HEADER ---
        tk.Label(self.card, text="🏥 L3AC Clinic", font=("Arial", 28, "bold"), 
                 bg=self.colors["card_bg"], fg=self.colors["primary"]).pack(pady=(0, 10))
        
        tk.Label(self.card, text="Welcome back! Please login to continue.", 
                 font=("Arial", 10), bg=self.colors["card_bg"], fg=self.colors["text_light"]).pack(pady=(0, 20))

       # --- ROLE SELECTOR (TABS) ---
        self.role_frame = tk.Frame(self.card, bg=self.colors["card_bg"])
        
        # CHANGE 1: Remove 'fill="x"' so the frame shrinks to fit content in the center
        self.role_frame.pack(pady=10) 

        # We keep references to buttons to change their colors
        self.btn_patient = self.create_role_btn(self.role_frame, "Patient", "patient")
        self.btn_doctor = self.create_role_btn(self.role_frame, "Doctor", "doctor")
        
        # CHANGE 2: Create the Admin button (same as before)
        self.btn_admin = tk.Button(self.role_frame, text="Admin Portal", bg="#555", fg="white", bd=0, 
                                   font=("Arial", 9, "bold"), padx=10, pady=5, cursor="hand2",
                                   command=lambda: controller.show_view(admin.AdminScreen))

        # CHANGE 3: Pack ALL buttons side-by-side with padding
        self.btn_patient.pack(side="left", padx=5)
        self.btn_doctor.pack(side="left", padx=5)
        self.btn_admin.pack(side="left", padx=5)

        # Update buttons visuals to show Patient is selected by default
        self.update_role_visuals()

        # We keep references to buttons to change their colors
        self.btn_patient = self.create_role_btn(self.role_frame, "Patient", "patient")
        self.btn_doctor = self.create_role_btn(self.role_frame, "Doctor", "doctor")
        self.btn_admin = tk.Button(self.role_frame, text="Admin Portal", bg="#555", fg="white", bd=0, 
                                   font=("Arial", 9, "bold"), padx=10, pady=5, cursor="hand2",
                                   command=lambda: controller.show_view(admin.AdminScreen))

        # Update buttons visuals to show Patient is selected by default
        self.update_role_visuals()

        # --- LOGIN FORM FRAME ---
        self.login_form_frame = tk.Frame(self.card, bg=self.colors["card_bg"])
        self.login_form_frame.pack(fill="x", pady=10)

        self.lbl_prompt = tk.Label(self.login_form_frame, text="Enter Patient ID", 
                                   bg=self.colors["card_bg"], fg=self.colors["text_dark"], font=("Arial", 10, "bold"))
        self.lbl_prompt.pack(anchor="w", pady=(10, 5))

        self.ent_id = tk.Entry(self.login_form_frame, font=self.input_font, bg=self.colors["secondary"], 
                               relief="flat", highlightthickness=1, highlightbackground="#DDD")
        self.ent_id.config(highlightcolor=self.colors["primary"]) # Turn blue when clicked
        self.ent_id.pack(fill="x", ipady=8, pady=5)

        # Login Button
        self.btn_login = tk.Button(self.login_form_frame, text="Secure Login", 
                                   bg=self.colors["primary"], fg="white", 
                                   font=self.btn_font, bd=0, pady=10, cursor="hand2",
                                   activebackground=self.colors["primary_hover"],
                                   command=self.login)
        self.btn_login.pack(fill="x", pady=20)

        # Footer Link
        self.footer_frame = tk.Frame(self.card, bg=self.colors["card_bg"])
        self.footer_frame.pack(pady=10)
        tk.Label(self.footer_frame, text="New Patient? ", bg=self.colors["card_bg"], fg=self.colors["text_light"]).pack(side="left")
        
        self.btn_toggle = tk.Button(self.footer_frame, text="Create Account", 
                                    bg=self.colors["card_bg"], fg=self.colors["primary"], 
                                    font=("Arial", 10, "bold"), bd=0, cursor="hand2",
                                    activebackground=self.colors["card_bg"],
                                    command=self.toggle_register_view)
        self.btn_toggle.pack(side="left")


        # --- REGISTRATION FRAME (Hidden initially) ---
        self.reg_frame = tk.Frame(self.card, bg=self.colors["card_bg"])
        # We don't pack it yet

        tk.Label(self.reg_frame, text="Create Patient Profile", font=("Arial", 14, "bold"), 
                 bg=self.colors["card_bg"], fg=self.colors["text_dark"]).pack(pady=10)

        # Registration Fields
        self.r_name = self.create_input_field(self.reg_frame, "Full Name")
        self.r_gender = self.create_input_field(self.reg_frame, "Gender (Male/Female)")
        self.r_dob = self.create_input_field(self.reg_frame, "Birth Date (YYYY-MM-DD)")
        self.r_phone = self.create_input_field(self.reg_frame, "Phone Number")

        # Register Action Buttons
        reg_btn_frame = tk.Frame(self.reg_frame, bg=self.colors["card_bg"])
        reg_btn_frame.pack(fill="x", pady=20)

        tk.Button(reg_btn_frame, text="Sign Up", bg=self.colors["primary"], fg="white", 
                  font=self.btn_font, bd=0, pady=8, width=15, cursor="hand2",
                  command=self.register).pack(side="right")
        
        tk.Button(reg_btn_frame, text="Cancel", bg="#EEE", fg="#333", 
                  font=self.btn_font, bd=0, pady=8, width=10, cursor="hand2",
                  command=self.toggle_register_view).pack(side="right", padx=10)


    # --- HELPER UI FUNCTIONS ---
    def create_role_btn(self, parent, text, role):
        return tk.Button(parent, text=text, width=10, font=("Arial", 10, "bold"),
                         bd=0, pady=5, cursor="hand2",
                         command=lambda: self.set_role(role))

    def create_input_field(self, parent, label_text):
        tk.Label(parent, text=label_text, bg=self.colors["card_bg"], fg=self.colors["text_light"], 
                 font=("Arial", 9)).pack(anchor="w", pady=(5,0))
        entry = tk.Entry(parent, font=self.input_font, bg=self.colors["secondary"], relief="flat", width=35)
        entry.pack(fill="x", ipady=6, pady=(0, 10))
        return entry

    # --- LOGIC FUNCTIONS ---

    def set_role(self, role):
        self.role = role
        self.update_role_visuals()
        self.lbl_prompt.config(text=f"Enter {role.capitalize()} ID")

    def update_role_visuals(self):
        # Reset styles
        default_bg = "#EEE"
        default_fg = "#555"
        active_bg = self.colors["primary"]
        active_fg = "white"

        if self.role == "patient":
            self.btn_patient.config(bg=active_bg, fg=active_fg)
            self.btn_doctor.config(bg=default_bg, fg=default_fg)
        else:
            self.btn_patient.config(bg=default_bg, fg=default_fg)
            self.btn_doctor.config(bg=active_bg, fg=active_fg)

    def toggle_register_view(self):
        if self.reg_frame.winfo_ismapped():
            # Show Login
            self.reg_frame.pack_forget()
            self.role_frame.pack(fill="x", pady=10)
            self.login_form_frame.pack(fill="x", pady=10)
            self.footer_frame.pack(pady=10)
        else:
            # Show Register
            self.role_frame.pack_forget()
            self.login_form_frame.pack_forget()
            self.footer_frame.pack_forget()
            self.reg_frame.pack(fill="both", expand=True)

    def register(self):
        name = self.r_name.get()
        if not name: return messagebox.showerror("Error", "Name Required")
        
        sql = "INSERT INTO patient (patientName, patientGender, patientBirthDate, patientPhoneNumber) VALUES (%s, %s, %s, %s)"
        try:
            new_id = database.execute_query(sql, (name, self.r_gender.get(), self.r_dob.get(), self.r_phone.get()))
            if new_id:
                messagebox.showinfo("Success", f"Account Created!\n\nIMPORTANT: Your Patient ID is {new_id}.")
                self.toggle_register_view() # Return to login
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def login(self):
        uid = self.ent_id.get()
        if not uid.isdigit(): return messagebox.showerror("Error", "ID must be a number")
        
        table = "patient" if self.role == "patient" else "doctor"
        col = "patientID" if self.role == "patient" else "doctorID"
        
        # Note: Ensure your database.py has fetch_all function
        user = database.fetch_all(f"SELECT * FROM {table} WHERE {col}=%s", (uid,))
        
        if user:
            self.controller.current_user_id = uid
            if self.role == 'patient':
                self.controller.show_view(patient_view.PatientScreen)
            else:
                self.controller.show_view(doctor_view.DoctorScreen)
        else:
            messagebox.showerror("Failed", "ID Not Found")
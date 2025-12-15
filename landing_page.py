import tkinter as tk
from PIL import Image, ImageTk
from login_view import LoginScreen  # Ensure this import matches your file name
from admin import AdminScreen


class ClinicLandingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # keep PhotoImage references (important for Tkinter)
        self._img_refs = []

        # --- THEME CONFIGURATION ---
        self.colors = {
            "primary_pink": "#2576B8",    # Using your Blue/Teal tone
            "primary_blue": "#00A3E0",
            "accent_orange": "#2981C9",
            "white": "#FFFFFF",
            "text_dark": "#333333",
            "text_light": "#FFFFFF",
            "text_gray": "#777777",
            "bg_gray": "#F0F0F0",
            "section_header": "#0099CC"
        }

        self.configure(bg=self.colors["white"])

        # --- FONTS ---
        self.header_font = ("Helvetica", 24, "bold")
        self.sub_header_font = ("Helvetica", 14)
        self.body_font = ("Helvetica", 11)
        self.article_title_font = ("Arial", 10, "bold")
        self.article_date_font = ("Arial", 9)

        # --- LAYOUT ---
        self.create_navbar()

        # Content Frame
        self.content_frame = tk.Frame(self, bg=self.colors["white"])
        self.content_frame.pack(fill="both", expand=True)

        self.show_home()

    # =========================
    # HELPERS
    # =========================
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def load_image(self, path, size):
        """
        Loads and resizes an image using Pillow.
        Keeps reference to prevent Tkinter garbage collection.
        """
        try:
            img = Image.open(path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self._img_refs.append(photo)
            return photo
        except Exception as e:
            print(f"[Image load failed] {path} -> {e}")
            return None

    def create_section_title(self, parent, title, subtitle=None):
        tk.Label(
            parent, text=title, font=self.header_font,
            bg=self.colors["white"], fg=self.colors["text_dark"]
        ).pack(pady=(20, 5))
        if subtitle:
            tk.Label(
                parent, text=subtitle, font=self.body_font,
                bg=self.colors["white"], fg=self.colors["text_gray"]
            ).pack(pady=(0, 20))

    # =========================
    # NAVBAR
    # =========================
    def create_navbar(self):
        """Creates the top white navigation bar"""
        nav_frame = tk.Frame(self, bg=self.colors["white"], height=70)
        nav_frame.pack(side="top", fill="x", ipadx=10, ipady=10)

        # Logo
        logo_frame = tk.Frame(nav_frame, bg=self.colors["white"])
        logo_frame.pack(side="left", padx=30)

        tk.Label(logo_frame, text="🏥", font=("Arial", 24), bg=self.colors["white"]).pack(side="left")
        tk.Label(
            logo_frame, text="L3AC\nClinic", justify="left",
            font=("Arial", 10, "bold"), fg=self.colors["primary_pink"], bg=self.colors["white"]
        ).pack(side="left", padx=5)

        # Search Bar (placeholder)
        search_frame = tk.Frame(nav_frame, bg=self.colors["bg_gray"], padx=10, pady=5)
        search_frame.pack(side="left", padx=50)
        tk.Label(search_frame, text="Search...", bg=self.colors["bg_gray"], fg="#999").pack()

        # --- LOGIN BUTTON ---
        login_btn = tk.Button(
            nav_frame, text="Login", bg=self.colors["accent_orange"],
            fg=self.colors["white"], font=("Arial", 10, "bold"),
            bd=0, padx=20, pady=8, cursor="hand2",
            command=lambda: self.controller.show_view(LoginScreen)
        )
        login_btn.pack(side="right", padx=30)

        # Menu Links
        links_frame = tk.Frame(nav_frame, bg=self.colors["white"])
        links_frame.pack(side="right", padx=20)

        menu_items = [
            ("Home", "Home"),
            ("About Us", "About Us"),
            ("Services", "Services"),
            ("Doctors", "Contact")
        ]

        for label, page_name in menu_items:
            btn = tk.Label(
                links_frame, text=label, bg=self.colors["white"], fg=self.colors["text_dark"],
                font=("Arial", 10, "bold"), cursor="hand2"
            )
            btn.pack(side="left", padx=15)
            btn.bind("<Button-1>", lambda e, p=page_name: self.navigate(p))
            btn.bind("<Enter>", lambda e, b=btn: b.config(fg=self.colors["primary_blue"]))
            btn.bind("<Leave>", lambda e, b=btn: b.config(fg=self.colors["text_dark"]))

    def go_to_admin(self):
        """Switches to Admin Screen with lazy import to prevent crash"""
        import admin
        self.controller.show_view(admin.AdminScreen)

    def navigate(self, page_name):
        self.clear_content()

        if page_name == "Home":
            self.show_home()
        elif page_name == "About Us":
            self.show_about()
        elif page_name == "Services":
            self.show_services()
        elif page_name == "Contact":
            self.show_contact()

    # =========================
    # HOME
    # =========================
    def show_home(self):
        self.create_hero_section(self.content_frame)
        self.create_action_cards(self.content_frame)
        self.create_article_section(self.content_frame)

    def create_hero_section(self, parent):
        hero_frame = tk.Frame(parent, bg=self.colors["primary_pink"])
        hero_frame.pack(fill="x", ipady=20)

        hero_frame.columnconfigure(0, weight=1)
        hero_frame.columnconfigure(1, weight=1)

        # Left Text
        text_container = tk.Frame(hero_frame, bg=self.colors["primary_pink"])
        text_container.grid(row=0, column=0, sticky="ns", padx=50, pady=30)

        tk.Label(
            text_container, text="L3AC Clinic",
            font=("Helvetica", 36, "bold"), bg=self.colors["primary_pink"],
            fg=self.colors["white"], justify="left"
        ).pack(anchor="w", pady=(0, 20))

        features = ["Create and Manage Appointments", "Monitor Doctor Queue", "Video Call", "Medical Check-Up"]
        for feature in features:
            row = tk.Frame(text_container, bg=self.colors["primary_pink"])
            row.pack(anchor="w", pady=2)
            tk.Label(row, text="✔", fg=self.colors["white"], bg=self.colors["primary_pink"], font=("Arial", 12)).pack(side="left")
            tk.Label(row, text=feature, fg=self.colors["white"], bg=self.colors["primary_pink"], font=("Arial", 12), padx=10).pack(side="left")

        # Right Image
        img_container = tk.Frame(hero_frame, bg=self.colors["primary_pink"])
        img_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        hero_img = self.load_image("assets/landingpic.jpg", (300, 250))
        if hero_img:
            tk.Label(img_container, image=hero_img, bg=self.colors["white"]).pack(expand=True)
        else:
            tk.Label(img_container, text="[Insert: assets/landingpic.jpg]", bg="#ddd", fg="#555", width=40, height=10).pack(expand=True)

    def create_action_cards(self, parent):
        cards_container = tk.Frame(parent, bg=self.colors["white"], pady=20)
        cards_container.pack(fill="x")

        center_frame = tk.Frame(cards_container, bg=self.colors["white"])
        center_frame.pack()

        card_data = [
            ("📋", "Medical Check Up"),
            ("📅", "Doctor Consultation"),
            ("📱", "Contact Us")
        ]

        for icon, title in card_data:
            self.create_card(center_frame, icon, title)

    def create_card(self, parent, icon, title):
        card = tk.Frame(parent, bg=self.colors["primary_blue"], width=250, height=70)
        card.pack(side="left", padx=10)
        card.pack_propagate(False)

        tk.Label(card, text=icon, font=("Arial", 20), bg=self.colors["primary_blue"], fg="white").pack(side="left", padx=15)
        text_frame = tk.Frame(card, bg=self.colors["primary_blue"])
        text_frame.pack(side="left", fill="y", pady=10)
        tk.Label(text_frame, text=title, font=("Arial", 10, "bold"), bg=self.colors["primary_blue"], fg="white",
                 wraplength=120, justify="left").pack(anchor="w")
        tk.Label(card, text=">", font=("Arial", 12, "bold"), bg=self.colors["primary_blue"], fg="white").pack(side="right", padx=10)

    # =========================
    # ARTICLE SECTION
    # =========================
    def create_article_section(self, parent):
        container = tk.Frame(parent, bg=self.colors["white"], pady=20, padx=50)
        container.pack(fill="x")

        header_frame = tk.Frame(container, bg=self.colors["white"])
        header_frame.pack(fill="x", pady=(0, 10))

        tk.Label(
            header_frame, text="Latest from L3AC Clinic",
            font=("Helvetica", 16, "bold"), fg=self.colors["section_header"], bg=self.colors["white"]
        ).pack(side="left")

        tk.Label(
            header_frame, text="See All..>", cursor="hand2",
            font=("Arial", 10, "bold"), fg=self.colors["primary_blue"], bg=self.colors["white"]
        ).pack(side="right")

        tabs_frame = tk.Frame(container, bg=self.colors["white"])
        tabs_frame.pack(fill="x", pady=(0, 20))

        art_tab_frame = tk.Frame(tabs_frame, bg=self.colors["white"])
        art_tab_frame.pack(side="left", padx=(0, 20))
        tk.Label(art_tab_frame, text="Articles", font=("Arial", 11, "bold"), fg=self.colors["primary_blue"], bg=self.colors["white"]).pack()
        tk.Frame(art_tab_frame, bg=self.colors["primary_blue"], height=2, width=50).pack(fill="x", pady=(5, 0))

        tk.Label(tabs_frame, text="Video", font=("Arial", 11), fg="#999", bg=self.colors["white"]).pack(side="left")

        grid_frame = tk.Frame(container, bg=self.colors["white"])
        grid_frame.pack(fill="x")

        articles_data = [
            ("Causes and How to Overcome\nDiabetes", "11 December 2025", "#FFD1DC"),
            ("What is Leptospirosis?\nFind Out The Cause", "11 December 2025", "#D3D3D3"),
            ("Difference Between HIV and AIDS:\nSymptomps and...", "09 December 2025", "#FFCCCB"),
            ("How Tonsillectomy Works\nProcedure and Methods", "04 December 2025", "#ADD8E6")
        ]

        for title, date, color in articles_data:
            self.create_single_article(grid_frame, title, date, color)

    def create_single_article(self, parent, title, date, color):
        card = tk.Frame(parent, bg=self.colors["white"], width=200)
        card.pack(side="left", padx=10, fill="y")

        tk.Label(
            card, text=title, font=self.article_title_font, fg=self.colors["text_dark"],
            bg=self.colors["white"], wraplength=200, justify="left"
        ).pack(anchor="w", pady=(10, 5))

        tk.Label(
            card, text=date, font=self.article_date_font, fg=self.colors["text_gray"],
            bg=self.colors["white"]
        ).pack(anchor="w")

    # =========================
    # ABOUT US
    # =========================
    def show_about(self):
        self.clear_content()
        self.create_section_title(
            self.content_frame,
            "About Us",
            "L3AC Clinic provides modern, fast, and reliable healthcare services."
        )

        wrapper = tk.Frame(self.content_frame, bg=self.colors["white"])
        wrapper.pack(fill="both", expand=True, padx=60, pady=10)

        wrapper.columnconfigure(0, weight=1)
        wrapper.columnconfigure(1, weight=1)

        # LEFT: Image
        left = tk.Frame(wrapper, bg=self.colors["white"])
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 30))

        about_img = self.load_image("assets/about.jpg", (420, 280))
        if about_img:
            tk.Label(left, image=about_img, bg=self.colors["white"]).pack(anchor="w")
        else:
            tk.Label(left, text="[Insert About Image: assets/about.jpg]",
                     bg=self.colors["bg_gray"], fg="#666", width=55, height=12).pack(anchor="w")

        # RIGHT: Text
        right = tk.Frame(wrapper, bg=self.colors["white"])
        right.grid(row=0, column=1, sticky="nsew")

        desc = (
            "At L3AC Clinic, our mission is to make healthcare easier to access.\n\n"
            "We combine technology with professional medical care to help patients:\n"
            "• Book appointments quickly\n"
            "• Monitor doctor queues\n"
            "• Access consultations efficiently\n"
            "• Receive better patient support"
        )

        tk.Label(
            right, text=desc, justify="left",
            bg=self.colors["white"], fg=self.colors["text_dark"],
            font=("Arial", 11), wraplength=420
        ).pack(anchor="w", pady=(0, 15))

        # Highlights
        highlights = tk.Frame(right, bg=self.colors["white"])
        highlights.pack(anchor="w", fill="x")

        for title, body in [
            ("Fast Service", "Smooth queue and appointment flow."),
            ("Trusted Doctors", "Professional medical team."),
            ("Modern System", "Digital-first clinic experience.")
        ]:
            box = tk.Frame(highlights, bg=self.colors["bg_gray"], padx=12, pady=10)
            box.pack(fill="x", pady=6)

            tk.Label(box, text=title, bg=self.colors["bg_gray"], fg=self.colors["text_dark"],
                     font=("Arial", 10, "bold")).pack(anchor="w")
            tk.Label(box, text=body, bg=self.colors["bg_gray"], fg=self.colors["text_gray"],
                     font=("Arial", 9)).pack(anchor="w")

    # =========================
    # SERVICES
    # =========================
    def show_services(self):
        self.clear_content()
        self.create_section_title(
            self.content_frame,
            "Services",
            "Explore what L3AC Clinic can help you with."
        )

        container = tk.Frame(self.content_frame, bg=self.colors["white"])
        container.pack(fill="both", expand=True, padx=60, pady=10)

        for c in range(3):
            container.columnconfigure(c, weight=1)

        services = [
            ("Medical Check-Up", "General health check and screening.", "assets/service_checkup.jpg"),
            ("Doctor Consultation", "Consult with specialists and general doctors.", "assets/service_consult.jpg"),
            ("Online Appointment", "Book your visit quickly with fewer steps.", "assets/service_appointment.jpg"),
            ("Laboratory Tests", "Basic lab tests and diagnostics support.", "assets/service_lab.jpg"),
            ("Vaccination", "Routine and recommended vaccinations.", "assets/service_vaccine.jpg"),
            ("Emergency Support", "Fast response assistance during urgent needs.", "assets/service_emergency.jpg"),
        ]

        def service_card(parent, title, desc, img_path):
            card = tk.Frame(parent, bg=self.colors["bg_gray"], padx=12, pady=12)
            card.pack_propagate(False)

            img = self.load_image(img_path, (220, 140))
            if img:
                tk.Label(card, image=img, bg=self.colors["bg_gray"]).pack(anchor="w")
            else:
                tk.Label(card, text=f"[Insert: {img_path}]", bg="#ddd", fg="#555", width=30, height=7).pack(anchor="w")

            tk.Label(card, text=title, bg=self.colors["bg_gray"], fg=self.colors["text_dark"],
                     font=("Arial", 11, "bold")).pack(anchor="w", pady=(10, 3))
            tk.Label(card, text=desc, bg=self.colors["bg_gray"], fg=self.colors["text_gray"],
                     font=("Arial", 9), wraplength=230, justify="left").pack(anchor="w")

            tk.Button(card, text="Learn More", bg=self.colors["primary_blue"], fg="white",
                      bd=0, padx=12, pady=6, cursor="hand2").pack(anchor="w", pady=(12, 0))

            return card

        r = 0
        c = 0
        for title, desc, img_path in services:
            card = service_card(container, title, desc, img_path)
            card.grid(row=r, column=c, padx=12, pady=12, sticky="nsew")
            card.configure(width=260, height=300)

            c += 1
            if c == 3:
                c = 0
                r += 1

    # =========================
    # DOCTORS
    # =========================
    def show_contact(self):
        self.clear_content()
        self.create_section_title(
            self.content_frame,
            "Doctors",
            "Meet our clinic doctors and specialists."
        )

        container = tk.Frame(self.content_frame, bg=self.colors["white"])
        container.pack(fill="both", expand=True, padx=60, pady=10)

        for c in range(2):
            container.columnconfigure(c, weight=1)

        doctors = [
            ("Dr. Sarah Tan", "Cardiology", "Mon–Fri • 09:00–15:00", "assets/doc1.jpg"),
            ("Dr. Jonathan Lee", "Neurology", "Mon–Thu • 10:00–14:00", "assets/doc2.jpg"),
            ("Dr. Rachel Ong", "Dermatology", "Tue–Sat • 11:00–16:00", "assets/doc3.jpg"),
            ("Dr. Michael Lim", "Orthopedics", "Mon–Fri • 12:00–17:00", "assets/doc4.jpg"),
            ("Dr. Emily Wong", "Pediatrics", "Mon–Fri • 12:00–17:00", "assets/doc5.jpg"),
        ]

        def doctor_card(parent, name, specialty, schedule, img_path):
            card = tk.Frame(parent, bg=self.colors["bg_gray"], padx=14, pady=14)
            img = self.load_image(img_path, (120, 120))

            top = tk.Frame(card, bg=self.colors["bg_gray"])
            top.pack(fill="x")

            if img:
                tk.Label(top, image=img, bg=self.colors["bg_gray"]).pack(side="left", padx=(0, 12))
            else:
                tk.Label(top, text="[Photo]", bg="#ddd", fg="#555", width=12, height=6).pack(side="left", padx=(0, 12))

            info = tk.Frame(top, bg=self.colors["bg_gray"])
            info.pack(side="left", fill="both", expand=True)

            tk.Label(info, text=name, bg=self.colors["bg_gray"], fg=self.colors["text_dark"],
                     font=("Arial", 12, "bold")).pack(anchor="w")
            tk.Label(info, text=specialty, bg=self.colors["bg_gray"], fg=self.colors["primary_blue"],
                     font=("Arial", 10, "bold")).pack(anchor="w", pady=(2, 2))
            tk.Label(info, text=schedule, bg=self.colors["bg_gray"], fg=self.colors["text_gray"],
                     font=("Arial", 9)).pack(anchor="w")

            btns = tk.Frame(card, bg=self.colors["bg_gray"])
            btns.pack(fill="x", pady=(12, 0))

            tk.Button(
                btns, text="View Profile", bg="white", fg=self.colors["text_dark"],
                bd=0, padx=12, pady=6, cursor="hand2"
            ).pack(side="left")

            tk.Button(
                btns, text="Book", bg=self.colors["primary_blue"], fg="white",
                bd=0, padx=18, pady=6, cursor="hand2",
                command=lambda: self.controller.show_view(LoginScreen)
            ).pack(side="right")

            return card


        r = 0
        c = 0
        for name, spec, sched, img in doctors:
            card = doctor_card(container, name, spec, sched, img)
            card.grid(row=r, column=c, padx=12, pady=12, sticky="nsew")

            c += 1
            if c == 2:
                c = 0
                r += 1

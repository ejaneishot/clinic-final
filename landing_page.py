import tkinter as tk
from PIL import Image, ImageTk
from login_view import LoginScreen  # Ensure this import matches your file name
from admin import AdminScreen

class ClinicLandingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # --- THEME CONFIGURATION ---
        self.colors = {
            "primary_pink": "#2576B8",    # Using your Blue/Teal tone
            "primary_blue": "#00A3E0",    
            "accent_orange": "#2981C9",   
            "white": "#FFFFFF",
            "text_dark": "#333333",
            "text_light": "#FFFFFF",
            "text_gray": "#777777",       # Added for dates
            "bg_gray": "#F0F0F0",
            "section_header": "#0099CC"   # Specific blue from your image
        }
        
        # Configure Main Background
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

    def create_navbar(self):
        """Creates the top white navigation bar"""
        nav_frame = tk.Frame(self, bg=self.colors["white"], height=70)
        nav_frame.pack(side="top", fill="x", ipadx=10, ipady=10)
        
        # Logo
        logo_frame = tk.Frame(nav_frame, bg=self.colors["white"])
        logo_frame.pack(side="left", padx=30)
        
        tk.Label(logo_frame, text="🏥", font=("Arial", 24), bg=self.colors["white"]).pack(side="left")
        tk.Label(logo_frame, text="L3AC\nClinic", justify="left", 
                 font=("Arial", 10, "bold"), fg=self.colors["primary_pink"], bg=self.colors["white"]).pack(side="left", padx=5)

        # Search Bar
        search_frame = tk.Frame(nav_frame, bg=self.colors["bg_gray"], padx=10, pady=5)
        search_frame.pack(side="left", padx=50)
        tk.Label(search_frame, text="Search...", bg=self.colors["bg_gray"], fg="#999").pack()

        # --- LOGIN BUTTON ---
        login_btn = tk.Button(nav_frame, text="Login", bg=self.colors["accent_orange"], 
                              fg=self.colors["white"], font=("Arial", 10, "bold"), 
                              bd=0, padx=20, pady=8, cursor="hand2",
                              command=lambda: self.controller.show_view(LoginScreen)) 
        login_btn.pack(side="right", padx=30)


        # Menu Links
        links_frame = tk.Frame(nav_frame, bg=self.colors["white"])
        links_frame.pack(side="right", padx=20)
        
        menu_items = [
            ("Home", "Home"), ("About Us", "About Us"), 
            ("Services", "Services"), ("Doctors", "Contact")
        ]
        
        for label, page_name in menu_items:
            btn = tk.Label(links_frame, text=label, bg=self.colors["white"], fg=self.colors["text_dark"],
                           font=("Arial", 10, "bold"), cursor="hand2")
            btn.pack(side="left", padx=15)
            btn.bind("<Button-1>", lambda e, p=page_name: self.navigate(p))
            btn.bind("<Enter>", lambda e, b=btn: b.config(fg=self.colors["primary_blue"]))
            btn.bind("<Leave>", lambda e, b=btn: b.config(fg=self.colors["text_dark"]))

    def go_to_admin(self):
        """Switches to Admin Screen with lazy import to prevent crash"""
        # We import inside the function to avoid 'Circular Import' errors
        import admin 
        self.controller.show_view(admin.AdminScreen)

    def navigate(self, page_name):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if page_name == "Home": self.show_home()
        elif page_name == "About Us": self.show_about()
        elif page_name == "Services": self.show_services()
        elif page_name == "Contact": self.show_contact()

    # --- HOME PAGE LOGIC ---
    def show_home(self):
        # 1. Hero Section
        self.create_hero_section(self.content_frame)
        # 2. Action Cards
        self.create_action_cards(self.content_frame)
        # 3. Article Section (NEW)
        self.create_article_section(self.content_frame)

    def create_hero_section(self, parent):
        hero_frame = tk.Frame(parent, bg=self.colors["primary_pink"])
        hero_frame.pack(fill="x", ipady=20) 

        hero_frame.columnconfigure(0, weight=1) 
        hero_frame.columnconfigure(1, weight=1) 

        # Left Text
        text_container = tk.Frame(hero_frame, bg=self.colors["primary_pink"])
        text_container.grid(row=0, column=0, sticky="ns", padx=50, pady=30)

        tk.Label(text_container, text="L3AC Clinic", 
                 font=("Helvetica", 36, "bold"), bg=self.colors["primary_pink"], 
                 fg=self.colors["white"], justify="left").pack(anchor="w", pady=(0, 20))

        features = ["Create and Manage Appointments", "Monitor Doctor Queue", "Video Call", "Medical Check-Up"]
        for feature in features:
            row = tk.Frame(text_container, bg=self.colors["primary_pink"])
            row.pack(anchor="w", pady=2)
            tk.Label(row, text="✔", fg=self.colors["white"], bg=self.colors["primary_pink"], font=("Arial", 12)).pack(side="left")
            tk.Label(row, text=feature, fg=self.colors["white"], bg=self.colors["primary_pink"], font=("Arial", 12), padx=10).pack(side="left")

        # Right Image
        img_container = tk.Frame(hero_frame, bg=self.colors["primary_pink"])
        img_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        raw_image = Image.open("assets/landingpic.jpg")
        resized_image = raw_image.resize((300, 250), Image.Resampling.LANCZOS)
        self.hero_photo = ImageTk.PhotoImage(resized_image)
        img_label = tk.Label(img_container, image=self.hero_photo, bg=self.colors["white"])
        img_label.pack(expand=True)

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
        tk.Label(text_frame, text=title, font=("Arial", 10, "bold"), bg=self.colors["primary_blue"], fg="white", wraplength=120, justify="left").pack(anchor="w")
        tk.Label(card, text=">", font=("Arial", 12, "bold"), bg=self.colors["primary_blue"], fg="white").pack(side="right", padx=10)

    # --- ARTICLE SECTION ---
    def create_article_section(self, parent):
        container = tk.Frame(parent, bg=self.colors["white"], pady=20, padx=50)
        container.pack(fill="x")

        # 1. Header Row
        header_frame = tk.Frame(container, bg=self.colors["white"])
        header_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(header_frame, text="Latest from L3AC Clinic", 
                 font=("Helvetica", 16, "bold"), fg=self.colors["section_header"], bg=self.colors["white"]).pack(side="left")
        
        tk.Label(header_frame, text="See All..>", cursor="hand2",
                 font=("Arial", 10, "bold"), fg=self.colors["primary_blue"], bg=self.colors["white"]).pack(side="right")

        # 2. Tabs (Artikel / Video)
        tabs_frame = tk.Frame(container, bg=self.colors["white"])
        tabs_frame.pack(fill="x", pady=(0, 20))
        
        # 'Artikel' Tab 
        art_tab_frame = tk.Frame(tabs_frame, bg=self.colors["white"])
        art_tab_frame.pack(side="left", padx=(0, 20))
        tk.Label(art_tab_frame, text="Articles", font=("Arial", 11, "bold"), fg=self.colors["primary_blue"], bg=self.colors["white"]).pack()
        tk.Frame(art_tab_frame, bg=self.colors["primary_blue"], height=2, width=50).pack(fill="x", pady=(5,0)) 

        # 'Video' Tab
        tk.Label(tabs_frame, text="Video", font=("Arial", 11), fg="#999", bg=self.colors["white"]).pack(side="left")

        # 3. Articles Grid
        grid_frame = tk.Frame(container, bg=self.colors["white"])
        grid_frame.pack(fill="x")

        # Data 
        articles_data = [
            ("Causes and How to Overcome\nDiabetes", "11 December 2025", "#FFD1DC"), 
            ("What is Leptospirosis?\nFind Out The Cause", "11 December 2025", "#D3D3D3"),   
            ("Difference Between HIV and AIDS:\nSymptomps and...", "09 December 2025", "#FFCCCB"),      
            ("How Tonsillectomy Works\nProcedure and Methods", "04 December 2025", "#ADD8E6")     
        ]

        for title, date, color in articles_data:
            self.create_single_article(grid_frame, title, date, color)

    def create_single_article(self, parent, title, date, color):
        """Creates a single article card with image placeholder"""
        card = tk.Frame(parent, bg=self.colors["white"], width=200) 
        card.pack(side="left", padx=10, fill="y")
        
        
        # Title
        tk.Label(card, text=title, font=self.article_title_font, fg=self.colors["text_dark"], 
                 bg=self.colors["white"], wraplength=200, justify="left").pack(anchor="w", pady=(10, 5))
        
        # Date
        tk.Label(card, text=date, font=self.article_date_font, fg=self.colors["text_gray"], 
                 bg=self.colors["white"]).pack(anchor="w")

    # --- OTHER PAGES ---
    def show_about(self):
        tk.Label(self.content_frame, text="About Us", font=self.header_font, bg=self.colors["white"]).pack(pady=20)

    def show_services(self):
        tk.Label(self.content_frame, text="Services", font=self.header_font, bg=self.colors["white"]).pack(pady=20)

    def show_contact(self):
        tk.Label(self.content_frame, text="Contact / Doctors", font=self.header_font, bg=self.colors["white"]).pack(pady=20)
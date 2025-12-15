import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import database
import login_view


class PatientScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.pid = controller.current_user_id

        # Fetch current patient name
        p = database.fetch_all("SELECT patientName FROM patient WHERE patientID=%s", (self.pid,))[0]

        # --- HEADER ---
        header = tk.Frame(self, bg="#e3f2fd", pady=15)
        header.pack(fill="x")
        tk.Label(header, text=f"Hello, {p['patientName']}", bg="#e3f2fd", font=("Arial", 14)).pack(side="left", padx=20)
        tk.Button(header, text="Logout", command=lambda: controller.show_view(login_view.LoginScreen)).pack(
            side="right", padx=20)

        # --- BOOKING FORM ---
        form = tk.LabelFrame(self, text="Request New Appointment", padx=10, pady=10)
        form.pack(padx=20, pady=10, fill="x")

        # Doctor Selection
        tk.Label(form, text="Select Doctor:").grid(row=0, column=0, sticky="w")
        docs = database.fetch_all("SELECT doctorID, doctorName, doctorSpecialty FROM doctor")
        self.doc_map = {f"{d['doctorName']} ({d['doctorSpecialty']})": d['doctorID'] for d in docs}
        self.cb_doc = ttk.Combobox(form, values=list(self.doc_map.keys()), width=35)
        self.cb_doc.grid(row=0, column=1, padx=10)

        # Date Selection (Dropdowns)
        tk.Label(form, text="Date:").grid(row=1, column=0, sticky="w")
        d_frame = tk.Frame(form)
        d_frame.grid(row=1, column=1, sticky="w", padx=10)
        self.cb_day = ttk.Combobox(d_frame, values=[str(i).zfill(2) for i in range(1, 32)], width=3)
        self.cb_month = ttk.Combobox(d_frame, values=[str(i).zfill(2) for i in range(1, 13)], width=3)
        self.cb_year = ttk.Combobox(d_frame, values=["2025", "2026"], width=5)

        self.cb_day.pack(side="left")
        self.cb_month.pack(side="left")
        self.cb_year.pack(side="left")

        # Set defaults
        self.cb_day.set("01")
        self.cb_month.set("01")
        self.cb_year.set("2025")

        # Time Selection
        tk.Label(form, text="Time:").grid(row=2, column=0, sticky="w")
        self.cb_time = ttk.Combobox(form,
                                    values=["09:00 AM", "10:00 AM", "11:00 AM", "01:00 PM", "02:00 PM", "03:00 PM"])
        self.cb_time.grid(row=2, column=1, padx=10, sticky="w")

        tk.Button(form, text="Book Now", bg="#4CAF50", fg="white", command=self.book).grid(row=3, columnspan=2, pady=15)

        # --- HISTORY TABLE ---
        cols = ("Date", "Time", "Doctor", "Room", "Status", "Cost")
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        for c in cols: self.tree.heading(c, text=c)
        self.tree.pack(padx=20, fill="both", expand=True)
        self.refresh()

    def refresh(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        rows = database.fetch_all("""
            SELECT a.appointmentDate, a.appointmentTime, a.appointmentStatus, d.doctorName, a.roomNumber, p.paymentAmount
            FROM appointment a JOIN doctor d ON a.doctorID=d.doctorID LEFT JOIN payment p ON a.paymentID=p.paymentID
            WHERE a.patientID=%s ORDER BY a.appointmentDate DESC
        """, (self.pid,))
        for r in rows:
            cost = f"${r['paymentAmount']}" if r['paymentAmount'] else "-"
            room = r['roomNumber'] if r['roomNumber'] else "-"
            self.tree.insert("", "end", values=(
                r['appointmentDate'], r['appointmentTime'], r['doctorName'], room, r['appointmentStatus'], cost
            ))

    def book(self):
        try:
            # 1. Gather Input Data
            if not self.cb_doc.get():
                return messagebox.showerror("Error", "Please select a doctor.")

            did = self.doc_map[self.cb_doc.get()]
            date_str = f"{self.cb_year.get()}-{self.cb_month.get()}-{self.cb_day.get()}"
            time_str = self.cb_time.get()

            if not time_str:
                return messagebox.showerror("Error", "Please select a time.")

            # --- LOGIC: LINEAR TIMELINE CHECK ---
            # "The next appointment cannot be before the one already set."

            # A. Convert user's desired time to a compare-able object
            new_booking_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %I:%M %p")

            # B. Get the patient's LATEST active appointment from DB
            last_appt_rows = database.fetch_all("""
                SELECT appointmentDate, appointmentTime 
                FROM appointment 
                WHERE patientID=%s AND appointmentStatus != 'Cancelled'
                ORDER BY appointmentDate DESC, appointmentTime DESC 
                LIMIT 1
            """, (self.pid,))

            if last_appt_rows:
                # Parse the database record
                last_date = last_appt_rows[0]['appointmentDate']  # String: "2025-10-10"
                last_time = last_appt_rows[0]['appointmentTime']  # String: "09:00 AM"

                # Create a datetime object for the existing appointment
                last_booking_dt = datetime.strptime(f"{last_date} {last_time}", "%Y-%m-%d %I:%M %p")

                # C. The Comparison: Is the New Date BEHIND the Old Date?
                if new_booking_dt <= last_booking_dt:
                    return messagebox.showerror(
                        "Sequence Error",
                        f"Impossible Sequence.\n\nYou already have an appointment scheduled for:\n{last_date} at {last_time}\n\nYour next appointment must be AFTER this date."
                    )
            # -------------------------------------

            # 2. Check Availability (Standard Check)
            room = database.fetch_all("SELECT assignedRoom FROM doctor WHERE doctorID=%s", (did,))[0]['assignedRoom']
            if not database.is_slot_available(room, date_str, time_str):
                return messagebox.showerror("Unavailable", "Doctor/Room is busy at this time!")

            # 3. Create Payment & Appointment Records
            pay_id = database.execute_query("INSERT INTO payment (paymentAmount, paymentStatus) VALUES (0, 'Pending')")

            database.execute_query(
                "INSERT INTO appointment (patientID, doctorID, roomNumber, paymentID, appointmentDate, appointmentTime, appointmentStatus) VALUES (%s, %s, %s, %s, %s, %s, 'Pending')",
                (self.pid, did, room, pay_id, date_str, time_str)
            )

            database.set_room_status(room, 'Occupied')

            messagebox.showinfo("Success", "Booking Sent!")
            self.refresh()

        except ValueError:
            messagebox.showerror("Error", "Invalid Date selected.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import database


class AdminScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Header
        header = tk.Frame(self, bg="#222", height=50)
        header.pack(fill="x")
        tk.Label(header, text="ADMINISTRATION DASHBOARD", fg="white", bg="#222", font=("Arial", 16, "bold")).pack(
            side="left", padx=20)
        tk.Button(header, text="Logout", command=self.logout).pack(side="right", padx=20)

        # Tabs
        tabs = ttk.Notebook(self)
        tabs.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_sched = tk.Frame(tabs)
        self.tab_finance = tk.Frame(tabs)
        self.tab_patients = tk.Frame(tabs)
        self.tab_doctors = tk.Frame(tabs)
        self.tab_staff = tk.Frame(tabs)
        self.tab_rooms = tk.Frame(tabs)

        tabs.add(self.tab_sched, text="Master Schedule")
        tabs.add(self.tab_finance, text="Transactions")
        tabs.add(self.tab_patients, text="Manage Patients")
        tabs.add(self.tab_doctors, text="Manage Doctors")
        tabs.add(self.tab_staff, text="Manage Staff")
        tabs.add(self.tab_rooms, text="Manage Rooms")

        self.setup_schedule()
        self.setup_finance()
        self.setup_patients()
        self.setup_doctors()
        self.setup_staff()
        self.setup_rooms()

    def logout(self):
        from login_view import LoginScreen
        self.controller.show_view(LoginScreen)

    # ==========================
    # TAB 1: MASTER SCHEDULE
    # ==========================
    def setup_schedule(self):
        tools = tk.Frame(self.tab_sched, pady=10)
        tools.pack(fill="x")

        tk.Button(tools, text="1. Verify & Schedule", bg="green", fg="white", command=self.verify_window).pack(
            side="left", padx=5)
        tk.Button(tools, text="2. Cancel Appt", bg="orange", fg="white", command=self.cancel_appointment).pack(
            side="left", padx=5)
        tk.Button(tools, text="Reschedule (Cancel & Rebook)", bg="blue", fg="white",
                  command=self.reschedule_appointment).pack(side="left", padx=5)
        tk.Button(tools, text="3. Delete Record", bg="red", fg="white", command=self.delete_record).pack(side="left",
                                                                                                         padx=5)

        # New Booking Button
        tk.Button(tools, text="+ New Booking", command=self.add_appointment_window).pack(side="right", padx=5)

        cols = ("ID", "Date", "Time", "Patient", "Doctor", "Room", "Staff", "Status", "Treatment", "Notes")
        self.tree_appt = ttk.Treeview(self.tab_sched, columns=cols, show='headings', height=15)
        for c in cols: self.tree_appt.heading(c, text=c)

        self.tree_appt.column("ID", width=30)
        self.tree_appt.column("Room", width=50)
        self.tree_appt.column("Status", width=80)
        self.tree_appt.pack(fill="both", expand=True)

        self.refresh_schedule()

    def refresh_schedule(self):
        for i in self.tree_appt.get_children(): self.tree_appt.delete(i)
        rows = database.fetch_all("""
            SELECT a.id, a.appointmentDate, a.appointmentTime, p.patientName, d.doctorName, 
                   a.roomNumber, a.appointmentStatus, t.treatment, a.doctorNotes, s.staffName
            FROM appointment a 
            JOIN patient p ON a.patientID=p.patientID 
            JOIN doctor d ON a.doctorID=d.doctorID
            LEFT JOIN treatment t ON a.treatmentID=t.treatmentID
            LEFT JOIN staff s ON a.staffID=s.staffID
            ORDER BY a.appointmentDate DESC
        """)
        for r in rows:
            treat = r['treatment'] if r['treatment'] else "-"
            note = r['doctorNotes'] if r['doctorNotes'] else "-"
            room = r['roomNumber'] if r['roomNumber'] else "-"
            staff = r['staffName'] if r['staffName'] else "Unassigned"
            self.tree_appt.insert("", "end", values=(
                r['id'], r['appointmentDate'], r['appointmentTime'], r['patientName'],
                r['doctorName'], room, staff, r['appointmentStatus'], treat, note
            ))

    # ==========================
    # TAB 2: TRANSACTIONS (Updated with Date)
    # ==========================
    def setup_finance(self):
        tk.Label(self.tab_finance, text="Payment History", font=("Arial", 12, "bold")).pack(pady=10)

        # Columns: Added "Trans. Date"
        cols = ("Pay ID", "Trans. Date", "Patient", "Amount", "Status")

        self.tree_fin = ttk.Treeview(self.tab_finance, columns=cols, show='headings')
        for c in cols: self.tree_fin.heading(c, text=c)

        self.tree_fin.column("Pay ID", width=50)
        self.tree_fin.column("Trans. Date", width=100)
        self.tree_fin.column("Patient", width=150)
        self.tree_fin.column("Amount", width=80)
        self.tree_fin.column("Status", width=80)

        self.tree_fin.pack(fill="both", expand=True)
        self.refresh_finance()

    def refresh_finance(self):
        # Clear the table first
        for i in self.tree_fin.get_children(): self.tree_fin.delete(i)

        # 1. FETCH BOTH DATES (paymentDate AND appointmentDate)
        rows = database.fetch_all("""
            SELECT pay.paymentID, pay.paymentDate, a.appointmentDate, 
                   pt.patientName, pay.paymentAmount, pay.paymentStatus
            FROM payment pay 
            JOIN appointment a ON pay.paymentID = a.paymentID
            JOIN patient pt ON a.patientID = pt.patientID 
            ORDER BY pay.paymentID DESC
        """)

        for r in rows:
            # 2. THE FALLBACK LOGIC
            # If paymentDate exists, use it. If not, use appointmentDate.
            if r['paymentDate']:
                display_date = r['paymentDate']
            else:
                display_date = f"{r['appointmentDate']} (Est.)"

            self.tree_fin.insert("", "end", values=(
                r['paymentID'],
                display_date,            # Shows the calculated date
                r['patientName'],
                f"${r['paymentAmount']}",
                r['paymentStatus']
            ))

    # ==========================
    # TAB 3: PATIENTS
    # ==========================
    def setup_patients(self):
        form = tk.Frame(self.tab_patients, pady=10)
        form.pack()

        inputs = [("Name:", 15), ("Gender:", 8), ("DOB:", 10), ("Phone:", 12)]
        self.pat_entries = []
        for lbl, w in inputs:
            tk.Label(form, text=lbl).pack(side="left")
            e = tk.Entry(form, width=w)
            e.pack(side="left", padx=2)
            self.pat_entries.append(e)

        self.ent_p_name, self.ent_p_gen, self.ent_p_dob, self.ent_p_phone = self.pat_entries

        tk.Button(form, text="Add", bg="#333", fg="white", command=self.add_patient).pack(side="left", padx=10)
        tk.Button(form, text="Remove", bg="red", fg="white", command=self.del_patient).pack(side="left")

        self.tree_pat = ttk.Treeview(self.tab_patients, columns=("ID", "Name", "Gender", "Phone"), show='headings')
        for c in ("ID", "Name", "Gender", "Phone"): self.tree_pat.heading(c, text=c)
        self.tree_pat.pack(fill="both", expand=True)
        self.refresh_patients()

    def refresh_patients(self):
        for i in self.tree_pat.get_children(): self.tree_pat.delete(i)
        for r in database.fetch_all("SELECT * FROM patient"):
            self.tree_pat.insert("", "end",
                                 values=(r['patientID'], r['patientName'], r['patientGender'], r['patientPhoneNumber']))

    def add_patient(self):
        database.execute_query(
            "INSERT INTO patient (patientName, patientGender, patientBirthDate, patientPhoneNumber) VALUES (%s, %s, %s, %s)",
            (self.ent_p_name.get(), self.ent_p_gen.get(), self.ent_p_dob.get(), self.ent_p_phone.get()))
        self.refresh_patients()

    def del_patient(self):
        pid = self.get_sel_id(self.tree_pat)
        if pid and database.execute_query("DELETE FROM patient WHERE patientID=%s", (pid,)):
            self.refresh_patients()
        else:
            messagebox.showerror("Error", "Cannot delete: Patient has records.")

    # ==========================
    # TAB 4: DOCTORS
    # ==========================
    def setup_doctors(self):
        form = tk.Frame(self.tab_doctors, pady=10)
        form.pack()

        tk.Label(form, text="Name:").pack(side="left")
        self.ent_d_name = tk.Entry(form, width=15);
        self.ent_d_name.pack(side="left", padx=5)
        tk.Label(form, text="Spec:").pack(side="left")
        self.ent_d_spec = tk.Entry(form, width=15);
        self.ent_d_spec.pack(side="left", padx=5)

        tk.Label(form, text="Room:").pack(side="left")
        self.cb_d_room = ttk.Combobox(form, width=5)
        self.cb_d_room.pack(side="left", padx=5)

        tk.Button(form, text="Add", bg="#333", fg="white", command=self.add_doctor).pack(side="left", padx=10)
        tk.Button(form, text="Remove", bg="red", fg="white", command=self.del_doctor).pack(side="left")

        self.tree_doc = ttk.Treeview(self.tab_doctors, columns=("ID", "Name", "Spec", "Room"), show='headings')
        for c in ("ID", "Name", "Spec", "Room"): self.tree_doc.heading(c, text=c)
        self.tree_doc.pack(fill="both", expand=True)
        self.refresh_doctors()

    def refresh_doctors(self):
        rooms = database.fetch_all("SELECT roomNumber FROM room")
        self.cb_d_room['values'] = [r['roomNumber'] for r in rooms]
        for i in self.tree_doc.get_children(): self.tree_doc.delete(i)
        for r in database.fetch_all("SELECT * FROM doctor"):
            self.tree_doc.insert("", "end",
                                 values=(r['doctorID'], r['doctorName'], r['doctorSpecialty'], r['assignedRoom']))

    def add_doctor(self):
        database.execute_query("INSERT INTO doctor (doctorName, doctorSpecialty, assignedRoom) VALUES (%s, %s, %s)",
                               (self.ent_d_name.get(), self.ent_d_spec.get(), self.cb_d_room.get()))
        self.refresh_doctors()

    def del_doctor(self):
        did = self.get_sel_id(self.tree_doc)
        if did and database.execute_query("DELETE FROM doctor WHERE doctorID=%s", (did,)):
            self.refresh_doctors()
        else:
            messagebox.showerror("Error", "Cannot delete: Doctor has records.")

    # ==========================
    # TAB 5: STAFF
    # ==========================
    def setup_staff(self):
        form = tk.Frame(self.tab_staff, pady=10)
        form.pack()
        tk.Label(form, text="Name:").pack(side="left")
        self.ent_s_name = tk.Entry(form);
        self.ent_s_name.pack(side="left", padx=5)
        tk.Label(form, text="Role:").pack(side="left")
        self.ent_s_role = tk.Entry(form);
        self.ent_s_role.pack(side="left", padx=5)
        tk.Button(form, text="Add", bg="#333", fg="white", command=self.add_staff).pack(side="left", padx=10)
        tk.Button(form, text="Remove", bg="red", fg="white", command=self.del_staff).pack(side="left")

        self.tree_staff = ttk.Treeview(self.tab_staff, columns=("ID", "Name", "Role"), show='headings')
        for c in ("ID", "Name", "Role"): self.tree_staff.heading(c, text=c)
        self.tree_staff.pack(fill="both", expand=True)
        self.refresh_staff()

    def refresh_staff(self):
        for i in self.tree_staff.get_children(): self.tree_staff.delete(i)
        for r in database.fetch_all("SELECT * FROM staff"):
            self.tree_staff.insert("", "end", values=(r['staffID'], r['staffName'], r['staffRole']))

    def add_staff(self):
        database.execute_query("INSERT INTO staff (staffName, staffRole) VALUES (%s, %s)",
                               (self.ent_s_name.get(), self.ent_s_role.get()))
        self.refresh_staff()

    def del_staff(self):
        sid = self.get_sel_id(self.tree_staff)
        if sid:
            database.execute_query("DELETE FROM staff WHERE staffID=%s", (sid,))
            self.refresh_staff()

    # ==========================
    # TAB 6: ROOMS
    # ==========================
    def setup_rooms(self):
        form = tk.Frame(self.tab_rooms, pady=10)
        form.pack()
        tk.Label(form, text="Room Number:").pack(side="left")
        self.ent_room = tk.Entry(form);
        self.ent_room.pack(side="left", padx=5)
        tk.Button(form, text="Add", bg="#333", fg="white", command=self.add_room).pack(side="left", padx=10)
        tk.Button(form, text="Remove", bg="red", fg="white", command=self.del_room).pack(side="left")

        self.tree_room = ttk.Treeview(self.tab_rooms, columns=("Number", "Status"), show='headings')
        for c in ("Number", "Status"): self.tree_room.heading(c, text=c)
        self.tree_room.pack(fill="both", expand=True)
        self.refresh_rooms()

    def refresh_rooms(self):
        for i in self.tree_room.get_children(): self.tree_room.delete(i)
        for r in database.fetch_all("SELECT * FROM room"):
            self.tree_room.insert("", "end", values=(r['roomNumber'], r['roomStatus']))

    def add_room(self):
        database.execute_query("INSERT INTO room (roomNumber, roomStatus) VALUES (%s, 'Available')",
                               (self.ent_room.get(),))
        self.refresh_rooms()

    def del_room(self):
        rid = self.get_sel_id(self.tree_room)
        if rid:
            database.execute_query("DELETE FROM room WHERE roomNumber=%s", (rid,))
            self.refresh_rooms()

    # ==========================
    # CORE ACTIONS (Logic)
    # ==========================
    def get_sel_id(self, tree):
        sel = tree.selection()
        return tree.item(sel[0])['values'][0] if sel else None

    # --- ADD APPOINTMENT POPUP (Includes Validation & Reschedule logic) ---
    def add_appointment_window(self, block_date=None, block_time=None):
        top = tk.Toplevel(self)
        top.title("Book New Appointment")
        top.geometry("400x350")

        title_text = "Reschedule Appointment" if block_date else "New Booking"
        tk.Label(top, text=title_text, font=("Arial", 14, "bold")).pack(pady=10)

        # Helper to create fields
        def make_field(label_text):
            tk.Label(top, text=label_text).pack()
            e = tk.Entry(top)
            e.pack()
            return e

        e_pid = make_field("Patient ID:")
        e_did = make_field("Doctor ID:")
        e_date = make_field("Date (YYYY-MM-DD):")
        e_time = make_field("Time (HH:MM):")

        def save_new_booking():
            pid, did, date, time = e_pid.get(), e_did.get(), e_date.get(), e_time.get()
            if not (pid and did and date and time):
                return messagebox.showerror("Error", "All fields are required!", parent=top)

            # --- VALIDATION: Prevent Past Dates ---
            try:
                input_date_obj = datetime.strptime(date, "%Y-%m-%d").date()
                today = datetime.now().date()
                if input_date_obj < today:
                    return messagebox.showerror("Logic Error", "Cannot book an appointment in the past!", parent=top)
            except ValueError:
                return messagebox.showerror("Format Error", "Date must be YYYY-MM-DD", parent=top)
            # --------------------------------------

            # --- VALIDATION: Reschedule Restriction (Block old slot) ---
            if block_date and block_time:
                # Basic string comparison to prevent exact rebooking
                if str(date) == str(block_date) and str(time) == str(block_time):
                    return messagebox.showerror(
                        "Reschedule Error",
                        f"You cannot reschedule to the same slot ({date} at {time}).\nPlease pick a different time.",
                        parent=top
                    )
            # -----------------------------------------------------------

            # Insert Booking (Status: Pending)
            database.execute_query("""
                INSERT INTO appointment (appointmentDate, appointmentTime, appointmentStatus, 
                                         patientID, doctorID, paymentID, staffID)
                VALUES (%s, %s, 'Pending', %s, %s, NULL, NULL)
            """, (date, time, pid, did))

            # Generate Payment Record (WITH DATE) & Link it
            last_id = database.fetch_all("SELECT MAX(id) as mid FROM appointment")[0]['mid']

            # --- UPDATED INSERT: Uses CURDATE() ---
            database.execute_query("""
                INSERT INTO payment (paymentAmount, paymentStatus, paymentDate, appointmentID) 
                VALUES (0, 'Pending', CURDATE(), %s)
            """, (last_id,))

            # Link back (Redundant safety, but good to keep)
            database.execute_query("UPDATE appointment SET paymentID=(SELECT MAX(paymentID) FROM payment) WHERE id=%s",
                                   (last_id,))

            messagebox.showinfo("Success", "New appointment created!\nPlease VERIFY it to assign a room.", parent=top)
            self.refresh_schedule()
            top.destroy()

        tk.Button(top, text="Confirm Booking", bg="green", fg="white", command=save_new_booking).pack(pady=20)

    # --- VERIFY & SCHEDULE ---
    def verify_window(self):
        sel = self.tree_appt.selection()
        if not sel: return

        item = self.tree_appt.item(sel[0])
        status = item['values'][7]
        if status in ['Cancelled', 'Completed']:
            return messagebox.showerror("Error", f"Appointment is {status}.")

        self.ver_id = item['values'][0]
        date, time = item['values'][1], item['values'][2]

        self.win = tk.Toplevel(self)
        self.win.title("Assign Staff")
        tk.Label(self.win, text="Select Staff:", font=("bold")).pack(pady=10)

        avail_staff = database.get_available_staff(date, time)
        self.staff_map = {f"{s['staffName']} ({s['staffRole']})": s['staffID'] for s in avail_staff}

        self.cb_staff = ttk.Combobox(self.win, values=list(self.staff_map.keys()), width=30)
        self.cb_staff.pack(pady=5)
        tk.Button(self.win, text="Confirm", bg="green", fg="white", command=self.confirm_verify).pack(pady=10)

    def confirm_verify(self):
        if not self.cb_staff.get(): return messagebox.showerror("Error", "Select Staff")
        sid = self.staff_map[self.cb_staff.get()]
        database.execute_query("UPDATE appointment SET appointmentStatus='Scheduled', staffID=%s WHERE id=%s",
                               (sid, self.ver_id))
        self.win.destroy()
        self.refresh_schedule()

    # --- CANCEL APPOINTMENT ---
    def cancel_appointment(self):
        aid = self.get_sel_id(self.tree_appt)
        if not aid: return

        status = self.tree_appt.item(self.tree_appt.selection()[0])['values'][7]
        if status in ['Cancelled', 'Completed']:
            return messagebox.showerror("Error", f"Cannot cancel {status} visit.")

        if messagebox.askyesno("Confirm", "Cancel this appointment?"):
            rows = database.fetch_all("SELECT roomNumber FROM appointment WHERE id=%s", (aid,))
            if rows and rows[0]['roomNumber']:
                database.execute_query("UPDATE room SET roomStatus='Available' WHERE roomNumber=%s",
                                       (rows[0]['roomNumber'],))
            database.execute_query("UPDATE appointment SET appointmentStatus='Cancelled' WHERE id=%s", (aid,))
            self.refresh_schedule()

    # --- DELETE RECORD ---
    def delete_record(self):
        aid = self.get_sel_id(self.tree_appt)
        if not aid: return

        status = self.tree_appt.item(self.tree_appt.selection()[0])['values'][7]
        if status == 'Scheduled':
            return messagebox.showerror("Restricted", "Cannot delete 'Scheduled' appointment.\nPlease CANCEL it first.")

        msg = "Are you sure? This effectively deletes the record forever."
        if status == 'Completed':
            msg = "WARNING: Deleting a COMPLETED medical record. Continue?"

        if messagebox.askyesno("Confirm Delete", msg):
            rows = database.fetch_all("SELECT roomNumber FROM appointment WHERE id=%s", (aid,))
            if rows and rows[0]['roomNumber']:
                database.execute_query("UPDATE room SET roomStatus='Available' WHERE roomNumber=%s",
                                       (rows[0]['roomNumber'],))
            database.execute_query("DELETE FROM appointment WHERE id=%s", (aid,))
            self.refresh_schedule()

    # --- RESCHEDULE LOGIC (Cancel + Rebook) ---
    def reschedule_appointment(self):
        aid = self.get_sel_id(self.tree_appt)
        if not aid: return

        # Get item details
        item = self.tree_appt.item(self.tree_appt.selection()[0])
        status = item['values'][7]
        old_date = item['values'][1]  # Column 1 is Date
        old_time = item['values'][2]  # Column 2 is Time

        if status != 'Scheduled':
            return messagebox.showerror("Error", "Only 'Scheduled' items can be rescheduled.")

        if messagebox.askyesno("Reschedule",
                               "To reschedule, we must CANCEL the current slot and create a NEW one.\n\nProceed?"):
            # 1. Free room and Cancel
            rows = database.fetch_all("SELECT roomNumber FROM appointment WHERE id=%s", (aid,))
            if rows and rows[0]['roomNumber']:
                database.execute_query("UPDATE room SET roomStatus='Available' WHERE roomNumber=%s",
                                       (rows[0]['roomNumber'],))
            database.execute_query("UPDATE appointment SET appointmentStatus='Cancelled' WHERE id=%s", (aid,))
            self.refresh_schedule()

            # 2. Open new booking window (Passing old date/time to BLOCK them)
            messagebox.showinfo("Step 2", "Original cancelled. Opening booking window.")
            self.add_appointment_window(block_date=old_date, block_time=old_time)
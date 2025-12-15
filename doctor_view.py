import tkinter as tk
from tkinter import ttk, messagebox
import database
import login_view


class DoctorScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.did = controller.current_user_id

        doc = database.fetch_all("SELECT doctorName, assignedRoom, doctorSpecialty FROM doctor WHERE doctorID=%s",
                                 (self.did,))[0]

        header = tk.Frame(self, bg="#eee", pady=15)
        header.pack(fill="x")
        tk.Label(header, text=f"Dr. {doc['doctorName']}", font=("Arial", 16, "bold"), bg="#eee").pack(side="left",
                                                                                                      padx=20)
        tk.Label(header, text=f"{doc['doctorSpecialty']} | Room: {doc['assignedRoom']}", bg="#eee").pack(side="left")
        tk.Button(header, text="Logout", command=lambda: controller.show_view(login_view.LoginScreen)).pack(
            side="right", padx=20)

        cols = ("ID", "Time", "Patient", "Status", "Current Notes")
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        for c in cols: self.tree.heading(c, text=c)
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        f_act = tk.LabelFrame(self, text="Consultation", padx=10, pady=10)
        f_act.pack(fill="x", padx=20, pady=10)

        tk.Label(f_act, text="Notes:").pack(side="left")
        self.en_note = tk.Entry(f_act, width=40);
        self.en_note.pack(side="left", padx=10)

        tk.Label(f_act, text="Treatment:").pack(side="left")
        treats = database.fetch_all("SELECT treatmentID, treatment, treatmentCost FROM treatment")
        self.t_map = {f"{t['treatment']} (${t['treatmentCost']})": t for t in treats}
        self.cb_treat = ttk.Combobox(f_act, values=list(self.t_map.keys()));
        self.cb_treat.pack(side="left", padx=10)

        tk.Button(f_act, text="Complete Visit", bg="green", fg="white", command=self.complete).pack(side="left")
        self.refresh()

    def refresh(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        # CHANGE: Added "AND a.appointmentStatus IN ('Scheduled', 'Completed')"
        # This hides Pending (unverified) and Cancelled appointments from the doctor.
        rows = database.fetch_all("""
            SELECT a.id, a.appointmentTime, a.appointmentStatus, a.doctorNotes, p.patientName 
            FROM appointment a JOIN patient p ON a.patientID=p.patientID 
            WHERE a.doctorID=%s 
            AND a.appointmentStatus IN ('Scheduled', 'Completed')
            ORDER BY a.appointmentDate ASC
        """, (self.did,))

        for r in rows:
            self.tree.insert("", "end", values=(
                r['id'], r['appointmentTime'], r['patientName'], r['appointmentStatus'], r['doctorNotes']
            ))

    def complete(self):
        sel = self.tree.selection()
        if not sel or not self.cb_treat.get(): return messagebox.showerror("Error", "Select Appt & Treatment")

        aid = self.tree.item(sel[0])['values'][0]
        treat = self.t_map[self.cb_treat.get()]

        # 1. Update Appt
        database.execute_query(
            "UPDATE appointment SET appointmentStatus='Completed', doctorNotes=%s, treatmentID=%s WHERE id=%s",
            (self.en_note.get(), treat['treatmentID'], aid))
        # 2. Update Payment
        pid = database.fetch_all("SELECT paymentID FROM appointment WHERE id=%s", (aid,))[0]['paymentID']
        database.execute_query("UPDATE payment SET paymentAmount=%s, paymentStatus='Paid' WHERE paymentID=%s",
                               (treat['treatmentCost'], pid))
        # 3. Free Room
        room = database.fetch_all("SELECT roomNumber FROM appointment WHERE id=%s", (aid,))[0]['roomNumber']
        if room: database.set_room_status(room, 'Available')

        messagebox.showinfo("Success", "Visit Completed");
        self.refresh();
        self.en_note.delete(0, 'end')
import tkinter as tk
from tkinter import ttk, messagebox, Label, Button, Frame, Entry, LabelFrame, Toplevel, filedialog
from PIL import Image, ImageTk
import time
import mysql.connector
from mysql.connector import errorcode
import os
import csv # <--- NEW IMPORT

# --- DatabaseManager Class ---
# Manages all database connections and queries for attendance
class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.db_config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }
        self.conn = None
        self.connect()

    def connect(self):
        """Establishes a persistent connection to the database."""
        try:
            self.conn = mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to database: {err}")
            self.conn = None

    def get_connection(self):
        """Returns the current connection, reconnects if necessary."""
        try:
            if self.conn is None or not self.conn.is_connected():
                self.connect()
            self.conn.ping(reconnect=True, attempts=1, delay=1)
        except mysql.connector.Error as err:
            self.conn = None
            messagebox.showerror("Database Connection Lost", f"Lost connection to database: {err}. Please restart.")
        return self.conn

    def fetch_all_attendance(self):
        """Fetches all attendance records, joined with student info."""
        conn = self.get_connection()
        if conn is None:
            return []
        
        # This query JOINS the new attendance table with the existing face table
        sql = """
            SELECT
                ar.record_id,         -- The unique key for the attendance record
                f.id,                 -- The student's ID
                f.roll,
                f.name,
                f.dep,
                f.course,
                f.div,
                ar.attendance_time,
                ar.attendance_date,
                ar.attendance_status
            FROM attendance_records AS ar
            JOIN face AS f ON ar.student_id = f.id
            ORDER BY ar.attendance_date DESC, ar.attendance_time DESC
        """
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch attendance data: {err}")
            return []

    def update_attendance(self, record_id, new_status):
        """Updates ONLY the attendance status for a specific record."""
        conn = self.get_connection()
        if conn is None:
            return False
        
        sql = "UPDATE attendance_records SET attendance_status = %s WHERE record_id = %s"
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (new_status, record_id))
                conn.commit()
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to update status: {err}")
            return False

    def delete_attendance(self, record_id):
        """Deletes a specific attendance record by its unique record_id."""
        conn = self.get_connection()
        if conn is None:
            return False
        
        sql = "DELETE FROM attendance_records WHERE record_id = %s"
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (record_id,))
                conn.commit()
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to delete record: {err}")
            return False

    def close(self):
        """Closes the database connection if it's open."""
        if self.conn and self.conn.is_connected():
            self.conn.close()


class attendance:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Details")
        self.root.geometry("1300x734+0+0")
        self.root.resizable(0, 0)
        try:
            self.root.wm_iconbitmap("face-icon.ico")
        except tk.TclError:
            print("Icon 'face-icon.ico' not found.")

        # ==================== variables ====================
        self.var_dep = tk.StringVar()
        self.var_course = tk.StringVar()
        self.var_id = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_div = tk.StringVar()
        self.var_roll = tk.StringVar()
        self.var_time = tk.StringVar()
        self.var_date = tk.StringVar()
        self.var_attendance = tk.StringVar()
        
        # This will store the unique PK (record_id) of the selected attendance row
        self.record_id_to_update = None

        # --- Initialize Database Manager ---
        self.db = DatabaseManager(
            host="localhost",
            user="root",
            password="1234",
            database="face_system"
        )

        faceframe = Frame(self.root, bg="#FFFFFF")
        faceframe.place(x=0, y=0, width=1300, height=734)

        # Heading
        heading = Label(faceframe, text="Attendance Window", font=('times now roman', 35, "bold"), bg="#CFE4FA", fg="blue")
        heading.place(x=0, y=0, width=1300, height=60)

        # back button
        b = Button(self.root, text="Back", cursor="hand2", font=('times now roman', 20, "bold"), bg="#EF2A2A", fg="white", command=self.on_close)
        b.place(x=1180, y=12, width=100, height=35)
        
        # --- FIXED CLOCK ---
        # Create the label ONCE
        self.subtitlelabel = Label(self.root, text=" ", font=('times now roman', 12, "bold"), bg="#1060B7", fg="#ffffff")
        self.subtitlelabel.place(x=0, y=60, width=1300, height=30)
        self._update_clock_text() # Start the clock loop

        # Left frame
        Left_frame = LabelFrame(faceframe, text="Attendance Details", font=('times now roman', 15, "bold"), bg="#CFE4FA", fg="blue", bd=2, relief=tk.RIDGE)
        Left_frame.place(x=10, y=100, width=640, height=550)

        class_frame = Frame(Left_frame, bg="#FFFFFF", bd=2, relief=tk.RIDGE)
        class_frame.place(x=3, y=0, width=630, height=500)

        # --- Form Fields ---
        # All fields are now read-only except for the 'Attendance' status
        
        # department
        dep_label = Label(class_frame, text='Department :', font=('roman new time', 13, "bold"), bg="#f1f1f1")
        dep_label.grid(row=0, column=0, padx=5, pady=(25, 5), sticky='w')
        dep_combo = ttk.Combobox(class_frame, textvariable=self.var_dep, font=('roman new time', 12), state="readonly", cursor="hand2")
        dep_combo.grid(row=0, column=1, pady=(25, 5), sticky='w')

        # Course
        Course_label = Label(class_frame, text='Course :', font=('roman new time', 13, "bold"), bg="#f1f1f1")
        Course_label.grid(row=0, column=2, padx=(5, 0), pady=(25, 5), sticky='w')
        Course_combo = ttk.Combobox(class_frame, textvariable=self.var_course, font=('roman new time', 12), state="readonly", cursor="hand2")
        Course_combo.grid(row=0, column=3, padx=(0, 5), pady=(25, 5), sticky='w')

        # Name
        Student_name_label = Label(class_frame, text='Name :', font=('roman new time', 13, "bold"), bg="#f1f1f1")
        Student_name_label.grid(row=1, column=0, padx=5, pady=(25, 5), sticky='w')
        Student_name_entry = ttk.Entry(class_frame, textvariable=self.var_name, font=('roman new time', 12), state="readonly")
        Student_name_entry.grid(row=1, column=1, padx=(0, 5), pady=(25, 5), sticky='w')

        # ID
        StudentId_label = Label(class_frame, text='ID :', font=('roman new time', 13, "bold"), bg="#f1f1f1")
        StudentId_label.grid(row=1, column=2, padx=5, pady=(25, 5), sticky='w')
        StudentId_entry = ttk.Entry(class_frame, textvariable=self.var_id, font=('roman new time', 12), state="readonly")
        StudentId_entry.grid(row=1, column=3, padx=(0, 5), pady=(25, 5), sticky='w')

        # Class Division
        class_div_label = Label(class_frame, text='Division :', font=('roman new time', 13, "bold"), bg="#f1f1f1")
        class_div_label.grid(row=2, column=0, padx=5, pady=(25, 5), sticky='w')
        class_div_entry = ttk.Entry(class_frame, textvariable=self.var_div, font=('roman new time', 12), state="readonly")
        class_div_entry.grid(row=2, column=1, padx=(0, 5), sticky='w')

        # Roll No.
        roll_no_label = Label(class_frame, text='Roll No. :', font=('roman new time', 13, "bold"), bg="#f1f1f1")
        roll_no_label.grid(row=2, column=2, padx=5, pady=(25, 5), sticky='w')
        roll_no_entry = ttk.Entry(class_frame, textvariable=self.var_roll, font=('roman new time', 12), state="readonly")
        roll_no_entry.grid(row=2, column=3, padx=(0, 5), pady=(25, 5), sticky='w')

        # Time
        timeing_label = Label(class_frame, text='Time :', font=('roman new time', 13, "bold"), bg="#ffffff")
        timeing_label.grid(row=3, column=0, padx=5, pady=(25, 5), sticky='w')
        timeing_entry = ttk.Entry(class_frame, textvariable=self.var_time, font=('roman new time', 13), state="readonly")
        timeing_entry.grid(row=3, column=1, padx=(0, 5), pady=(25, 5), sticky='w')

        # Date
        date_label = Label(class_frame, text='Date :', font=('roman new time', 13, "bold"), bg="#ffffff")
        date_label.grid(row=3, column=2, padx=5, pady=(25, 5), sticky='w')
        date_entry = ttk.Entry(class_frame, textvariable=self.var_date, font=('roman new time', 13), state="readonly")
        date_entry.grid(row=3, column=3, padx=(0, 5), pady=(25, 5), sticky='w')

        # attendance
        attendance_label = Label(class_frame, text='Attendance :', font=('roman new time', 13, "bold"), bg="#ffffff")
        attendance_label.grid(row=4, column=0, padx=5, pady=(25, 5), sticky='w')
        # This is the ONLY editable field
        self.attendance_combo = ttk.Combobox(class_frame, textvariable=self.var_attendance, font=('roman new time', 12), state="readonly", cursor="hand2", width=10)
        self.attendance_combo["values"] = ("Status", "Present", "Absent")
        self.attendance_combo.current(0)
        self.attendance_combo.grid(row=4, column=1, padx=(0, 5), pady=(25, 5), sticky='w')

        # button frame
        button_frame = Frame(class_frame, bd=2, bg="#f1f1f1")
        button_frame.place(x=0, y=300, width=620, height=150)

        # --- MODIFIED Buttons (2x2 Grid) ---
        update_button = Button(button_frame, text="Update Status", font=("roman new times", 12, "bold"), bg="#0147bf", fg="#ffffff", width=12, cursor="hand2", command=self.update_data)
        update_button.grid(row=0, column=0, padx=(130, 20), pady=(30, 10)) # Adjusted padding

        delete_button = Button(button_frame, text="Delete Record", font=("roman new times", 12, "bold"), bg="#0147bf", fg="#ffffff", width=12, cursor="hand2", command=self.delete_data)
        delete_button.grid(row=0, column=1, padx=(35, 20), pady=(30, 10)) # Adjusted padding

        clear_button = Button(button_frame, text="Clear", font=("roman new times", 12, "bold"), bg="#0147bf", fg="#ffffff", width=12, cursor="hand2", command=self.clear_data)
        clear_button.grid(row=1, column=0, padx=(130, 20), pady=(10, 25)) # Adjusted padding
        
        # --- NEW Export Button ---
        export_button = Button(button_frame, text="Export to CSV", font=("roman new times", 12, "bold"), bg="#17a2b8", fg="#ffffff", width=12, cursor="hand2", command=self.export_to_csv)
        export_button.grid(row=1, column=1, padx=(35, 20), pady=(10, 25))


        # Right frame
        Right_frame = LabelFrame(faceframe, text="Attendance List", font=('times now roman', 15, "bold"), bg="#CFE4FA", fg="blue", bd=2, relief=tk.RIDGE)
        Right_frame.place(x=655, y=100, width=640, height=550)

        table_frame = Frame(Right_frame, bd=2, relief=tk.RIDGE)
        table_frame.place(x=3, y=0, width=630, height=500)

        scrollx = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scrolly = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)

        # --- MODIFIED: Table Columns ---
        # Added 'record_id' as a hidden first column
        self.attendance_table = ttk.Treeview(table_frame,
            columns=("record_id", "id", "roll", 'name', 'dep', 'course', "div", "time", "date", "attendance"),
            show='headings', yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=tk.BOTTOM, fill=tk.X)
        scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        scrollx.config(command=self.attendance_table.xview)
        scrolly.config(command=self.attendance_table.yview)

        # Headings
        self.attendance_table.heading('record_id', text='Rec ID')
        self.attendance_table.heading('id', text='Student ID')
        self.attendance_table.heading('roll', text='Roll No.')
        self.attendance_table.heading('name', text='Name')
        self.attendance_table.heading('dep', text='Department')
        self.attendance_table.heading('course', text='Course')
        self.attendance_table.heading('div', text='Division')
        self.attendance_table.heading('time', text='Time')
        self.attendance_table.heading('date', text='Date')
        self.attendance_table.heading('attendance', text='Attendance')

        # --- MODIFIED: Column Widths ---
        # Hide the 'record_id' column
        self.attendance_table.column('record_id', width=0, minwidth=0, stretch=tk.NO)
        self.attendance_table.column('id', width=60)
        self.attendance_table.column('roll', width=60)
        self.attendance_table.column('name', width=100)
        self.attendance_table.column('dep', width=80)
        self.attendance_table.column('course', width=50)
        self.attendance_table.column('div', width=40)
        self.attendance_table.column('time', width=65)
        self.attendance_table.column('date', width=75)
        self.attendance_table.column('attendance', width=80)
        
        self.attendance_table.pack(fill=tk.BOTH, expand=1)
        self.attendance_table.bind("<ButtonRelease>", self.get_cursor)
        
        # Close window protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Load data from DB on start
        self.fetch_data()

    # ==================== Function Declarations ====================

    def populate_table(self, data):
        """Clears the table and inserts new data."""
        self.attendance_table.delete(*self.attendance_table.get_children())
        if data:
            for row in data:
                self.attendance_table.insert("", tk.END, values=row)

    def fetch_data(self):
        """Fetches all data from the database and populates the table."""
        data = self.db.fetch_all_attendance()
        self.populate_table(data)

    def get_cursor(self, event=""):
        """Populates the form fields when a table row is clicked."""
        try:
            cursor_focus = self.attendance_table.focus()
            if not cursor_focus:
                return
                
            content = self.attendance_table.item(cursor_focus)
            data = content['values']

            # data[0] is the hidden record_id
            self.record_id_to_update = data[0] 

            # data[1] onwards are the visible columns
            self.var_id.set(data[1])
            self.var_roll.set(data[2])
            self.var_name.set(data[3])
            self.var_dep.set(data[4])
            self.var_course.set(data[5])
            self.var_div.set(data[6])
            self.var_time.set(data[7])
            self.var_date.set(data[8])
            self.var_attendance.set(data[9])
        except (IndexError, tk.TclError):
            pass # Ignore errors from empty table clicks

    # --- NEW: Function to export table data to CSV ---
    def export_to_csv(self):
        """Exports the data currently in the attendance table to a CSV file."""
        try:
            # Get all item IDs from the treeview
            item_ids = self.attendance_table.get_children()
            if not item_ids:
                messagebox.showwarning("No Data", "There is no data in the table to export.", parent=self.root)
                return

            # Ask user for a filename
            filepath = filedialog.asksaveasfilename(
                initialdir=os.getcwd(),
                title="Save CSV",
                filetypes=(("CSV File", "*.csv"), ("All File", "*.*")),
                parent=self.root,
                defaultextension=".csv"
            )
            
            if not filepath: # User cancelled
                return

            # Get visible column IDs (skip the hidden 'record_id')
            visible_cols = self.attendance_table['columns'][1:]
            
            # Get headers for visible columns
            headers = [self.attendance_table.heading(col)['text'] for col in visible_cols]
            
            # Get data rows (skipping the hidden 'record_id' value)
            data_rows = []
            for item in item_ids:
                values = self.attendance_table.item(item)['values']
                data_rows.append(values[1:]) # Append all values except the first one

            # Write to CSV
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(data_rows)
            
            messagebox.showinfo("Success", f"Data exported successfully to {os.path.basename(filepath)}", parent=self.root)

        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred while exporting data: {str(e)}", parent=self.root)


    def update_data(self):
        """Updates the attendance status of the selected record."""
        if self.record_id_to_update is None:
            messagebox.showerror("Error", "Please select a record to update.", parent=self.root)
            return
            
        new_status = self.var_attendance.get()
        if new_status == "Status":
            messagebox.showwarning("Warning", "Please select a valid attendance status.", parent=self.root)
            return

        if self.db.update_attendance(self.record_id_to_update, new_status):
            messagebox.showinfo("Success", "Record updated successfully.", parent=self.root)
            self.fetch_data()
            self.clear_data()
        else:
            messagebox.showerror("Error", "Failed to update record in database.", parent=self.root)

    def delete_data(self):
        """Deletes the selected attendance record."""
        if self.record_id_to_update is None:
            messagebox.showerror("Error", "Please select a record to delete.", parent=self.root)
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this specific record?", parent=self.root)
        if not confirm:
            return

        if self.db.delete_attendance(self.record_id_to_update):
            messagebox.showinfo("Success", "Record deleted successfully.", parent=self.root)
            self.fetch_data()
            self.clear_data()
        else:
            messagebox.showerror("Error", "Failed to delete record from database.", parent=self.root)

    def clear_data(self):
        """Clears the form fields and selection."""
        self.var_dep.set("")
        self.var_course.set("")
        self.var_id.set("")
        self.var_name.set("")
        self.var_div.set("")
        self.var_roll.set("")
        self.var_time.set("")
        self.var_date.set("")
        self.var_attendance.set("Status")
        self.record_id_to_update = None
        self.attendance_table.selection_remove(self.attendance_table.selection())

    def _update_clock_text(self):
        """Updates the clock label text every second."""
        date_time = time.strftime(' %B %d, %Y \t\t\t \t%I:%M:%S %p on %A ')
        self.subtitlelabel.config(text=f"{date_time}")
        self.subtitlelabel.after(1000, self._update_clock_text)

    def on_close(self):
        """Closes the database connection and the application."""
        self.db.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    obj = attendance(root)
    root.mainloop()
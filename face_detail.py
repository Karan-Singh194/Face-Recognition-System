import tkinter as tk
from tkinter import ttk, messagebox, Label, Button, Frame, Entry, LabelFrame, Toplevel
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import time
import mysql.connector
from mysql.connector import errorcode
import os
# We import the PhotoCapture app.
# This assumes the file is named 'capture_image.py' as in your original code.
try:
    from capture_image import PhotoCapture
except ImportError:
    messagebox.showerror("Import Error", "Could not import 'capture_image.py'. Make sure the file is in the same directory.")
    # We'll define a placeholder class so the app can at least start
    class PhotoCapture:
        def __init__(self, root):
            messagebox.showerror("Error", "PhotoCapture module not found.", parent=root)
            root.destroy()

# --- DatabaseManager Class ---
# Manages all database connections and queries
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
            # Ping the server to check if the connection is alive
            self.conn.ping(reconnect=True, attempts=1, delay=1)
        except mysql.connector.Error as err:
            self.conn = None # Connection failed, set to None
            messagebox.showerror("Database Connection Lost", f"Lost connection to database: {err}. Please restart.")
        return self.conn

    def fetch_all(self):
        """Fetches all student records from the 'face' table."""
        conn = self.get_connection()
        if conn is None:
            return []
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM face")
                return cursor.fetchall()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch data: {err}")
            return []

    def add(self, data_tuple):
        """Adds a new student record to the 'face' table."""
        conn = self.get_connection()
        if conn is None:
            return False
        
        # Add the 'No' for photo status as the 14th item
        data_with_photo = data_tuple + ('No',)
        
        sql = """
            INSERT INTO face (dep, course, year, sem, id, name, `div`, roll, gender, dob, email, phone, address, photo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, data_with_photo)
                conn.commit()
            return True
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DUP_ENTRY:
                messagebox.showerror("Error", f"A student with ID {data_tuple[4]} already exists.")
            else:
                messagebox.showerror("Database Error", f"Error due to {err}")
            return False

    def update(self, data_tuple):
        """Updates an existing student record based on ID."""
        conn = self.get_connection()
        if conn is None:
            return False
        
        # Note: We are NOT updating the 'photo' status here.
        # That is handled by the PhotoCapture app.
        sql = """
            UPDATE face SET 
                dep=%s, course=%s, year=%s, sem=%s, 
                name=%s, `div`=%s, roll=%s, gender=%s, dob=%s, 
                email=%s, phone=%s, address=%s 
            WHERE id=%s
        """
        try:
            # We need a tuple of 13 values: 12 for SET, 1 for WHERE.
            # data_tuple has 13 values, with ID at index 4.
            # We create (data[0-3]), (data[5-12]), (data[4])
            
            # --- THIS IS THE CORRECTED LINE ---
            update_tuple = data_tuple[:4] + data_tuple[5:] + (data_tuple[4],)
            
            with conn.cursor() as cursor:
                cursor.execute(sql, update_tuple)
                conn.commit()
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error due to {err}")
            return False

    def delete(self, student_id):
        """Deletes a student record by ID."""
        conn = self.get_connection()
        if conn is None:
            return False
        
        sql = "DELETE FROM face WHERE id=%s"
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (student_id,))
                conn.commit()
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error due to {err}")
            return False

    # --- NEW: Function to update only the photo status ---
    def update_photo_status(self, student_id, status):
        """Updates the 'photo' column for a specific student."""
        conn = self.get_connection()
        if conn is None:
            return False
        
        sql = "UPDATE face SET photo = %s WHERE id = %s"
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (status, student_id))
                conn.commit()
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to update photo status: {err}")
            return False

    def search(self, search_by, search_text):
        """Searches for students by a specific column."""
        conn = self.get_connection()
        if conn is None:
            return []

        # Sanitize 'search_by' to prevent SQL injection on column name
        if search_by == "Roll No.":
            column = "roll"
        elif search_by == "Name":
            column = "name"
        else:
            messagebox.showerror("Search Error", "Invalid search category.")
            return []
        
        # Use placeholders for the search text
        sql = f"SELECT * FROM face WHERE {column} LIKE %s"
        query_param = f"%{search_text}%"
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (query_param,))
                return cursor.fetchall()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to search data: {err}")
            return []

    def close(self):
        """Closes the database connection if it's open."""
        if self.conn and self.conn.is_connected():
            self.conn.close()


# --- Main Application Class ---
class Face:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Detail")
        self.root.geometry("1300x734+0+0")
        self.root.resizable(0, 0)
        # self.root.wm_iconbitmap("face-icon.ico") # Uncomment if you have this icon file

        # Initialize Database Manager
        self.db = DatabaseManager(
            host="localhost",
            user="root",
            password="1234",
            database="face_system"
        )

        # --- Variables ---
        self.var_dep = tk.StringVar()
        self.var_course = tk.StringVar()
        self.var_year = tk.StringVar()
        self.var_sem = tk.StringVar()
        self.var_id = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_div = tk.StringVar()
        self.var_roll = tk.StringVar()
        self.var_gender = tk.StringVar()
        self.var_dob = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_phone = tk.StringVar()
        self.var_address = tk.StringVar()
        # self.var_radio is no longer needed
        
        self.student_photo = None # <--- NEW: To hold the image reference
        
        self.search_by_var = tk.StringVar()
        self.search_text_var = tk.StringVar()

        self._setup_gui()
        self._update_clock() # Start the clock
        
        self.fetch_data() # Initial data load

        # Ensure database connection is closed when window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _setup_gui(self):
        """Sets up the main GUI layout."""
        faceframe = Frame(self.root, bg="#FFFFFF")
        faceframe.place(x=0, y=0, width=1300, height=734)

        # Heading
        heading = Label(faceframe, text="Student Face Detail", font=('times now roman', 35, "bold"), bg="#CFE4FA", fg="blue")
        heading.place(x=0, y=0, width=1300, height=60)

        # back button
        b = Button(self.root, text="Back", cursor="hand2", font=('times now roman', 20, "bold"), bg="#EF2A2A", fg="white", command=self.on_close)
        b.place(x=1180, y=12, width=100, height=35)

        # Clock Label (created once, updated by _update_clock)
        self.subtitlelabel = Label(self.root, text="Loading...", font=('times now roman', 12, "bold"), bg="#1060B7", fg="#ffffff")
        self.subtitlelabel.place(x=0, y=60, width=1300, height=30)

        # Create GUI components
        self._create_left_frame(faceframe)
        self._create_right_frame(faceframe)

    def _create_left_frame(self, parent):
        """Creates the left-side form for student details."""
        Left_frame = LabelFrame(parent, text="Student Details", font=('times now roman', 15, "bold"), bg="#CFE4FA", fg="black", bd=2, relief=tk.RIDGE)
        Left_frame.place(x=10, y=100, width=640, height=600)

        current_course_frame = LabelFrame(Left_frame, text="Current Course Details", font=('times now roman', 13, "bold"), bg="#FFFFFF", fg="blue", bd=2, relief=tk.RIDGE)
        current_course_frame.place(x=3, y=10, width=630, height=150)

        # --- Widgets for current_course_frame ---
        Label(current_course_frame, text='Department :', font=('roman new time', 13, "bold"), bg="#f1f1f1").grid(row=0, column=0, padx=5, sticky='w')
        dep_combo = ttk.Combobox(current_course_frame, textvariable=self.var_dep, font=('roman new time', 12), state="readonly", cursor="hand2")
        dep_combo["values"] = ("Select Department", "Computer", "IT", "CSE")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, sticky='w')

        Label(current_course_frame, text='Course :', font=('roman new time', 13, "bold"), bg="#f1f1f1").grid(row=0, column=2, padx=5, sticky='w')
        Course_combo = ttk.Combobox(current_course_frame, textvariable=self.var_course, font=('roman new time', 12), state="readonly", cursor="hand2")
        Course_combo["values"] = ("Select Course", "AI", "ML", "DBMS")
        Course_combo.current(0)
        Course_combo.grid(row=0, column=3, padx=(0, 5), sticky='w')

        Label(current_course_frame, text='Year :', font=('roman new time', 13, "bold"), bg="#f1f1f1").grid(row=1, column=0, padx=5, sticky='w')
        year_combo = ttk.Combobox(current_course_frame, textvariable=self.var_year, font=('roman new time', 12), state="readonly", cursor="hand2")
        year_combo["values"] = ("Select Year", "2022", "2023", "2024", "2025")
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=(0, 5), pady=10, sticky='w')

        Label(current_course_frame, text='Semester:', font=('roman new time', 13, "bold"), bg="#f1f1f1").grid(row=1, column=2, padx=(0, 5), sticky='w')
        sem_combo = ttk.Combobox(current_course_frame, textvariable=self.var_sem, font=('roman new time', 12), state="readonly", cursor="hand2")
        sem_combo["values"] = ("Select Semester", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th")
        sem_combo.current(0)
        sem_combo.grid(row=1, column=3, padx=(0, 5), pady=10, sticky='w')

        # --- Widgets for class_student_frame ---
        class_student_frame = LabelFrame(Left_frame, text="Class Student information", font=('times now roman', 13, "bold"), bg="#FFFFFF", fg="blue", bd=2, relief=tk.RIDGE)
        class_student_frame.place(x=3, y=170, width=630, height=400)

        Label(class_student_frame, text='Student Name:', font=('roman new time', 13, "bold"), bg="#f1f1f1").grid(row=0, column=0, padx=5, sticky='w')
        ttk.Entry(class_student_frame, textvariable=self.var_name, font=('roman new time', 12), cursor="hand2").grid(row=0, column=1, padx=5, pady=5, sticky='w')

        Label(class_student_frame, text='Student ID:', font=('roman new time', 13, "bold"), bg="#f1f1f1").grid(row=0, column=2, padx=5, sticky='w')
        ttk.Entry(class_student_frame, textvariable=self.var_id, font=('roman new time', 12), cursor="hand2").grid(row=0, column=3, padx=5, pady=5, sticky='w')

        Label(class_student_frame, text='Class Division:', font=('roman new time', 13, "bold"), bg="#f1f1f1").grid(row=1, column=0, padx=5, sticky='w')
        ttk.Entry(class_student_frame, textvariable=self.var_div, font=('roman new time', 12), cursor="hand2").grid(row=1, column=1, padx=5, pady=5, sticky='w')

        Label(class_student_frame, text='Roll No.:', font=('roman new time', 13, "bold"), bg="#f1f1f1").grid(row=1, column=2, padx=5, sticky='w')
        ttk.Entry(class_student_frame, textvariable=self.var_roll, font=('roman new time', 12), cursor="hand2").grid(row=1, column=3, padx=5, pady=5, sticky='w')

        Label(class_student_frame, text='Gender:', font=('roman new time', 13, "bold"), bg="#f1f1f1").grid(row=2, column=0, padx=5, sticky='w')
        gender_combo = ttk.Combobox(class_student_frame, textvariable=self.var_gender, font=('roman new time', 12), state="readonly", cursor="hand2", width=15)
        gender_combo["values"] = ("Select Gender", "Male", "Female", "Other")
        gender_combo.current(0)
        gender_combo.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        Label(class_student_frame, text='DOB', font=("roman new times", 13, "bold"), bg="#f1f1f1").grid(row=2, column=2, padx=5, sticky='w')
        DateEntry(class_student_frame, textvariable=self.var_dob, width=18, font=("roman new times", 12), state="readonly", date_pattern='dd/MM/yyyy').grid(row=2, column=3, padx=5, pady=5, sticky='w')

        Label(class_student_frame, text='Email:', font=('roman new time', 13, "bold"), bg="#f1f1f1").grid(row=3, column=0, padx=5, sticky='w')
        ttk.Entry(class_student_frame, textvariable=self.var_email, font=('roman new time', 12), cursor="hand2").grid(row=3, column=1, padx=5, pady=5, sticky='w')

        Label(class_student_frame, text='Phone:', font=('roman new time', 13, "bold"), bg="#f1f1f1").grid(row=3, column=2, padx=5, sticky='w')
        ttk.Entry(class_student_frame, textvariable=self.var_phone, font=('roman new time', 12), cursor="hand2").grid(row=3, column=3, padx=5, pady=5, sticky='w')

        Label(class_student_frame, text='Address:', font=('roman new time', 13, "bold"), bg="#f1f1f1").grid(row=4, column=0, padx=5, sticky='w')
        ttk.Entry(class_student_frame, textvariable=self.var_address, font=('roman new time', 12), cursor="hand2", width=30).grid(row=4, column=1, columnspan=3, padx=5, pady=5, sticky='w')

        # Radio buttons are removed as per new workflow

        # --- Button Frames ---
        button_frame = Frame(class_student_frame, bd=2, bg="#f1f1f1")
        button_frame.place(x=0, y=260, width=620, height=50)

        Button(button_frame, text="Save", font=("roman new times", 14), bg="#0147bf", fg="#fefefe", width=8, cursor="hand2", command=self.add_data).grid(row=0, column=0, padx=20)
        Button(button_frame, text="Update", font=("roman new times", 14), bg="#0147bf", fg="#fefefe", width=8, cursor="hand2", command=self.update_data).grid(row=0, column=1, padx=20)
        Button(button_frame, text="Delete", font=("roman new times", 14), bg="#0147bf", fg="#ffffff", width=8, cursor="hand2", command=self.delete_data).grid(row=0, column=2, padx=20)
        Button(button_frame, text="Clear", font=("roman new times", 14), bg="#0147bf", fg="#cfe4fa", width=8, cursor="hand2", command=self.reset_data).grid(row=0, column=3, padx=20)

        button_frame1 = Frame(class_student_frame, bd=2, bg="#ffffff")
        button_frame1.place(x=0, y=310, width=620, height=65)

        Button(button_frame1, text="Take Face Sample", font=("roman new times", 12, "bold"), bg="#0147bf", fg="#cfe4fa", command=self.open_photo_capture, width=30, cursor="hand2").grid(row=0, column=0, padx=5, pady=15)
        Button(button_frame1, text="Show Face Sample", font=("roman new times", 12, "bold"), bg="#0147bf", fg="#cfe4fa", command=self.open_img_folder, width=30, cursor="hand2").grid(row=0, column=2, padx=5, pady=15)

    def _create_right_frame(self, parent):
        """Creates the right-side table and search system."""
        Right_frame = LabelFrame(parent, text="Student List", font=('times now roman', 15, "bold"), bg="#CFE4FA", fg="black", bd=2, relief=tk.RIDGE)
        Right_frame.place(x=655, y=100, width=640, height=600)

        # Searching frame
        search_frame = LabelFrame(Right_frame, text="Search System", font=('times now roman', 13, "bold"), bg="#FFFFFF", fg="blue", bd=2, relief=tk.RIDGE)
        search_frame.place(x=3, y=10, width=630, height=85)

        Label(search_frame, text='Search :', font=('roman new time', 13, "bold"), bg="#ffffff").grid(row=0, column=0, padx=5, sticky='w')
        search_combo = ttk.Combobox(search_frame, textvariable=self.search_by_var, font=('roman new time', 12), state="readonly", cursor="hand2", width=10)
        search_combo["values"] = ("Search by", "Roll No.", "Name")
        search_combo.current(0)
        search_combo.grid(row=0, column=2, padx=(5, 15), pady=10, sticky='w')

        Entry(search_frame, textvariable=self.search_text_var, font=('roman new time', 13), bg='lightyellow', width=15).grid(row=0, column=3, pady=10)

        Button(search_frame, text="Search", font=("roman new times", 12, "bold"), bg="#0147bf", fg="#ffffff", width=8, cursor="hand2", command=self.search_data).grid(row=0, column=4, padx=15)
        Button(search_frame, text="Show All", font=("roman new times", 12, "bold"), bg="#0147bf", fg="#ffffff", width=8, cursor="hand2", command=self.fetch_data).grid(row=0, column=5)

        # table frame
        table_frame = Frame(Right_frame, bd=2, relief=tk.RIDGE)
        table_frame.place(x=3, y=100, width=630, height=270) # <--- Height set to 270

        scrollx = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scrolly = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)

        self.student_table = ttk.Treeview(table_frame,
            columns=('dep', 'course', 'year', "sem", "id", 'name', "div", "roll",
                     "gender", "dob", "email", "phone", "address", "photo"),
            yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=tk.BOTTOM, fill=tk.X)
        scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        scrollx.config(command=self.student_table.xview)
        scrolly.config(command=self.student_table.yview)

        self.student_table.heading('dep', text='Department')
        self.student_table.heading('course', text='Course')
        self.student_table.heading('year', text='Year')
        self.student_table.heading('sem', text='Semester')
        self.student_table.heading('id', text='Student ID')
        self.student_table.heading('name', text='Name')
        self.student_table.heading('div', text='Division')
        self.student_table.heading('roll', text='Roll No.')
        self.student_table.heading('gender', text='Gender')
        self.student_table.heading('dob', text='DOB')
        self.student_table.heading('email', text='Email')
        self.student_table.heading('phone', text='Phone')
        self.student_table.heading('address', text='Address')
        self.student_table.heading('photo', text='Photo Sample')
        self.student_table['show'] = 'headings'

        self.student_table.column('dep', width=80)
        self.student_table.column('course', width=50)
        self.student_table.column('year', width=50)
        self.student_table.column('sem', width=30)
        self.student_table.column('id', width=80)
        self.student_table.column('name', width=100)
        self.student_table.column('div', width=60)
        self.student_table.column('roll', width=80)
        self.student_table.column('gender', width=60)
        self.student_table.column('dob', width=80)
        self.student_table.column('email', width=100)
        self.student_table.column('phone', width=80)
        self.student_table.column('address', width=150)
        self.student_table.column('photo', width=80)

        self.student_table.pack(fill=tk.BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)
        
        # --- MODIFIED: Photo Preview Frame Layout ---
        photo_preview_frame = LabelFrame(Right_frame, text="Student Photo Preview", font=('times now roman', 13, "bold"), bg="#FFFFFF", fg="blue", bd=2, relief=tk.RIDGE)
        photo_preview_frame.place(x=3, y=375, width=630, height=215) # Placed below the table

        # --- Delete Photo Button ---
        # We pack this FIRST, so it reserves its space on the right
        self.delete_photo_button = Button(
            photo_preview_frame,
            text="Delete\nThis Photo",
            font=("roman new times", 14, "bold"),
            bg="#ff0019", # Red
            fg="white",
            cursor="hand2",
            command=self.delete_photo,
            state=tk.DISABLED,
            width=15 # Give it a fixed width
        )
        self.delete_photo_button.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5) # Pack to the RIGHT

        # --- This label will hold the photo ---
        # We pack this SECOND, so it fills the remaining space
        self.photo_preview_label = Label(photo_preview_frame, bg="white", text="No Photo Selected", font=('times now roman', 12))
        self.photo_preview_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5) # Pack to the LEFT


    # --- Clock Function ---
    def _update_clock(self):
        """Updates the clock label every second."""
        date_time = time.strftime(' %B %d, %Y \t\t\t \t%I:%M:%S %p on %A ')
        self.subtitlelabel.config(text=date_time)
        self.subtitlelabel.after(1000, self._update_clock)
        
    # --- Data Functions ---
    def get_data_tuple(self):
        """Returns a tuple of all data from the form variables."""
        return (
            self.var_dep.get(),
            self.var_course.get(),
            self.var_year.get(),
            self.var_sem.get(),
            self.var_id.get(),
            self.var_name.get(),
            self.var_div.get(),
            self.var_roll.get(),
            self.var_gender.get(),
            self.var_dob.get(),
            self.var_email.get(),
            self.var_phone.get(),
            self.var_address.get()
        )

    def add_data(self):
        """Adds data from the form to the database."""
        if self.var_dep.get() == "Select Department" or self.var_name.get() == "" or self.var_id.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return
            
        data_tuple = self.get_data_tuple()
        if self.db.add(data_tuple):
            messagebox.showinfo("Success", "Data added successfully", parent=self.root)
            self.fetch_data()
            self.reset_data()

    def update_data(self):
        """Updates an existing student record."""
        if self.var_id.get() == "":
            messagebox.showerror("Error", "Student ID is required to update.", parent=self.root)
            return

        if messagebox.askyesno("Update", "Do you want to update this data?", parent=self.root):
            data_tuple = self.get_data_tuple()
            if self.db.update(data_tuple):
                messagebox.showinfo("Success", "Data updated successfully", parent=self.root)
                self.fetch_data()
                self.reset_data()

    def delete_data(self):
        """Deletes a student record from the database."""
        if self.var_id.get() == "":
            messagebox.showerror("Error", "Student ID is required", parent=self.root)
            return

        if messagebox.askyesno("Delete", "Do you want to delete this data?", parent=self.root):
            if self.db.delete(self.var_id.get()):
                messagebox.showinfo("Success", "Data deleted successfully", parent=self.root)
                self.fetch_data()
                self.reset_data()

    def reset_data(self):
        """Clears all form fields."""
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Year")
        self.var_sem.set("Select Semester")
        self.var_id.set("")
        self.var_name.set("")
        self.var_div.set("")
        self.var_roll.set("")
        self.var_gender.set("Select Gender")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.student_table.selection_remove(self.student_table.selection())
        
        # --- NEW: Clear photo preview on reset ---
        self.photo_preview_label.config(image=None, text="No Photo Selected")
        self.student_photo = None
        self.delete_photo_button.config(state=tk.DISABLED) # <--- NEW: Disable button on reset

    def fetch_data(self):
        """Fetches all data from the database and populates the table."""
        data = self.db.fetch_all()
        self.populate_table(data)
        
    def search_data(self):
        """Searches the database and populates the table with results."""
        search_by = self.search_by_var.get()
        search_text = self.search_text_var.get()
        
        if search_by == "Search by":
            messagebox.showerror("Error", "Please select a search category.", parent=self.root)
            return
        if search_text == "":
            messagebox.showerror("Error", "Please enter text to search.", parent=self.root)
            return
            
        data = self.db.search(search_by, search_text)
        if data:
            self.populate_table(data)
        else:
            messagebox.showinfo("No Results", "No records found matching your criteria.", parent=self.root)
            self.populate_table([]) # Clear table

    def populate_table(self, data):
        """Clears the table and inserts new data."""
        self.student_table.delete(*self.student_table.get_children())
        if data:
            for row in data:
                self.student_table.insert("", tk.END, values=row)

    def get_cursor(self, event=""):
        """Populates the form fields when a table row is clicked."""
        try:
            cursor_focus = self.student_table.focus()
            if not cursor_focus:
                return
            content = self.student_table.item(cursor_focus)
            data = content['values']

            self.var_dep.set(data[0])
            self.var_course.set(data[1])
            self.var_year.set(data[2])
            self.var_sem.set(data[3])
            self.var_id.set(data[4])
            self.var_name.set(data[5])
            self.var_div.set(data[6])
            self.var_roll.set(data[7])
            self.var_gender.set(data[8])
            self.var_dob.set(data[9])
            self.var_email.set(data[10])
            self.var_phone.set(data[11])
            self.var_address.set(data[12])
            # We don't set var_radio anymore
            
            # --- NEW: Load and display the student's photo ---
            self.load_student_photo(student_id=data[4], student_name=data[5])
            
        except (IndexError, tk.TclError):
            # This can happen if the table is empty or being rebound
            pass

    # --- MODIFIED: Function to load photo into preview ---
    def load_student_photo(self, student_id, student_name):
        """Loads and displays the photo for the given student."""
        try:
            # Format name (e.g., "Karan Singh" -> "Karan_Singh")
            formatted_name = student_name.replace(" ", "_")
            filename = f"{student_id}_{formatted_name}.jpg"
            filepath = os.path.join("student_images", filename)

            if os.path.exists(filepath):
                # Open, resize, and display the image
                img = Image.open(filepath)
                
                # Resize to fit the preview label, keeping aspect ratio
                # The preview box is roughly 470x205 (630 - 150_button - padding)
                preview_size = (470, 205)
                img.thumbnail(preview_size, Image.Resampling.LANCZOS)
                
                self.student_photo = ImageTk.PhotoImage(img) # Store reference
                self.photo_preview_label.config(image=self.student_photo, text="")
                self.delete_photo_button.config(state=tk.NORMAL) # <--- NEW: Enable button
            else:
                # If file doesn't exist
                self.photo_preview_label.config(image=None, text="No Photo Available")
                self.student_photo = None
                self.delete_photo_button.config(state=tk.DISABLED) # <--- NEW: Disable button
        except Exception as e:
            # In case of file corruption or other errors
            self.photo_preview_label.config(image=None, text="Error loading photo")
            self.student_photo = None
            self.delete_photo_button.config(state=tk.DISABLED) # <--- NEW: Disable button
            print(f"Error loading photo: {e}")


    # --- Button Functions ---
    def open_photo_capture(self):
        """Opens the photo capture window and waits for it to close."""
        self.new_window = Toplevel(self.root)
        self.app = PhotoCapture(self.new_window)
        
        # This makes the main window wait until the new_window is closed
        self.root.wait_window(self.new_window)
        
        # After the window is closed, refresh the data
        self.fetch_data()

    def open_img_folder(self):
        """Opens the 'student_images' folder in the file explorer."""
        try:
            os.startfile("student_images")
        except FileNotFoundError:
            messagebox.showerror("Error", "The 'student_images' directory does not exist.")
            
    # --- NEW: Function to delete a student's photo ---
    def delete_photo(self):
        """Deletes the selected student's photo file and updates the DB."""
        student_id = self.var_id.get()
        student_name = self.var_name.get()
        
        if not student_id:
            messagebox.showwarning("Warning", "No student selected.", parent=self.root)
            return

        # Confirmation
        if not messagebox.askyesno("Delete Photo", f"Are you sure you want to delete the photo for {student_name} (ID: {student_id})?", parent=self.root):
            return
            
        try:
            # 1. Construct file path
            formatted_name = student_name.replace(" ", "_")
            filename = f"{student_id}_{formatted_name}.jpg"
            filepath = os.path.join("student_images", filename)
            
            # 2. Delete the file
            if os.path.exists(filepath):
                os.remove(filepath)
            else:
                messagebox.showwarning("Warning", "Photo file not found, but proceeding to update database.", parent=self.root)

            # 3. Update the database
            if self.db.update_photo_status(student_id, 'No'):
                messagebox.showinfo("Success", "Photo deleted and database updated.", parent=self.root)
            else:
                messagebox.showerror("Error", "File deleted, but failed to update database.", parent=self.root)

            # 4. Refresh the UI
            self.fetch_data()
            self.reset_data() # This will clear the form, clear the preview, and disable the button

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while deleting the photo: {e}", parent=self.root)

            
    def on_close(self):
        """Handles window close event."""
        self.db.close()
        self.root.destroy()


# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    obj = Face(root)
    root.mainloop()
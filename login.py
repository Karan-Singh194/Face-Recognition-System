import tkinter as tk
from tkinter import messagebox, Button, Frame, Label, Entry, Toplevel, END
from PIL import Image, ImageTk
import mysql.connector
import time
import os # <--- Added for file path checking

# --- Import other app modules ---
# We import the main dashboard and the face recognition app
try:
    import main_dashboard # <--- MODIFIED: This is your 'Face_recognition_System' file
    from fe import FaceRecognition
except ImportError as e:
    messagebox.showerror("Import Error", f"Failed to import a required module: {e}")

class Login:
    def __init__(self, root: tk.Tk):
        # Create login window
        self.root = root
        self.root.title("Login")
        self.root.geometry("1000x634+0+0")
        self.root.resizable(0, 0)
        
        # --- FIXED: Added try...except for icon ---
        try:
            self.root.wm_iconbitmap("face-icon.ico")
        except tk.TclError:
            print("Icon 'face-icon.ico' not found.")

        # --- FIXED: Added path check for background ---
        bg_image_path = r"photos\bg2.png"
        if os.path.exists(bg_image_path):
            bg_icon = Image.open(bg_image_path)
            self.photoimg4 = ImageTk.PhotoImage(bg_icon)
            self.bg_icon_label = Label(self.root, image=self.photoimg4)
            self.bg_icon_label.pack()
        else:
            # Fallback if image is missing
            self.bg_icon_label = Label(self.root, bg="#f0f0f0")
            self.bg_icon_label.pack(fill="both", expand=True)
            print(f"Warning: Could not find image: {bg_image_path}")

        # --- Date/Time label (REMOVED) ---
        # self.datetime_label = tk.Label(
        #     self.bg_icon_label, 
        #     text="",
        #     font=('times new roman', 12, "bold"),
        #     bg="#1060B7", 
        #     fg="#ffffff"
        # )
        # self.datetime_label.place(x=0, y=0, width=900, height=30)

        # Exit button
        _exit = tk.Button(
            self.bg_icon_label, 
            text="Exit",
            font=('times new roman', 15, "bold"),
            bg="#FF1241", 
            fg="#ffffff",
            relief="raised",
            cursor="hand2",
            command=self.i_exit
        )
        _exit.place(x=904, y=0, width=90, height=30)

        # Login Frame
        login_frame = Frame(self.root)
        login_frame.place(x=65, y=197, height=215, width=280)

        # --- FIXED: Added path check for login frame background ---
        login_bg_path = r"photos\bg2l.png"
        if os.path.exists(login_bg_path):
            bg_iconl = Image.open(login_bg_path)
            self.bg_iconl = ImageTk.PhotoImage(bg_iconl)
            bg_icon_label1 = Label(login_frame, image=self.bg_iconl)
            bg_icon_label1.place(x=0, y=0, height=215, width=280)
        else:
            print(f"Warning: Could not find image: {login_bg_path}")
            # Fallback in case image is missing
            bg_icon_label1 = Label(login_frame, bg="#03051B") # Dark background
            bg_icon_label1.place(x=0, y=0, height=215, width=280)


        # Header
        heading_label = Label(login_frame, text="Login Board", font=("Segoe UI", 12, "bold"), 
                                bg="#009DFF", fg="white", pady=5)
        heading_label.grid(row=0, column=0, columnspan=3, sticky='we')

        # Username Field
        empid_label = Label(login_frame, text="User ID :", bg="#03051B", font=('Segoe UI', 11, "bold"), fg="white")
        empid_label.grid(row=1, column=1, padx=(20, 5), pady=15, sticky='w')

        self.entry_username = Entry(login_frame, font=("Segoe UI", 10), width=20, relief="solid", bd=1)
        self.entry_username.grid(row=1, column=2, padx=(5, 30), pady=10, sticky='w')

        # Password Field
        password_label = Label(login_frame, text="Password :", bg="#03051B", font=('Segoe UI', 11, "bold"), fg="white")
        password_label.grid(row=2, column=1, padx=(20, 5), pady=15, sticky='w')

        self.entry_password = Entry(login_frame, font=("Segoe UI", 10), width=20, relief="solid", bd=1, show="*")
        self.entry_password.grid(row=2, column=2, padx=(5, 30), pady=10, sticky='w')

        # Buttons
        login_button = Button(login_frame, text="Login", font=("Segoe UI", 10, "bold"), 
                                bg="#009DFF", fg="white", width=8, relief="raised", cursor="hand2", command=self.login)
        login_button.grid(row=3, column=1, padx=(40, 0), pady=10, sticky='e')

        clear_button = Button(login_frame, text="Clear", font=("Segoe UI", 10, "bold"), 
                                bg="#009DFF", fg="white", width=8, relief="raised", cursor="hand2", command=self.clear_fields)
        clear_button.grid(row=3, column=2, padx=(20, 5), pady=10, sticky='w')

        L1_button = Button(self.bg_icon_label, text="Mark Your Attendance", font=('times now roman', 13, "bold",), bg="#009DFF", fg="white",
                            relief="raised", cursor="hand2", command=self.face_call)
        L1_button.place(x=520, y=600, width=220, height=26)

        # Hover effects
        login_button.bind("<Enter>", lambda e: self.on_hover(login_button, "#010c48"))
        login_button.bind("<Leave>", lambda e: self.on_hover(login_button, "#009DFF"))
        clear_button.bind("<Enter>", lambda e: self.on_hover(clear_button, "#010c48"))
        clear_button.bind("<Leave>", lambda e: self.on_hover(clear_button, "#009DFF"))
        L1_button.bind("<Enter>", lambda e: self.on_hover(L1_button, "#010c48"))
        L1_button.bind("<Leave>", lambda e: self.on_hover(L1_button, "#009DFF"))
        _exit.bind("<Enter>", lambda e: self.on_hover(_exit, "#55FF00"))
        _exit.bind("<Leave>", lambda e: self.on_hover(_exit, "#FF1241"))

        # --- REMOVED CALL TO _update_clock() ---
        # self._update_clock()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Database connection
        cursor, connection = self.connect_database()
        if not cursor or not connection:
            return

        try:
            # --- FIXED: Removed the "USE face_system" query ---
            query = "SELECT name FROM admin WHERE id =%s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Login query failed: {e}")
            result = None
        finally:
            cursor.close()
            connection.close()

        if result:
            name = result[0]
            messagebox.showinfo("Login Successful", f"Welcome, {name}!")
            self.root.destroy()  # close login window

            # --- MODIFIED: Imports and calls the main dashboard file ---
            try:
                main_dashboard.run_main()
            except NameError:
                messagebox.showerror("Error", "Could not launch main_dashboard. File not found or contains errors.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while opening the dashboard: {e}")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


    def clear_fields(self):
        self.entry_username.delete(0, END)
        self.entry_password.delete(0, END)

    def on_hover(self, button, color):
        button.config(bg=color)

    def connect_database(self):
        try:
            # --- FIXED: Connects directly to the database ---
            connection = mysql.connector.connect(
                host="localhost", 
                user="root", 
                password="1234",
                database="face_system" # <--- Added this
            )
            cursor = connection.cursor()
        # --- FIXED: Catches specific database errors ---
        except mysql.connector.Error as e:
            messagebox.showerror('Error', f'Database connectivity issue: {e}')
            return None, None

        return cursor, connection
    
    # --- REMOVED _update_clock FUNCTION ---
    # def _update_clock(self):
    #     """Update the date/time display."""
    #     date_time = time.strftime(' %B %d, %Y \t\t\t \t%I:%M:%S %p on %A ')
    #     self.datetime_label.config(text=date_time)
    #     self.datetime_label.after(1000, self._update_clock)

    def i_exit(self):
        # --- FIXED: Uses a local variable to avoid overwriting the function ---
        confirm_exit = messagebox.askyesno("Face Recognition", "Are you sure you want to exit?", parent=self.root)
        if confirm_exit:
            self.root.destroy()
        else:
            return
            
    def face_call(self):
        try:
            window = Toplevel(self.root)
            obj = FaceRecognition(window)
            # --- FIXED: Removed the .mainloop() call ---
        except NameError:
             messagebox.showerror("Error", "Could not launch FaceRecognition. File 'fe.py' not found or contains errors.", parent=self.root)
        except Exception as e:
             messagebox.showerror("Error", f"An error occurred while opening Face Recognition: {e}", parent=self.root)


if __name__ == "__main__":
    root = tk.Tk()
    obj = Login(root)
    root.mainloop()
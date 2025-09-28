from tkinter import *
import tkinter 
from tkinter import messagebox
import subprocess
import sys 
from PIL import Image, ImageTk
import mysql.connector
import pymysql
import time
import datetime
import tkinter as tk
from face_recognition1 import Face_Recognition

class Login:
    def __init__(self,root:tk.Tk):
        # Create login window
        self.root = root
        self.root.title("Login")
        self.root.geometry("1000x634+0+0")
        self.root.resizable(0,0)
        self.root.wm_iconbitmap("face-icon.ico")


        # Background Image
        bg_icon=Image.open(r"photos\bg2.png")
        # bg_icon=bg_icon.resize((120,120), Image.Resampling.LANCZOS)
        self.photoimg4=ImageTk.PhotoImage(bg_icon)

        self.bg_icon_label = Label(self.root, image=self.photoimg4)
        self.bg_icon_label.pack()
        # bg_icon_label.place(x=475, y=25,height=581, width=775)


        # Date/Time label
        self.datetime_label = tk.Label(
            self.bg_icon_label, 
            text="",
            font=('times new roman', 12, "bold"),
            bg="#1060B7", 
            fg="#ffffff"
        )
        self.datetime_label.place(x=0, y=0, width=900, height=30)

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


        bg_iconl=Image.open(r"photos\bg2l.png")
        self.bg_iconl=ImageTk.PhotoImage(bg_iconl)
        bg_icon_label1 = Label(login_frame, image=self.bg_iconl)
        bg_icon_label1.place(x=0, y=0, height=215, width=280)

            # Header
        heading_label = Label(login_frame, text="Login Board", font=("Segoe UI", 12, "bold"), 
                                bg="#009DFF", fg="white", pady=5)
        heading_label.grid(row=0,column=0, columnspan=3, sticky='we')



            # Username Field
        empid_label = Label(login_frame, text="User ID :",bg="#03051B", font=('Segoe UI', 11,"bold"),fg="white")
        empid_label.grid(row=1, column=1, padx=(20,5), pady=15, sticky='w')

        self.entry_username = Entry(login_frame, font=("Segoe UI", 10), width=20, relief="solid", bd=1)
        self.entry_username.grid(row=1, column=2, padx=(5,30), pady=10,sticky='w')

            # Password Field
        password_label = Label(login_frame, text="Password :", bg="#03051B", font=('Segoe UI', 11,"bold"), fg="white")
        password_label.grid(row=2, column=1, padx=(20,5), pady=15, sticky='w')

        self.entry_password = Entry(login_frame, font=("Segoe UI", 10), width=20, relief="solid", bd=1, show="*")
        self.entry_password.grid(row=2, column=2, padx=(5,30), pady=10,sticky='w')

        # Buttons
        login_button = Button(login_frame, text="Login", font=("Segoe UI", 10, "bold"), 
                                bg="#009DFF", fg="white", width=8, relief="raised", cursor="hand2", command=self.login)
        login_button.grid(row=3, column=1, padx=(40,0), pady=10,sticky='e')

        clear_button = Button(login_frame, text="Clear", font=("Segoe UI", 10, "bold"), 
                                bg="#009DFF", fg="white", width=8, relief="raised", cursor="hand2", command=self.clear_fields)
        clear_button.grid(row=3, column=2, padx=(20,5), pady=10,sticky='w')

        L1_button = Button(self.bg_icon_label,text="Mark Your Attendance",font=('times now roman', 13,"bold",),bg="#009DFF", fg="white",
                        relief="raised", cursor="hand2", command=self.face_call)
        L1_button.place(x=520,y=600,width=220,height=26)


        login_button.bind("<Enter>", lambda e: self.on_hover(login_button, "#010c48"))
        login_button.bind("<Leave>", lambda e: self.on_hover(login_button, "#009DFF"))

        clear_button.bind("<Enter>", lambda e: self.on_hover(clear_button, "#010c48"))
        clear_button.bind("<Leave>", lambda e: self.on_hover(clear_button, "#009DFF"))
        
        L1_button.bind("<Enter>", lambda e: self.on_hover(L1_button, "#010c48"))
        L1_button.bind("<Leave>", lambda e: self.on_hover(L1_button, "#009DFF"))

        _exit.bind("<Enter>", lambda e: self.on_hover(_exit, "#55FF00"))
        _exit.bind("<Leave>", lambda e: self.on_hover(_exit, "#FF1241"))

        

        self._update_clock()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Database connection
        cursor, connection = self.connect_database()
        if not cursor or not connection:
            return

        cursor.execute("USE face_system")
        query = "SELECT name FROM admin WHERE id =%s AND password = %s"
        cursor.execute(query, (username,password))
        result = cursor.fetchone()

        connection.close()

        if result:
            name = result[0]
            messagebox.showinfo("Login Successful", f"Welcome, {name}!")
            self.root.destroy()   # close login window

            import main
            main.run_main()
                
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


    def clear_fields(self):
        self.entry_username.delete(0, END)
        self.entry_password.delete(0, END)

    def on_hover(self,button, color):
        button.config(bg=color)

    def connect_database(self):
        try:
            connection=mysql.connector.connect(host="localhost", user="root", password="1234")
            cursor = connection.cursor()
        except:
            messagebox.showerror('Error', 'Database connectivity issue , open mysql command line client')
            return None, None

        return cursor,connection
    
    def _update_clock(self):
        """Update the date/time display."""
        date_time = time.strftime(' %B %d, %Y \t\t\t  %I:%M:%S %p on %A ')
        self.datetime_label.config(text=date_time)
        self.datetime_label.after(1000, self._update_clock)

    def i_exit(self):
        self.i_exit=tkinter.messagebox.askyesno("Face Recongnition", "Are you sure exit this Window",parent=self.root)
        if self.i_exit >0:
            self.root.destroy()
        else:
            return
        
    def face_call(self):
        window = Toplevel()
        obj=Face_Recognition(window)
        window.mainloop()


if __name__ == "__main__":
    root=Tk()
    obj=Login(root)
    root.mainloop()
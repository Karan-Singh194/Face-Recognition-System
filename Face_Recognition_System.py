from tkinter import *
from tkinter import messagebox
import subprocess
import sys 
from PIL import Image, ImageTk
import mysql.connector
import pymysql
# from database import connect_database





class Login:
    def __init__(self,root):

            # Create login window
        self.root = root
        self.root.title("Login")
        self.root.geometry("1000x634+0+0")
        self.root.resizable(0,0)
        self.root.wm_iconbitmap("face.ico")

            # # Background Image
        bg_icon=Image.open(r"photos\bg2.png")
        # bg_icon=bg_icon.resize((120,120), Image.Resampling.LANCZOS)
        self.photoimg4=ImageTk.PhotoImage(bg_icon)

        bg_icon_label = Label(self.root, image=self.photoimg4)
        bg_icon_label.pack()
        # bg_icon_label.place(x=475, y=25,height=581, width=775)


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
        empid_label = Label(login_frame, text="User ID :",bg="#161E2A", font=('Segoe UI', 11,"bold"),fg="white")
        empid_label.grid(row=1, column=1, padx=(20,5), pady=15, sticky='w')

        self.entry_username = Entry(login_frame, font=("Segoe UI", 10), width=20, relief="solid", bd=1)
        self.entry_username.grid(row=1, column=2, padx=(5,30), pady=10,sticky='w')

            # Password Field
        password_label = Label(login_frame, text="Password :", bg="#0B1320", font=('Segoe UI', 11,"bold"), fg="white")
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

        login_button.bind("<Enter>", lambda e: self.on_hover(login_button, "#010c48"))
        login_button.bind("<Leave>", lambda e: self.on_hover(login_button, "#009DFF"))

        clear_button.bind("<Enter>", lambda e: self.on_hover(clear_button, "#010c48"))
        clear_button.bind("<Leave>", lambda e: self.on_hover(clear_button, "#009DFF"))


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


if __name__ == "__main__":
    root=Tk()
    obj=Login(root)
    root.mainloop()
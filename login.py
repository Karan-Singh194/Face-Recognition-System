from tkinter import *
from tkinter import messagebox
import subprocess
import sys 
from PIL import Image, ImageTk
from database import connect_database



def login():
    username = entry_username.get()

    # Database connection
    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    cursor.execute("USE face_system")
    query = "SELECT name FROM face WHERE id =%s"
    cursor.execute(query,(str(username)))
    result = cursor.fetchone()

    connection.close()

    if result:
        user_type = result[0]
        
        if user_type == "karan":
            subprocess.Popen([sys.executable, "main.py"])
            window.destroy()
            
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")



def clear_fields():
    entry_username.delete(0, END)
    entry_password.delete(0, END)

def on_hover(button, color):
    button.config(bg=color)

# Create login window
window = Tk()
window.title("Login")
window.geometry("1000x634+0+0")
window.resizable(0,0)

# # Background Image
bg_icon=Image.open(r"photos\bg2.png")
# bg_icon=bg_icon.resize((120,120), Image.Resampling.LANCZOS)
photoimg4=ImageTk.PhotoImage(bg_icon)

bg_icon_label = Label(window, image=photoimg4)
bg_icon_label.pack()
# bg_icon_label.place(x=475, y=25,height=581, width=775)


# Login Frame
login_frame = Frame(window)
login_frame.place(x=65, y=197, height=215, width=280)


bg_iconl=Image.open(r"photos\bg2l.png")
bg_iconl=ImageTk.PhotoImage(bg_iconl)
bg_icon_label1 = Label(login_frame, image=bg_iconl)
bg_icon_label1.place(x=0, y=0, height=215, width=280)

# Header
heading_label = Label(login_frame, text="Login Board", font=("Segoe UI", 12, "bold"), 
                      bg="#009DFF", fg="white", pady=5)
heading_label.grid(row=0,column=0, columnspan=3, sticky='we')



# Username Field
empid_label = Label(login_frame, text="User ID :",bg="#161E2A", font=('Segoe UI', 11,"bold"),fg="white")
empid_label.grid(row=1, column=1, padx=(20,5), pady=15, sticky='w')

entry_username = Entry(login_frame, font=("Segoe UI", 10), width=20, relief="solid", bd=1)
entry_username.grid(row=1, column=2, padx=(5,30), pady=10,sticky='w')

# Password Field
password_label = Label(login_frame, text="Password :", bg="#0B1320", font=('Segoe UI', 11,"bold"), fg="white")
password_label.grid(row=2, column=1, padx=(20,5), pady=15, sticky='w')

entry_password = Entry(login_frame, font=("Segoe UI", 10), width=20, relief="solid", bd=1, show="*")
entry_password.grid(row=2, column=2, padx=(5,30), pady=10,sticky='w')

# Buttons
login_button = Button(login_frame, text="Login", font=("Segoe UI", 10, "bold"), 
                      bg="#009DFF", fg="white", width=8, relief="raised", cursor="hand2", command=login)
login_button.grid(row=3, column=1, padx=(40,0), pady=10,sticky='e')

clear_button = Button(login_frame, text="Clear", font=("Segoe UI", 10, "bold"), 
                      bg="#009DFF", fg="white", width=8, relief="raised", cursor="hand2", command=clear_fields)
clear_button.grid(row=3, column=2, padx=(20,5), pady=10,sticky='w')

login_button.bind("<Enter>", lambda e: on_hover(login_button, "#010c48"))
login_button.bind("<Leave>", lambda e: on_hover(login_button, "#009DFF"))

clear_button.bind("<Enter>", lambda e: on_hover(clear_button, "#010c48"))
clear_button.bind("<Leave>", lambda e: on_hover(clear_button, "#009DFF"))


window.mainloop()

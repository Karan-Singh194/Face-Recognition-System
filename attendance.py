from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import subprocess
import time
from tkinter import messagebox
import mysql.connector
import cv2
import os


class attendance:
    def __init__(self,root):
        self.root=root
        self.root.title("Face detail")
        self.root.geometry("1300x734+0+0")
        self.root.resizable(0,0)

                # variables
        self.var_dep=StringVar()
        self.var_course=StringVar()
        self.var_year=StringVar()   
        self.var_sem=StringVar()
        self.var_id=StringVar()
        self.var_name=StringVar()
        self.var_div=StringVar()
        self.var_roll=StringVar()
        self.var_gender=StringVar()
        self.var_dob=StringVar()
        self.var_email=StringVar()
        self.var_phone=StringVar()
        self.var_address=StringVar()
        # self.photo_sample=StringVar()
        

        faceframe=Frame(self.root,bg="#FFFFFF")
        faceframe.place(x=0,y=0,width=1300,height=734)

        # Heading
        heading = Label(faceframe, text="Attendance Window",font=('times now roman', 35,"bold"),bg="#CFE4FA", fg="blue")
        heading.place(x=0,y=0,width=1300,height=60)

        # Left frame
        Left_frame=LabelFrame(faceframe, text="Attendance Details", font=('times now roman', 15, "bold"), bg="#CFE4FA", fg="blue",bd=2,relief=RIDGE)
        Left_frame.place(x=10,y=100,width=640,height=550)

        # class_student_frame
        class_frame=Frame(Left_frame,bg="#FFFFFF",bd=2,relief=RIDGE)
        class_frame.place(x=3,y=0,width=630,height=500)

        # department
        dep_label=Label(class_frame,text='Department :',font=('roman new time',13,"bold"),bg="#f1f1f1")
        dep_label.grid(row=0,column=0,padx=(5,5),pady=(25,5),sticky='w')

        dep_combo=ttk.Combobox(class_frame,textvariable=self.var_dep,font=('roman new time',12),state="readonly",cursor="hand2")
        dep_combo["values"]=("Select Department","Computer","IT","CSE")
        dep_combo.current(0)
        dep_combo.grid(row=0,column=1,pady=(25,5),sticky='w')

        # Course
        Course_label=Label(class_frame,text='Course :',font=('roman new time',13,"bold"),bg="#f1f1f1")
        Course_label.grid(row=0,column=2,padx=(5,0),pady=(25,5),sticky='w')

        Course_combo=ttk.Combobox(class_frame,textvariable=self.var_course,font=('roman new time',12),state="readonly",cursor="hand2")
        Course_combo["values"]=("Select Course","AI","ML","DBMS")
        Course_combo.current(0)
        Course_combo.grid(row=0,column=3,padx=(0,5),pady=(25,5),sticky='w')

        # Name
        Student_name_label=Label(class_frame,text='Name :',font=('roman new time',13,"bold"),bg="#f1f1f1")
        Student_name_label.grid(row=1,column=0,padx=(5,5),pady=(25,5),sticky='w')
        Student_name_entry=ttk.Entry(class_frame,textvariable=self.var_name,font=('roman new time',12))
        Student_name_entry.grid(row=1,column=1,padx=(0,5),pady=5,sticky='w')

        # ID
        StudentId_label=Label(class_frame,text='ID :',font=('roman new time',13,"bold"),bg="#f1f1f1")
        StudentId_label.grid(row=1,column=2,padx=(5,5),pady=(25,5),sticky='w')
        StudentId_entry=ttk.Entry(class_frame,textvariable=self.var_id,font=('roman new time',12))
        StudentId_entry.grid(row=1,column=3,padx=(0,5),pady=5,sticky='w')

        # Class Division
        class_div_label=Label(class_frame,text='Division :',font=('roman new time',13,"bold"),bg="#f1f1f1")
        class_div_label.grid(row=2,column=0,padx=(5,5),pady=(25,5),sticky='w')
        class_div_entry=ttk.Entry(class_frame,textvariable=self.var_div,font=('roman new time',12))
        class_div_entry.grid(row=2,column=1,padx=(0,5),sticky='w')

        # Roll No.
        roll_no_label=Label(class_frame,text='Roll No. :',font=('roman new time',13,"bold"),bg="#f1f1f1")
        roll_no_label.grid(row=2,column=2,padx=(5,5),pady=(25,5),sticky='w')
        roll_no_entry=ttk.Entry(class_frame,textvariable=self.var_roll,font=('roman new time',12))
        roll_no_entry.grid(row=2,column=3,padx=(0,5),sticky='w')

        # Time
        timeing_label=Label(class_frame,text='Timeing :',font=('roman new time',13,"bold"),bg="#ffffff")
        timeing_label.grid(row=3,column=0,padx=(5,5),pady=(25,5),sticky='w')
        timeing_entry=ttk.Entry(class_frame,font=('roman new time',13))
        timeing_entry.grid(row=3,column=1,padx=(0,5),sticky='w')

        # Date
        date_label=Label(class_frame,text='Date :',font=('roman new time',13,"bold"),bg="#ffffff")
        date_label.grid(row=3,column=2,padx=(5,5),pady=(25,5),sticky='w')
        date_entry=ttk.Entry(class_frame,font=('roman new time',13))
        date_entry.grid(row=3,column=3,padx=(0,5),sticky='w')
        

        # attendance
        attendance_label=Label(class_frame,text='Attendance :',font=('roman new time',13,"bold"),bg="#ffffff")
        attendance_label.grid(row=4,column=0,padx=(5,5),pady=(25,5),sticky='w')
        attendance_combo=ttk.Combobox(class_frame,font=('roman new time',12),state="readonly",cursor="hand2",width=10)
        attendance_combo["values"]=("Status","Present","Absent")
        attendance_combo.current(0)
        attendance_combo.grid(row=4,column=1,padx=(0,5),pady=(25,5),sticky='w')

        # search_entry=Entry(class_frame,font=('roman new time',13),bg='lightyellow',width=15)
        # search_entry.grid(row=0,column=3)

        # button frame
        button_frame=Frame(class_frame,bd=2,bg="#f1f1f1")
        button_frame.place(x=0,y=300,width=620,height=150)

        # buttons
        import_button=Button(button_frame,text="Import csv",font=("roman new times",12,"bold"), bg="#0147bf",fg="#ffffff",width=10, cursor="hand2",)
        import_button.grid(row=0,column=0,padx=(90,20),pady=(20,25))

        export_button=Button(button_frame,text="Export csv",font=("roman new times",12,"bold"), bg="#0147bf",fg="#ffffff",width=10, cursor="hand2",)
        export_button.grid(row=0,column=1,padx=(35,20),pady=(20,25))

        search_button=Button(button_frame,text="Search",font=("roman new times",12,"bold"), bg="#0147bf",fg="#ffffff",width=10, cursor="hand2",)
        search_button.grid(row=0,column=2,padx=(35,20),pady=(20,25))


        update_button=Button(button_frame,text="Update",font=("roman new times",12,"bold"), bg="#0147bf",fg="#ffffff",width=10, cursor="hand2",)
        update_button.grid(row=1,column=0,padx=(90,20),pady=(20,25))

        delete_button=Button(button_frame,text="Delete",font=("roman new times",12,"bold"), bg="#0147bf",fg="#ffffff",width=10, cursor="hand2",)
        delete_button.grid(row=1,column=1,padx=(35,20),pady=(20,25))

        clear_button=Button(button_frame,text="Clear",font=("roman new times",12,"bold"), bg="#0147bf",fg="#ffffff",width=10, cursor="hand2",)
        clear_button.grid(row=1,column=2,padx=(35,20),pady=(20,25))

        # Right frame
        Right_frame=LabelFrame(faceframe, text="Attendance List", font=('times now roman', 15, "bold"), bg="#CFE4FA", fg="blue",bd=2,relief=RIDGE)
        Right_frame.place(x=655,y=100,width=640,height=550)

        # table frame
        table_frame=Frame(Right_frame,bd=2,relief=RIDGE)
        table_frame.place(x=3,y=0,width=630,height=500)

        scrollx=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scrolly=ttk.Scrollbar(table_frame,orient=VERTICAL)

        self.student_table=ttk.Treeview(table_frame,columns=('dep', 'course', 'year',"sem","id",'name',
                                                              "div","roll","gender","dob","email", "phone",
                                                              "address","photo"),show='headings',
                              yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
 
        scrollx.config(command=self.student_table.xview)
        scrolly.config(command=self.student_table.yview)

        # # treeview.pack(fill=BOTH,expand=1)
        # self.student_table.heading('dep', text='Department')
        # self.student_table.heading('course', text='Course')
        # self.student_table.heading('year', text='Year')
        # self.student_table.heading('sem', text='Semester')
        # self.student_table.heading('id', text='Student ID')
        # self.student_table.heading('name', text='Name')
        # self.student_table.heading('div', text='Division')
        # self.student_table.heading('roll', text='Roll No.')
        # self.student_table.heading('gender', text='Gender')
        # self.student_table.heading('dob', text='DOB')
        # self.student_table.heading('email', text='Email')
        # self.student_table.heading('phone', text='Phone')
        # self.student_table.heading('address', text='Address')
        # self.student_table.heading('photo', text='Photo Sample')
        # self.student_table['show']='headings'

        # self.student_table.pack(fill=BOTH,expand=1)

        # self.student_table.column('dep', width=80)
        # self.student_table.column('course', width=50) 
        # self.student_table.column('year', width=50)
        # self.student_table.column('sem', width=30)
        # self.student_table.column('id', width=80)
        # self.student_table.column('name', width=100)
        # self.student_table.column('div', width=60)
        # self.student_table.column('roll', width=80)
        # self.student_table.column('gender', width=60)
        # self.student_table.column('dob', width=80)
        # self.student_table.column('email', width=100)
        # self.student_table.column('phone', width=80)
        # self.student_table.column('address', width=150)
        # self.student_table.column('photo', width=80)

        # self.student_table.pack(fill=BOTH,expand=1)
        # self.student_table.bind("<ButtonRelease>", self.get_cursor)   
        # self.fetch_data()  # Fetch data from the database to populate the table

        self.update(self.root)

# function declaration

    def add_data(self):
        if self.var_dep.get()=="Select Department" or self.var_name.get()=="" or self.var_id.get()=="":
            messagebox.showerror("Error","All fields are required",parent=self.root)
        else:
            # Add data to the database
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="1234",
                    database="face_system"
                )
                cursor = conn.cursor()
                cursor.execute("INSERT INTO face VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                               (self.var_dep.get(), self.var_course.get(), self.var_year.get(),
                                self.var_sem.get(), self.var_id.get(), self.var_name.get(), 
                                self.var_div.get(), self.var_roll.get(), self.var_gender.get(), 
                                self.var_dob.get(), self.var_email.get(), self.var_phone.get(), 
                                self.var_address.get(), self.var_radio.get()))
                conn.commit()
                self.fetch_data()  # Refresh the table after adding data
                conn.close()
                self.reset_data()  # Reset the form fields after adding data
                messagebox.showinfo("Success", "Data added successfully", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Error due to {str(e)}", parent=self.root)


    def fetch_data(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="face_system"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM face")
        data = cursor.fetchall()
        conn.close()

        if len(data) != 0:
            self.student_table.delete(*self.student_table.get_children())
            for row in data:
                self.student_table.insert('', END, values=row)
        conn.close()

    # get cursor
    def get_cursor(self, event=""):
        cursor_focus = self.student_table.focus()
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
        self.var_radio.set(data[13])



        # update function
    def update_data(self):
        if self.var_dep.get()=="Select Department" or self.var_name.get()=="" or self.var_id.get()=="" :
            messagebox.showerror("Error","All fields are required",parent=self.root)
        else:
            try:
                Update=messagebox.askyesno("Update","Do you want to update this data?",parent=self.root)
                if Update>0:
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="1234",
                        database="face_system"
                )
                    cursor = conn.cursor()
                    cursor.execute("UPDATE face SET dep=%s, course=%s, year=%s, sem=%s, name=%s, `div`=%s, roll=%s, gender=%s, dob=%s, email=%s, phone=%s, address=%s, photo=%s WHERE id=%s",
                        (self.var_dep.get(), self.var_course.get(), self.var_year.get(), 
                         self.var_sem.get(), self.var_name.get(), self.var_div.get(), 
                         self.var_roll.get(), self.var_gender.get(), self.var_dob.get(), 
                         self.var_email.get(), self.var_phone.get(), self.var_address.get(), 
                         self.var_radio.get(), self.var_id.get()))
                    conn.commit()
                    self.fetch_data()
                    conn.close()
                    self.reset_data()   # Reset the form fields after updating data
                    messagebox.showinfo("Success", "Data updated successfully", parent=self.root)
                else:
                    if not Update:
                        return
            except Exception as e:
                messagebox.showerror("Error", f"Error due to {str(e)}", parent=self.root)
            
            
            #delete function

    def delete_data(self):
        if self.var_id.get()=="":
            messagebox.showerror("Error","Student ID is required",parent=self.root)
        else:
            try:
                delete=messagebox.askyesno("Delete","Do you want to delete this data?",parent=self.root)
                if delete>0:
                    conn = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="1234",
                        database="face_system"
                    )
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM face WHERE id=%s", (self.var_id.get(),))
                    conn.commit()
                    self.fetch_data()
                    conn.close()
                    self.reset_data()   # Reset the form fields after deleting data
                    messagebox.showinfo("Success", "Data deleted successfully", parent=self.root)
                else:
                    if not delete:
                        return
            except Exception as e:
                messagebox.showerror("Error", f"Error due to {str(e)}", parent=self.root)

    def reset_data(self):
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Year")
        self.var_sem.set("Select Semester")
        self.var_id.set("")
        self.var_name.set("")
        self.var_div.set("")
        self.var_roll.set("")
        self.var_gender.set("")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_radio.set("")
        self.fetch_data()

        
    def update(self, root):
        subtitlelabel = Label(self.root, text=" ",font=('times now roman', 12,"bold"),bg="#1060B7", fg="#ffffff")
        subtitlelabel.place(x=0,y=60,width=1300,height=30)
        date_time=time.strftime(' %B %d, %Y \t\t\t  %I:%M:%S %p on %A ')
        subtitlelabel.config(text=f"{date_time}" )
        subtitlelabel.after(1000,self.update, root)


if __name__ == "__main__":
    root=Tk()
    obj=attendance(root)
    root.mainloop()
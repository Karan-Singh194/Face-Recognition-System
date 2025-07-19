from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import subprocess
import time

class Face:
    def __init__(self,root):
        self.root=root
        # Create login root
        self.root.title("Admin Page")
        self.root.geometry("1300x734+0+0")
        self.root.resizable(0,0)
        

        faceframe=Frame(self.root,bg="#FFFFFF")
        faceframe.place(x=0,y=0,width=1300,height=734)

        # Heading
        heading = Label(faceframe, text="Student Face Detail",font=('times now roman', 35,"bold"),bg="#CFE4FA", fg="blue")
        heading.place(x=0,y=0,width=1300,height=60)

        # Left frame
        Left_frame=LabelFrame(faceframe, text="Student Details", font=('times now roman', 15, "bold"), bg="#CFE4FA", fg="black",bd=2,relief=RIDGE)
        Left_frame.place(x=10,y=100,width=640,height=600)

        current_course_frame=LabelFrame(Left_frame, text="Current Course Details", font=('times now roman', 13, "bold"), bg="#FFFFFF", fg="blue",bd=2,relief=RIDGE)
        current_course_frame.place(x=3,y=10,width=630,height=150)

        # department
        dep_label=Label(current_course_frame,text='Department :',font=('roman new time',13,"bold"),bg="#f1f1f1")
        dep_label.grid(row=0,column=0,padx=(5,5),sticky='w')

        dep_combo=ttk.Combobox(current_course_frame,font=('roman new time',12),state="readonly",cursor="hand2")
        dep_combo["values"]=("Select Department","Computer","IT","CSE")
        dep_combo.current(0)
        dep_combo.grid(row=0,column=1,sticky='w')

        # Course
        Course_label=Label(current_course_frame,text='Course :',font=('roman new time',13,"bold"),bg="#f1f1f1")
        Course_label.grid(row=0,column=2,padx=(5,5),sticky='w')

        Course_combo=ttk.Combobox(current_course_frame,font=('roman new time',12),state="readonly",cursor="hand2")
        Course_combo["values"]=("Select Course","AI","ML","DBMS")
        Course_combo.current(0)
        Course_combo.grid(row=0,column=3,padx=(0,5),sticky='w')

        # Year
        year_label=Label(current_course_frame,text='Year :',font=('roman new time',13,"bold"),bg="#f1f1f1")
        year_label.grid(row=1,column=0,padx=(5,5),sticky='w')

        year_combo=ttk.Combobox(current_course_frame,font=('roman new time',12),state="readonly",cursor="hand2")
        year_combo["values"]=("Select Year","1st","2nd","3rd","4th")
        year_combo.current(0)
        year_combo.grid(row=1,column=1,padx=(0,5),pady=(10,5),sticky='w')

        # Semester
        sem_label=Label(current_course_frame,text='Semester:',font=('roman new time',13,"bold"),bg="#f1f1f1")
        sem_label.grid(row=1,column=2,padx=(0,5),sticky='w')

        sem_combo=ttk.Combobox(current_course_frame,font=('roman new time',12),state="readonly",cursor="hand2")
        sem_combo["values"]=("Select Semester","1st","2nd","3rd","4th","5th","6th","7th","8th")
        sem_combo.current(0)
        sem_combo.grid(row=1,column=3,padx=(0,5),pady=(10,5),sticky='w')

        # class_student_frame
        class_student_frame=LabelFrame(Left_frame, text="Class Student information", font=('times now roman', 13, "bold"), bg="#FFFFFF", fg="blue",bd=2,relief=RIDGE)
        class_student_frame.place(x=3,y=170,width=630,height=400)


        # Student Name
        Student_name_label=Label(class_student_frame,text='Student Name:',font=('roman new time',13,"bold"),bg="#f1f1f1")
        Student_name_label.grid(row=0,column=0,padx=(0,5),sticky='w')
        Student_name_entry=ttk.Entry(class_student_frame,font=('roman new time',12),cursor="hand2")
        Student_name_entry.grid(row=0,column=1,padx=(0,5),pady=5,sticky='w')

        # Student ID
        StudentId_label=Label(class_student_frame,text='Student ID:',font=('roman new time',13,"bold"),bg="#f1f1f1")
        StudentId_label.grid(row=0,column=2,padx=(0,5),sticky='w')
        StudentId_entry=ttk.Entry(class_student_frame,font=('roman new time',12),cursor="hand2")
        StudentId_entry.grid(row=0,column=3,padx=(0,5),pady=5,sticky='w')

        # Class Division
        class_div_label=Label(class_student_frame,text='Class Division:',font=('roman new time',13,"bold"),bg="#f1f1f1")
        class_div_label.grid(row=1,column=0,padx=(0,5),sticky='w')
        class_div_entry=ttk.Entry(class_student_frame,font=('roman new time',12),cursor="hand2")
        class_div_entry.grid(row=1,column=1,padx=(0,5),pady=5,sticky='w')

        # Roll No.
        roll_no_label=Label(class_student_frame,text='Roll No.:',font=('roman new time',13,"bold"),bg="#f1f1f1")
        roll_no_label.grid(row=1,column=2,padx=(0,5),sticky='w')
        roll_no_entry=ttk.Entry(class_student_frame,font=('roman new time',12),cursor="hand2")
        roll_no_entry.grid(row=1,column=3,padx=(0,5),pady=5,sticky='w')

        # gender
        gender_label=Label(class_student_frame,text='Gender:',font=('roman new time',13,"bold"),bg="#f1f1f1")
        gender_label.grid(row=2,column=0,padx=(0,5),sticky='w')
        gender_combo=ttk.Combobox(class_student_frame,font=('roman new time',12),state="readonly",cursor="hand2",width=15)
        gender_combo["values"]=("Select Gender","Male","Female","Other")
        gender_combo.current(0)
        gender_combo.grid(row=2,column=1,padx=(0,5),pady=5,sticky='w')

        # dob
        dob_label=Label(class_student_frame, text='DOB',font=("roman new times",13,"bold"),bg="#f1f1f1")
        dob_label.grid(row=2,column=2,padx=(0,5),sticky='w')
        dob_date_entry=DateEntry(class_student_frame,width=18,font=("roman new times",12),state="readonly",date_pattern='dd/mm/yyyy')
        dob_date_entry.grid(row=2,column=3,padx=(0,5),pady=5,sticky='w')

        # email
        email_label=Label(class_student_frame,text='Email:',font=('roman new time',13,"bold"),bg="#f1f1f1")
        email_label.grid(row=3,column=0,padx=(0,5),sticky='w')
        email_entry=ttk.Entry(class_student_frame,font=('roman new time',12),cursor ="hand2")
        email_entry.grid(row=3,column=1,padx=(0,5),pady=5,sticky='w')

        # phone
        phone_label=Label(class_student_frame,text='Phone:',font=('roman new time',13,"bold"),bg="#f1f1f1")
        phone_label.grid(row=3,column=2,padx=(0,5),sticky='w')
        phone_entry=ttk.Entry(class_student_frame,font=('roman new time',12),cursor ="hand2")
        phone_entry.grid(row=3,column=3,padx=(0,5),pady=5,sticky='w')   

        # address
        address_label=Label(class_student_frame,text='Address:',font=('roman new time',13,"bold"),bg="#f1f1f1")
        address_label.grid(row=4,column=0,padx=(0,5),sticky='w')
        address_text=Text(class_student_frame,font=('roman new time',12),cursor="hand2",width=30,height=3)
        address_text.grid(row=4,column=1,columnspan=3,padx=(0,5),pady=5,sticky='w') 
          
        # radio button
        radio_button=ttk.Radiobutton(class_student_frame,text='Take Photo Sample',value="Yes",cursor="hand2")
        radio_button.grid(row=5,column=0,padx=(0,5),pady=(10,5),sticky='w')
        radio_button2=ttk.Radiobutton(class_student_frame,text='No Photo Sample',value="No",cursor="hand2")
        radio_button2.grid(row=5,column=1,padx=(0,5),pady=(10,5),sticky='w')

        # button frame
        button_frame=Frame(class_student_frame,bd=2,bg="#f1f1f1")
        button_frame.place(x=0,y=260,width=620,height=100)

        # buttons
        save_button=Button(button_frame,text="Save",font=("roman new times",14), bg="#0147bf", fg="#fefefe",width=8, cursor="hand2",)
        save_button.grid(row=0,column=0,padx=20)

        update_button=Button(button_frame,text="Update",font=("roman new times",14), bg="#0147bf", fg="#fefefe",width=8, cursor="hand2",)
        update_button.grid(row=0,column=1,padx=20)  

        delete_button=Button(button_frame,text="Delete",font=("roman new times",14), bg="#0147bf", fg="#ffffff",width=8, cursor="hand2",)
        delete_button.grid(row=0,column=2,padx=20)

        reset_button=Button(button_frame,text="Reset",font=("roman new times",14), bg="#0147bf", fg="#cfe4fa",width=8, cursor="hand2",)
        reset_button.grid(row=0,column=3,padx=20)

        take_photo_button=Button(button_frame,text="Take Photo Sample",font=("roman new times",9,"bold"), bg="#0147bf", fg="#cfe4fa",width=20, cursor="hand2",)
        take_photo_button.grid(row=1,column=0,padx=10,pady=(20,0))

        update_button=Button(button_frame,text="Update Photo Sample",font=("roman new times",9,"bold"), bg="#0147bf", fg="#cfe4fa",width=20, cursor="hand2",)
        update_button.grid(row=1,column=2,padx=10,pady=(20,0))



        # Right frame
        Right_frame=LabelFrame(faceframe, text="Student List", font=('times now roman', 15, "bold"), bg="#CFE4FA", fg="black",bd=2,relief=RIDGE)
        Right_frame.place(x=655,y=100,width=640,height=600)

        # Searching frame

        search_frame=LabelFrame(Right_frame, text="Search System", font=('times now roman', 13, "bold"), bg="#FFFFFF", fg="blue",bd=2,relief=RIDGE)
        search_frame.place(x=3,y=10,width=630,height=85)

        search_label=Label(search_frame,text='Search :',font=('roman new time',13,"bold"),bg="#ffffff")
        search_label.grid(row=0,column=0,padx=(0,5),sticky='w')

        search_combo=ttk.Combobox(search_frame,font=('roman new time',12),state="readonly",cursor="hand2",width=10)
        search_combo["values"]=("Search by","Roll No.","Name")
        search_combo.current(0)
        search_combo.grid(row=0,column=2,padx=(5,15),pady=(5,5),sticky='w')

        search_entry=Entry(search_frame,font=('roman new time',13),bg='lightyellow',width=15)
        search_entry.grid(row=0,column=3)

        search_button=Button(search_frame,text="Search",font=("roman new times",12,"bold"), bg="#0147bf",fg="#ffffff",width=8, cursor="hand2",)
        search_button.grid(row=0,column=4,padx=15)

        show_button=Button(search_frame,text="Show All",font=("roman new times",12,"bold"), bg="#0147bf",fg="#ffffff",width=8, cursor="hand2",)
        show_button.grid(row=0,column=5)

        # table frame

        table_frame=Frame(Right_frame,bd=2,relief=RIDGE)
        table_frame.place(x=3,y=100,width=630,height=250)

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

        # treeview.pack(fill=BOTH,expand=1)
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
        self.student_table['show']='headings'

        self.student_table.pack(fill=BOTH,expand=1)

        self.student_table.column('dep', width=100)
        self.student_table.column('course', width=80) 
        self.student_table.column('year', width=50)
        self.student_table.column('sem', width=60)
        self.student_table.column('id', width=80)
        self.student_table.column('name', width=150)
        self.student_table.column('div', width=50)
        self.student_table.column('roll', width=80)
        self.student_table.column('gender', width=50)
        self.student_table.column('dob', width=50)
        self.student_table.column('email', width=80)
        self.student_table.column('phone', width=80)
        self.student_table.column('address', width=80)
        self.student_table.column('photo', width=100)

        update(self.root)


def update(a):
    subtitlelabel = Label(a, text=" ",font=('times now roman', 12,"bold"),bg="#1060B7", fg="#ffffff")
    subtitlelabel.place(x=0,y=60,width=1300,height=30)
    date_time=time.strftime(' %B %d, %Y \t\t\t  %I:%M:%S %p on %A ')
    subtitlelabel.config(text=f"{date_time}" )
    subtitlelabel.after(1000,update,a)


if __name__ == "__main__":
    root=Tk()
    obj=Face(root)
    root.mainloop()
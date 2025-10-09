from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import time
from tkinter import messagebox
import os
import csv
from tkinter import filedialog

mydata=[]

class attendance:
    def __init__(self,root):
        self.root=root
        self.root.title("Attendance Details")
        self.root.geometry("1300x734+0+0")
        self.root.resizable(0,0)
        try:
            self.root.wm_iconbitmap("face-icon.ico")
        except TclError:
            print("Icon 'face-icon.ico' not found.")

        # ==================== variables ====================
        self.var_dep=StringVar()
        self.var_course=StringVar()
        self.var_id=StringVar()
        self.var_name=StringVar()
        self.var_div=StringVar()
        self.var_roll=StringVar()
        self.var_time=StringVar()
        self.var_date=StringVar()
        self.var_attendance=StringVar()
        
        # NEW: This variable will store the exact row selected from the table
        self.original_selected_row = None

        faceframe=Frame(self.root,bg="#FFFFFF")
        faceframe.place(x=0,y=0,width=1300,height=734)

        # Heading
        heading = Label(faceframe, text="Attendance Window",font=('times now roman', 35,"bold"),bg="#CFE4FA", fg="blue")
        heading.place(x=0,y=0,width=1300,height=60)

        # back button
        b=Button(self.root,text="Back",cursor="hand2",font=('times now roman', 20,"bold"),bg="#EF2A2A", fg="white",command=self.root.destroy)
        b.place(x=1180,y=12,width=100,height=35)
        
        # Live Clock
        self.update_clock(self.root)

        # Left frame
        Left_frame=LabelFrame(faceframe, text="Attendance Details", font=('times now roman', 15, "bold"), bg="#CFE4FA", fg="blue",bd=2,relief=RIDGE)
        Left_frame.place(x=10,y=100,width=640,height=550)

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
        Student_name_entry=ttk.Entry(class_frame,textvariable=self.var_name,font=('roman new time',12),state="readonly")
        Student_name_entry.grid(row=1,column=1,padx=(0,5),pady=(25,5),sticky='w')

        # ID
        StudentId_label=Label(class_frame,text='ID :',font=('roman new time',13,"bold"),bg="#f1f1f1")
        StudentId_label.grid(row=1,column=2,padx=(5,5),pady=(25,5),sticky='w')
        StudentId_entry=ttk.Entry(class_frame,textvariable=self.var_id,font=('roman new time',12),state="readonly")
        StudentId_entry.grid(row=1,column=3,padx=(0,5),pady=(25,5),sticky='w')

        # Class Division
        class_div_label=Label(class_frame,text='Division :',font=('roman new time',13,"bold"),bg="#f1f1f1")
        class_div_label.grid(row=2,column=0,padx=(5,5),pady=(25,5),sticky='w')
        class_div_entry=ttk.Entry(class_frame,textvariable=self.var_div,font=('roman new time',12),state="readonly")
        class_div_entry.grid(row=2,column=1,padx=(0,5),sticky='w')

        # Roll No.
        roll_no_label=Label(class_frame,text='Roll No. :',font=('roman new time',13,"bold"),bg="#f1f1f1")
        roll_no_label.grid(row=2,column=2,padx=(5,5),pady=(25,5),sticky='w')
        roll_no_entry=ttk.Entry(class_frame,textvariable=self.var_roll,font=('roman new time',12),state="readonly")
        roll_no_entry.grid(row=2,column=3,padx=(0,5),pady=(25,5),sticky='w')

        # Time
        timeing_label=Label(class_frame,text='Time :',font=('roman new time',13,"bold"),bg="#ffffff")
        timeing_label.grid(row=3,column=0,padx=(5,5),pady=(25,5),sticky='w')
        timeing_entry=ttk.Entry(class_frame,textvariable=self.var_time,font=('roman new time',13),state="readonly")
        timeing_entry.grid(row=3,column=1,padx=(0,5),pady=(25,5),sticky='w')

        # Date
        date_label=Label(class_frame,text='Date :',font=('roman new time',13,"bold"),bg="#ffffff")
        date_label.grid(row=3,column=2,padx=(5,5),pady=(25,5),sticky='w')
        date_entry=ttk.Entry(class_frame,textvariable=self.var_date,font=('roman new time',13),state="readonly")
        date_entry.grid(row=3,column=3,padx=(0,5),pady=(25,5),sticky='w')

        # attendance
        attendance_label=Label(class_frame,text='Attendance :',font=('roman new time',13,"bold"),bg="#ffffff")
        attendance_label.grid(row=4,column=0,padx=(5,5),pady=(25,5),sticky='w')
        attendance_combo=ttk.Combobox(class_frame,textvariable=self.var_attendance,font=('roman new time',12),state="readonly",cursor="hand2",width=10)
        attendance_combo["values"]=("Status","Present","Absent")
        attendance_combo.current(0)
        attendance_combo.grid(row=4,column=1,padx=(0,5),pady=(25,5),sticky='w')

        # button frame
        button_frame=Frame(class_frame,bd=2,bg="#f1f1f1")
        button_frame.place(x=0,y=300,width=620,height=150)

        # buttons
        import_button=Button(button_frame,text="Import csv",font=("roman new times",12,"bold"), bg="#0147bf", fg="#ffffff",width=10, cursor="hand2",command=self.importcsv)
        import_button.grid(row=0,column=0,padx=(90,20),pady=(20,25))

        export_button=Button(button_frame,text="Export csv",font=("roman new times",12,"bold"), bg="#0147bf", fg="#ffffff",width=10, cursor="hand2",command=self.exportcsv)
        export_button.grid(row=0,column=1,padx=(35,20),pady=(20,25))

        remove_button=Button(button_frame,text="Deselect",font=("roman new times",12,"bold"), bg="#0147bf", fg="#ffffff",width=10, cursor="hand2",command=self.remove_selection)
        remove_button.grid(row=0,column=2,padx=(35,20),pady=(20,25))

        update_button=Button(button_frame,text="Update",font=("roman new times",12,"bold"), bg="#0147bf", fg="#ffffff",width=10, cursor="hand2",command=self.update_data)
        update_button.grid(row=1,column=0,padx=(90,20),pady=(20,25))

        delete_button=Button(button_frame,text="Delete",font=("roman new times",12,"bold"), bg="#0147bf", fg="#ffffff",width=10, cursor="hand2",command=self.delete_data)
        delete_button.grid(row=1,column=1,padx=(35,20),pady=(20,25))

        clear_button=Button(button_frame,text="Clear",font=("roman new times",12,"bold"), bg="#0147bf", fg="#ffffff",width=10, cursor="hand2",command=self.clear_data)
        clear_button.grid(row=1,column=2,padx=(35,20),pady=(20,25))

        # Right frame
        Right_frame=LabelFrame(faceframe, text="Attendance List", font=('times now roman', 15, "bold"), bg="#CFE4FA", fg="blue",bd=2,relief=RIDGE)
        Right_frame.place(x=655,y=100,width=640,height=550)

        table_frame=Frame(Right_frame,bd=2,relief=RIDGE)
        table_frame.place(x=3,y=0,width=630,height=500)

        scrollx=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scrolly=ttk.Scrollbar(table_frame,orient=VERTICAL)

        self.attendance_table=ttk.Treeview(table_frame,columns=("id","roll",'name','dep', 'course',"div","time","date","attendance"),show='headings', yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.attendance_table.xview)
        scrolly.config(command=self.attendance_table.yview)

        self.attendance_table.heading('id', text='ID')
        self.attendance_table.heading('roll', text='Roll No.')
        self.attendance_table.heading('name', text='Name')
        self.attendance_table.heading('dep', text='Department')
        self.attendance_table.heading('course', text='Course')
        self.attendance_table.heading('div', text='Division')
        self.attendance_table.heading('time', text='Time')
        self.attendance_table.heading('date', text='Date')
        self.attendance_table.heading('attendance', text='Attendance')

        self.attendance_table.column('id', width=30)
        self.attendance_table.column('roll', width=60)
        self.attendance_table.column('name', width=100)
        self.attendance_table.column('dep', width=80)
        self.attendance_table.column('course', width=50) 
        self.attendance_table.column('div', width=60)
        self.attendance_table.column('time', width=65)
        self.attendance_table.column('date', width=75)
        self.attendance_table.column('attendance', width=80)
        
        self.attendance_table.pack(fill=BOTH,expand=1)
        self.attendance_table.bind("<ButtonRelease>", self.get_cursor)
        
        self.importcsv(first_time=True)

    # ==================== Function Declarations ====================

    def fetch_data(self,rows):
        self.attendance_table.delete(*self.attendance_table.get_children())
        for row in rows:
            self.attendance_table.insert("", END, values=row)

    def importcsv(self, first_time=False):
        global mydata
        mydata.clear()
        if first_time:
            fin = os.path.join(os.getcwd(), "attendance/attendance.csv")
        else:
            fin = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open CSV", filetypes=(("CSV File", "*.csv"), ("All File", "*.*")), parent=self.root)
        
        if fin and os.path.exists(fin):
            with open(fin, "r") as myfile:
                csvread = csv.reader(myfile, delimiter=",")
                for i in csvread:
                    mydata.append(i)
            self.fetch_data(mydata)

    def exportcsv(self):
        try:
            if len(mydata)<1:
                messagebox.showerror("No Data","No Data found to export", parent=self.root)
                return False
            fin=filedialog.asksaveasfilename(initialdir=os.getcwd(),title="Save CSV",filetypes=(("CSV File","*.csv"),("All File","*.*")),parent=self.root, defaultextension=".csv")
            if fin:
                with open(fin,mode="w",newline="") as myfile:
                    exp_write=csv.writer(myfile,delimiter=",")
                    for i in mydata:
                        exp_write.writerow(i)
                    messagebox.showinfo("Data Export", "Your data was exported to "+os.path.basename(fin)+" successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error due to {str(e)}", parent=self.root)

    # UPDATED: This now stores the selected row's data for precise updates
    def get_cursor(self, event=""):
        cursor_focus = self.attendance_table.focus()
        if not cursor_focus:
            return
            
        content = self.attendance_table.item(cursor_focus)
        data = content['values']

        self.original_selected_row = list(data)

        self.var_id.set(data[0])
        self.var_roll.set(data[1])
        self.var_name.set(data[2])
        self.var_dep.set(data[3])
        self.var_course.set(data[4])
        self.var_div.set(data[5])
        self.var_time.set(data[6])
        self.var_date.set(data[7])
        self.var_attendance.set(data[8])

    def remove_selection(self):
        self.attendance_table.selection_remove(self.attendance_table.selection())
        self.clear_data()

    # UPDATED: Logic to handle non-unique IDs by using a composite key
    def update_data(self):
        # Check if a row was selected
        if self.original_selected_row is None:
            messagebox.showerror("Error", "Please select a record to update.", parent=self.root)
            return

        # Get the new data from the input fields
        new_data = [
            self.var_id.get(), self.var_roll.get(), self.var_name.get(),
            self.var_dep.get(), self.var_course.get(), self.var_div.get(),
            self.var_time.get(), self.var_date.get(), self.var_attendance.get()
        ]

        # --- KEY CHANGE ---
        # Get the composite key (ID, Time, Date) from the originally selected row.
        # NOTE: Adjust indices if your column order is different.
        # Assuming: ID is at index 0, Time is at 6, Date is at 7
        try:
            original_id = self.original_selected_row[0]
            original_time = self.original_selected_row[6]
            original_date = self.original_selected_row[7]
        except IndexError:
            messagebox.showerror("Error", "Invalid record selected. Please re-select.", parent=self.root)
            return

        record_found = False
        # Loop through your main data list to find the exact record
        for i, record in enumerate(mydata):
            # Compare using the composite key (ID, Date, and Time)
            if (str(record[0]) == str(original_id) and 
                str(record[7]) == str(original_date) and 
                str(record[6]) == str(original_time)):
                
                mydata[i] = new_data  # Update the row in the list
                record_found = True
                break  # Exit the loop once the record is found

        if record_found:
            self._save_to_csv()
            self.fetch_data(mydata)
            messagebox.showinfo("Success", "Record updated successfully.", parent=self.root)
            self.original_selected_row = None # Clear the selection
        else:
            messagebox.showerror("Error", "Could not find the original record. It may have been modified. Please re-select.", parent=self.root)

    # UPDATED: Corrected delete logic using a composite key
    def delete_data(self):
        selected_item = self.attendance_table.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a record to delete.", parent=self.root)
            return

        # Get the values from the selected row in the table
        content = self.attendance_table.item(selected_item)
        selected_row_values = content['values']

        # --- KEY CHANGE ---
        # Extract the composite key to uniquely identify the row to be deleted.
        # Assuming: ID is at index 0, Time is at 6, Date is at 7
        try:
            id_to_delete = selected_row_values[0]
            time_to_delete = selected_row_values[6]
            date_to_delete = selected_row_values[7]
        except IndexError:
            messagebox.showerror("Error", "Cannot read the selected row's data.", parent=self.root)
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this specific record?", parent=self.root)
        if not confirm:
            return

        record_to_remove_index = -1
        # Loop through the data to find the index of the exact record
        for i, record in enumerate(mydata):
            # Compare using the composite key for a precise match
            if (str(record[0]) == str(id_to_delete) and
                str(record[7]) == str(date_to_delete) and
                str(record[6]) == str(time_to_delete)):
                record_to_remove_index = i
                break # Found it, so we can stop searching

        # If the record was found (index is not -1), remove it
        if record_to_remove_index != -1:
            mydata.pop(record_to_remove_index) # Remove the item by its index
            
            self._save_to_csv()
            self.fetch_data(mydata)
            self.clear_data()
            self.original_selected_row = None
            messagebox.showinfo("Success", "Record deleted successfully.", parent=self.root)
        else:
            # This is the error you were seeing
            messagebox.showerror("Error", "Could not find the record to delete.", parent=self.root)

    def clear_data(self):
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        self.var_id.set("")
        self.var_name.set("")
        self.var_div.set("")
        self.var_roll.set("")    
        self.var_time.set("")
        self.var_date.set("")
        self.var_attendance.set("Status")
        self.original_selected_row = None
        self.attendance_table.selection_remove(self.attendance_table.selection())

    def update_clock(self, root):
        subtitlelabel = Label(self.root, text=" ",font=('times now roman', 12,"bold"),bg="#1060B7", fg="#ffffff")
        subtitlelabel.place(x=0,y=60,width=1300,height=30)
        date_time=time.strftime(' %B %d, %Y \t\t\t  %I:%M:%S %p on %A ')
        subtitlelabel.config(text=f"{date_time}" )
        subtitlelabel.after(1000,self.update_clock, root)

    # NEW: Helper method to save all changes back to the CSV file
    def _save_to_csv(self):
        try:
            file_path = os.path.join(os.getcwd(), "attendance/attendance.csv")
            with open(file_path, "w", newline="") as myfile:
                csv_writer = csv.writer(myfile, delimiter=",")
                csv_writer.writerows(mydata)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data to CSV: {str(e)}", parent=self.root)


if __name__ == "__main__":
    root=Tk()
    obj=attendance(root)
    root.mainloop()
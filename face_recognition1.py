from tkinter import *
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import time
import datetime
import mysql.connector
import cv2
import threading
import win32con
import win32gui
import time
import logging
import tkinter as tk
import tkinter
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from typing import Optional, Tuple, Dict
import subprocess
from tkinter import filedialog
import csv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
mydata=[]
count = 0
class Face_Recognition:

    def __init__(self,root:tk.Tk):
        self.root=root
        self.root.title("Face Recognition")
        self.root.geometry("1300x734+0+0")
        self.root.resizable(0,0)

        # Try to set icon, but don't crash if it doesn't exist
        try:
            self.root.wm_iconbitmap("face-icon.ico")
        except Exception as e:
            logging.warning(f"Could not load icon: {e}")

        # MODIFIED: Initialize variables for camera and recognition
        self.is_running = False
        self.video_capture = None
        self.face_cascade = None
        self.clf = None
        self.photo = None

        # Database configuration (assuming it's correct)
        # ... (your db_config remains the same)

        # Setup GUI
        self._setup_gui()
        
        # Start clock update
        self._update_clock()

    def _setup_gui(self):
        # Main Heading
        heading = Label(self.root, text="Face Recognition Attendance", font=('Helvetica', 30, "bold"), bg="#cfe4fa", fg="#002D62")
        heading.place(x=0, y=0, width=1300, height=60)

        # Date/Time Bar
        self.datetime_label = tk.Label(self.root, text="", font=('Helvetica', 12, "bold"), bg="#1060B7", fg="white")
        self.datetime_label.place(x=0, y=60, width=1300, height=30)

        # Back Button
        back_button = Button(self.root, text="Back", cursor="hand2", font=('Helvetica', 17, "bold"), bg="#FF0C0C", fg="white", activebackground="#FF022C", command=self.i_exit)
        back_button.place(x=1180, y=10, width=100, height=40)

        # Right Frame for Video Feed
        video_frame = Frame(self.root, bg="black", bd=2, relief=RIDGE)
        video_frame.place(x=640, y=95, width=650, height=490)
        
        # Label that will hold the camera feed
        self.video_label = Label(video_frame, text="CAMERA OFF", font=('Arial', 20, 'bold'), fg='white', bg='black')
        self.video_label.pack(fill=BOTH, expand=True)

        # Left Frame (unchanged)
        self.table()

        # Control and Status Area
        control_frame = Frame(self.root, bg="#CFE4FA", bd=2, relief=RIDGE)
        control_frame.place(x=640, y=590, width=650, height=130)

        # The button remains the same
        self.face_detection_button = Button(control_frame, text="Start Face Detection", cursor="hand2", command=self.toggle_face_recognition,
                                            font=("Helvetica", 18, "bold"), bg="#0147bf", fg="white",
                                            activebackground="#002D62", activeforeground="white")
        self.face_detection_button.pack(pady=10, ipady=10, fill=X, padx=20)

        # MODIFIED: Re-adding the two status labels
        # Label for general system status (at the very bottom)
        self.status_label = tk.Label(control_frame, text="System is ready. Click Start to begin.", fg="green", bg="#CFE4FA", font=("Helvetica", 12, 'italic'))
        self.status_label.pack(fill=X, side=BOTTOM, pady=(0,5))
        
        # Label for specific attendance messages (just above the general one)
        self.status_label_1 = tk.Label(self.Left_frame, text="", fg="blue", bg="#CFE4FA", font=("Helvetica", 12, 'bold'))
        self.status_label_1.place(x=3, y=420)


    # NEW: This method handles the button clicks
    def toggle_face_recognition(self):
        """Starts or stops the face recognition process."""
        if self.is_running:
            self.stop_face_recognition()
        else:
            self.start_face_recognition()

    # MODIFIED: This is the new core video loop
    def update_video_feed(self):
        """Reads a frame, processes it for face recognition, and displays it on the Tkinter label."""
        if not self.is_running:
            return

        ret, img = self.video_capture.read()
        if ret:
            # Resize the frame to fit the label (650x520)
            img = cv2.resize(img, (650, 520))
            
            # Process the image for recognition
            processed_img = self._recognize(img)

            # Convert the image for Tkinter display
            img_rgb = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(img_rgb))
            
            # Update the label with the new frame
            self.video_label.configure(image=self.photo)

        # Repeat this function after 15 milliseconds
        self.video_label.after(15, self.update_video_feed)

    # NEW: The recognition logic is now a helper method
    def _recognize(self, img):
        """Helper function to run the recognition on a single image frame."""
        coord = self._draw_boundary(img, self.face_cascade, 1.1, 10, (255, 25, 255), "Face", self.clf)
        return img

    # NEW: The boundary drawing logic is also a helper method
    def _draw_boundary(self, img, classifier, scaleFactor, minNeighbors, color, text, clf):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            id_num, predict = clf.predict(gray_image[y:y + h, x:x + w])
            confidence = int((100 * (1 - predict / 300)))

            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="1234", database="face_system")
                my_cursor = conn.cursor()

                # Fetch student data based on predicted ID
                my_cursor.execute("SELECT name, roll, dep, id, course, `div` FROM face WHERE id=%s", (id_num,))
                result = my_cursor.fetchone()

                if result and confidence > 77:
                    n, r, d, i, c, div = result
                    cv2.putText(img, f"Student Id: {i}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255,255,255), 2)
                    cv2.putText(img, f"Roll: {r}", (x, y - 25), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255,255,255), 2)
                    cv2.putText(img, f"Name: {n}", (x, y - 45), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255,255,255), 2)
                    self.mark_attendance(str(i), n, r, d, c, div)
                else:
                    cv2.putText(img, "Unknown face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0,0,255), 2)
                
                conn.close()
            except Exception as e:
                logging.error(f"Database error: {e}")

        return img


    def start_face_recognition(self):
        try:
            self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            self.clf = cv2.face.LBPHFaceRecognizer_create()
            self.clf.read("classifier.xml")
        except cv2.error as e:
            messagebox.showerror("Error", "Failed to load model files...", parent=self.root)
            return

        self.video_capture = cv2.VideoCapture(0)
        if not self.video_capture.isOpened():
            messagebox.showerror("Error", "Could not open webcam.", parent=self.root)
            return
        
        self.is_running = True
        
        # Update button and status messages
        self.face_detection_button.config(text="Stop Face Detection", bg="#D2042D", activebackground="#A50021")
        self.status_label.config(text="Detection Active: Looking for faces...", fg="#002D62")
        self.status_label_1.config(text="") # Clear previous attendance message
        
        self.video_label.config(text="")
        self.update_video_feed()

    def stop_face_recognition(self):
        self.is_running = False
        if self.video_capture:
            self.video_capture.release()
        
        if hasattr(self, 'video_label'):
            self.video_label.config(image='')
            self.photo = None
            self.video_label.config(text="CAMERA OFF", font=('Arial', 20, 'bold'), fg='white', bg='black')

        # Update button and status messages
        self.face_detection_button.config(text="Start Face Detection", bg="#0147bf", activebackground="#002D62")
        self.status_label.config(text="System is ready. Click Start to begin.", fg="green")
        self.status_label_1.config(text="") # Clear previous attendance message
                
    def i_exit(self): 
        self.stop_face_recognition()
        self.root.destroy()
        
    # --- All your other methods (table, fetch_data, importcsv, mark_attendance, _update_clock) remain exactly the same ---
    # ... (paste your other methods here unchanged) ...
    def table(self):

        # Right frame
        self.Left_frame=LabelFrame(self.root, text="Attendance List", font=('times now roman', 15, "bold"), bg="#CFE4FA", fg="blue",bd=2,relief=RIDGE)
        self.Left_frame.place(x=10,y=100,width=620,height=500)
        
        # table frame
        table_frame=Frame(self.Left_frame,bd=2,relief=RIDGE)
        table_frame.place(x=3,y=0,width=600,height=400)

        scrollx=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scrolly=ttk.Scrollbar(table_frame,orient=VERTICAL)

        self.attendance_table=ttk.Treeview(table_frame,columns=("id","roll",'name','dep', 'course',"div"
                                                                ,"time","date","attendance"),show='headings',
                                yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)

        scrollx.config(command=self.attendance_table.xview)
        scrolly.config(command=self.attendance_table.yview)

        # treeview.pack(fill=BOTH,expand=1)
        self.attendance_table.heading('id', text='ID')
        self.attendance_table.heading('roll', text='Roll No.')
        self.attendance_table.heading('name', text='Name')
        self.attendance_table.heading('dep', text='Department')
        self.attendance_table.heading('course', text='Course')
        self.attendance_table.heading('div', text='Division')
        self.attendance_table.heading('time', text='Time')
        self.attendance_table.heading('date', text='Date')
        self.attendance_table.heading('attendance', text='Attendance')
        self.attendance_table['show']='headings'

        self.attendance_table.pack(fill=BOTH,expand=1)

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
        # self.attendance_table.bind("<ButtonRelease>", self.get_cursor)   
        # self.fetch_data()  # Fetch data from the database to populate the table

        self.importcsv(first_time=True)


        # fetch csv data
    def fetch_data(self,rows):
        self.attendance_table.delete(*self.attendance_table.get_children())
        for row in rows:
            self.attendance_table.insert("", END, values=row)

        # import csv
    def importcsv(self, first_time=False):
        global mydata
        mydata.clear()

        # If first time calling, directly load attendance.csv
        if first_time:
            fin = os.path.join(os.getcwd(), "attendance\\attendance.csv")
        else:
            fin = filedialog.askopenfilename(
                initialdir=os.getcwd(),
                title="Open CSV",
                filetypes=(("CSV File", "*.csv"), ("All File", "*.*")),
                parent=self.root
            )

            # Only proceed if file exists
        if fin and os.path.exists(fin):
            with open(fin) as myfile:
                csvread = csv.reader(myfile, delimiter=",")
                for i in csvread:
                    mydata.append(i)
            self.fetch_data(mydata)

    def mark_attendance(self, i, n, r, d, div, c):
        with open("attendance\\attendance.csv", "r+", newline='') as f:
            myDataList = f.readlines()
            already_marked_today = False
            today_date = time.strftime('%d/%m/%Y')

            for line in myDataList:
                entry = line.strip().split(',')
                if len(entry) > 1 and entry[0] == i and entry[-2] == today_date:
                    already_marked_today = True
                    break

            if not already_marked_today:
                now = time.strftime('%H:%M:%S')
                f.writelines(f'\n{i},{r},{n},{d},{div},{c},{now},{today_date},Present')
                
                # MODIFIED: Send success message to status_label_1
                self.status_label_1.config(text=f"Attendance Marked: {n} ({r})", fg="green")
                self.importcsv(first_time=True)
            else:
                # MODIFIED: Send warning message to status_label_1
                self.status_label_1.config(text=f"Attendance already marked for {n} today.", fg="red")
                self.importcsv(first_time=True)

    def _update_clock(self):
        """Update the date/time display."""
        date_time = time.strftime(' %B %d, %Y \t\t\t  %I:%M:%S %p on %A ')
        self.datetime_label.config(text=date_time)
        self.datetime_label.after(1000, self._update_clock)

def main():
    root=Tk()
    obj=Face_Recognition(root)
    root.protocol("WM_DELETE_WINDOW", obj.i_exit)
    root.mainloop()

if __name__ == "__main__":
    main()
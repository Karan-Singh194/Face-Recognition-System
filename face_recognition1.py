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

        # Initialize components
        self.is_running = False
        self.video_capture = None
        self.face_cascade = None
        self.recognizer = None

        # Database configuration
        self.db_config = {
            'host': "localhost",
            'user': "root",
            'password': "1234",
            'database': "face_system"
        }

        # Setup GUI
        self._setup_gui()
        
        # Load face detection models
        # self._load_models()
        
        # Start clock update
        self._update_clock()

    def _setup_gui(self):
        # Heading
        heading = Label(self.root, text="Face Recognition",font=('times now roman', 35,"bold"),bg="#cfe4fa", fg="blue")
        heading.place(x=0,y=0,width=1300,height=60)

        # Date/Time label
        self.datetime_label = tk.Label(
            self.root, 
            text="",
            font=('times new roman', 12, "bold"),
            bg="#1060B7", 
            fg="#ffffff"
        )
        self.datetime_label.place(x=0, y=60, width=1300, height=30)


        # back button
        b=Button(self.root,text="Back",cursor="hand2",font=('times now roman', 20,"bold"),bg="#EF2A2A", fg="white",command=self.i_exit)
        b.place(x=1180,y=12,width=100,height=35)


        frame_box=Frame(self.root,bg="#61BAEE")
        frame_box.place(x=637,y=93,width=650,height=520)

        # Status label inside frame
        self.status = tk.Label(
            self.root,
            text="Click Above ⬆️",
            font=('times new roman', 15,'bold'),
            fg="green"
        )
        self.status.place(x=820, y=670)


        Face_Detection=Button(self.root,text="Face Detection",cursor="hand2",command=self.start_face_recognition,
                            font=("times new roman",20,"bold"),bg="#0147bf", fg="#f1f1f1")
        Face_Detection.place(x=820,y=620,width=300,height=50)

        self.status_label = tk.Label(self.root, text="System was ready✔️You can mark your Attendance", fg="green", font=("Arial", 12, 'bold'))
        self.status_label.place(x=3, y= 570)

        self.status_label_1 = tk.Label(self.root, text="Click on Face Detection Button ", fg="green", font=("Arial", 12, 'bold'))
        self.status_label_1.place(x=3, y= 600)
        self.table()

    def table(self):

        # Right frame
        Left_frame=LabelFrame(self.root, text="Attendance List", font=('times now roman', 15, "bold"), bg="#CFE4FA", fg="blue",bd=2,relief=RIDGE)
        Left_frame.place(x=10,y=100,width=620,height=450)
        
        # table frame
        table_frame=Frame(Left_frame,bd=2,relief=RIDGE)
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


    # mark_attendance
    def mark_attendance(self, i, n, r, d, div, c):
        with open("attendance\\attendance.csv", "r+", newline='') as f:
            myDataList = f.readlines()
            already_marked_today = False
            today_date = time.strftime('%d/%m/%Y')

            for line in myDataList:
                entry = line.strip().split(',')
                if entry[0] == i and entry[-2] == today_date:  # ID and Date match
                    already_marked_today = True
                    break

            if not already_marked_today:
                now = time.strftime('%H:%M:%S')
                f.writelines(f'\n{i},{r},{n},{d},{div},{c},{now},{today_date},Present')
                
                # Update label 
                self.status_label.config(text=f"Attendance marked, Name: {n}, Roll No: {i}, Timing: {now}, {today_date}", fg="green")
                # self.attendance_table.delete(*self.attendance_table.get_children())
                self.importcsv(first_time=True)
                global count
                count = 0
            else:
                # Show warning on label
                self.status_label_1.config(text=f"Attendance already marked today for Name: {n}, Roll No: {i}", fg="red")
                self.status.config(text=f"Warning, click on Enter button ", fg="green")

                
                if count == 2:
                    return 
                self.importcsv(first_time=True)
                count = count + 1


    def start_face_recognition(self):
        # import threading
        self.is_running = True
        # threading.Thread(target=self.face_recog, daemon=True).start()
        self.recognition_thread = threading.Thread(target=self.face_recog, daemon=True)
        self.recognition_thread.start()


        # face detection

    def face_recog(self):
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text,clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)
            coord = []

            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                id, predict = clf.predict(gray_image[y:y + h, x:x + w])
                confidence = int((100 * (1 - predict / 300)))

                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="1234",
                    database="face_system"
                )
                my_cursor = conn.cursor()

                my_cursor.execute("SELECT name FROM face WHERE id = "+str(id))
                n = my_cursor.fetchone()
                n="+".join(n)

                my_cursor.execute("SELECT roll FROM face WHERE id = "+str(id))
                r = my_cursor.fetchone()
                r="+".join(r)

                my_cursor.execute("SELECT dep FROM face WHERE id = "+str(id))
                d = my_cursor.fetchone()
                d="+".join(d)

                my_cursor.execute("SELECT id FROM face WHERE id = "+str(id))
                i = my_cursor.fetchone()
                i="+".join(i)

                my_cursor.execute("SELECT course FROM face WHERE id = "+str(id))
                c = my_cursor.fetchone()
                c="+".join(c)

                my_cursor.execute("SELECT `div` FROM face WHERE id = "+str(id))
                div = my_cursor.fetchone()
                div="+".join(div)

                if confidence > 77:
                    cv2.putText(img, f"Student Id: {i}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255,255,255), 2)
                    cv2.putText(img, f"Roll: {r}", (x, y - 25), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255,255,255), 2)
                    cv2.putText(img, f"Name: {n}", (x, y - 45), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255,255,255), 2)
                    cv2.putText(img, f"Department: {d}", (x, y - 65), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255,255,255), 2)
                    self.mark_attendance(i, n, r, d,c,div)
                else:
                    cv2.putText(img, "Unknown face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255,255,255), 2)
                coord = [x, y, w, h]

            return coord
        
        
        def recognize(img,clf,face_cascade):
            coord= draw_boundary(img, face_cascade, 1.1, 10, (255,25,255), "Face", clf)
            return img

        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        cv2.namedWindow("Face Recognition", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Face Recognition", 640, 480)

        # Small delay to let window appear
        time.sleep(0.5)

        # Get handle for OpenCV window
        hwnd = win32gui.FindWindow(None, "Face Recognition")

        # Force window always on top
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST,
                            0, 0, 0, 0,
                            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

        video_capture = cv2.VideoCapture(0)


        while self.is_running:
            ret, img = video_capture.read()
            if not ret:
                print("Failed to grab frame")
                break

            img=recognize(img, clf,face_cascade)
            cv2.imshow("Face Recognition", img)

            if cv2.waitKey(1)==13:
                self.status.config(text=f"Click Above ⬆️ ", fg="green")
                video_capture.release()
                cv2.destroyAllWindows()
                self.stop_face_recognition()
                break



    def _update_clock(self):
        """Update the date/time display."""
        date_time = time.strftime(' %B %d, %Y \t\t\t  %I:%M:%S %p on %A ')
        self.datetime_label.config(text=date_time)
        self.datetime_label.after(1000, self._update_clock)

    def stop_face_recognition(self):
        self.is_running = False # this will tell loop to stop
        # Release video capture if it exists
        if self.video_capture:
            self.video_capture.release()
            cv2.destroyAllWindows()

    def i_exit(self): 
        self.stop_face_recognition()
        self.root.destroy()



        
def main():
    root=Tk()
    obj=Face_Recognition(root)
    root.protocol("WM_DELETE_WINDOW", obj.i_exit)
    root.mainloop()

if __name__ == "__main__":
    main()
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import subprocess
import time
from tkinter import messagebox
import mysql.connector
import cv2



class Face_Recognition:
    def __init__(self,root):
        self.root=root
        self.root.title("Face Recognition")
        self.root.geometry("1300x734+0+0")
        self.root.resizable(0,0)

        # title_label=Label(self.root,text="Face Recognition",font=("times new roman",30,"bold"),bg="black",fg="white")
        # title_label.place(x=0,y=0,width=1300,height=50)

        heading = Label(self.root, text="Face Recognition",font=('times now roman', 35,"bold"),bg="#CFE4FA", fg="blue")
        heading.place(x=0,y=0,width=1300,height=60)

        self.update(self.root)

        train_button=Button(self.root,text="Face Detection",cursor="hand2",command=self.face_recog,
                            font=("times new roman",20,"bold"),bg="#CFE4FA",fg="blue")
        train_button.place(x=500,y=600,width=300,height=50)


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

                if confidence > 77:
                    cv2.putText(img, f"Roll: {r}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255,255,255), 2)
                    cv2.putText(img, f"Name: {n}", (x, y - 25), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255,255,255), 2)
                    cv2.putText(img, f"Department: {d}", (x, y - 45), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255,255,255), 2)
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

        video_capture = cv2.VideoCapture(0)

        while True:
            ret, img = video_capture.read()
            if not ret:
                print("Failed to grab frame")
                break

            img=recognize(img, clf,face_cascade)
            cv2.imshow("Face Recognition", img)

            if cv2.waitKey(1)==13:
                break
        video_capture.release()
        cv2.destroyAllWindows()

    def update(self, root):
        subtitlelabel = Label(self.root, text=" ",font=('times now roman', 12,"bold"),bg="#1060B7", fg="#ffffff")
        subtitlelabel.place(x=0,y=60,width=1300,height=30)
        date_time=time.strftime(' %B %d, %Y \t\t\t  %I:%M:%S %p on %A ')
        subtitlelabel.config(text=f"{date_time}" )
        subtitlelabel.after(1000,self.update, root)



        
if __name__ == "__main__":
    root=Tk()
    obj=Face_Recognition(root)
    root.mainloop()
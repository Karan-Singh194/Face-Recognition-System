from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import time
from face import Face
from train import Train
from face_recognition import Face_Recognition
from attendance import attendance
import os

class Face_recognition_System:
    def __init__(self,root):
        self.root=root
        # Create login root
        self.root.title("Admin Page")
        self.root.geometry("1300x734+0+0")
        self.root.resizable(0,0)

        self.heading = Label(self.root, text="Face Recognition Attendance System",font=('times now roman', 35,"bold"),bg="#CFE4FA", fg="blue")
        self.heading.place(x=0,y=0,width=1300,height=60)

        # img5=Image.open(r"photos\exit.png")
        # img5=img5.resize((25,25), Image.Resampling.LANCZOS)
        # self.photoimg5=ImageTk.PhotoImage(img5)

        b=Button(self.root,text="Exit",cursor="hand2",font=('times now roman', 20,"bold"),bg="#EF2A2A", fg="white",command=self.root.destroy)
        b.place(x=1180,y=12,width=100,height=35)


        # bg
        img=Image.open(r"photos\bg1.png")
        img=img.resize((1300,734), Image.Resampling.LANCZOS)
        self.photoimg=ImageTk.PhotoImage(img)

        bg=Label(self.root,image=self.photoimg)
        bg.place(x=0,y=90,width=1300,height=734)

        # button
        img1=Image.open(r"photos\bg4.png")
        img1=img1.resize((220,220), Image.Resampling.LANCZOS)
        self.photoimg1=ImageTk.PhotoImage(img1)

        b1 = Button(self.root, image=self.photoimg1, cursor="hand2", command=self.Face_Recognition)
        b1.place(x=120,y=100,width=220,height=220)

        L1=Label(self.root,text="Face Detection",font=('times now roman', 12,"bold"))
        L1.place(x=120,y=295,width=218,height=25)


        img2=Image.open(r"photos\attendance.png")
        img2=img2.resize((170,170), Image.Resampling.LANCZOS)
        self.photoimg2=ImageTk.PhotoImage(img2)

        b2=Button(self.root,image=self.photoimg2,cursor="hand2",command=self.attendance)
        b2.place(x=380,y=100,width=220,height=220)

        L2=Label(self.root,text="Attendance",font=('times now roman', 12,"bold"))
        L2.place(x=380,y=295,width=218,height=25)

        
        img3=Image.open(r"photos\computer.png")
        img3=img3.resize((120,110), Image.Resampling.LANCZOS)
        self.photoimg3=ImageTk.PhotoImage(img3)

        b3=Button(self.root,image=self.photoimg3,cursor="hand2",command=self.face_details)
        b3.place(x=120,y=350,width=220,height=220)

        L3=Label(self.root,text="Face Detail",font=('times now roman', 12,"bold"))
        L3.place(x=120,y=545,width=218,height=25)


        img4=Image.open(r"photos\image.png")
        img4=img4.resize((170,170), Image.Resampling.LANCZOS)
        self.photoimg4=ImageTk.PhotoImage(img4)

        b4=Button(self.root,image=self.photoimg4,cursor="hand2",command=self.train_data)
        b4.place(x=380,y=350,width=220,height=220)

        L4=Label(self.root,text="Train Data",font=('times now roman', 12,"bold"))
        L4.place(x=380,y=545,width=218,height=25)

        # img5=Image.open(r"photos\image.png")
        # img5=img5.resize((170,170), Image.Resampling.LANCZOS)
        # self.photoimg5=ImageTk.PhotoImage(img5)

        # b5=Button(self.root,image=self.photoimg5,cursor="hand2",command=lambda: exit(self.root))
        # b5.place(x=640,y=100,width=220,height=220)

        # L5=Label(self.root,text="Face Training",font=('times now roman', 12,"bold"))
        # L5.place(x=640,y=295,width=218,height=25)


        # bg2
        img5=Image.open(r"photos\img5.png")
        img5=img5.resize((570,334), Image.Resampling.LANCZOS)
        self.photoimg5=ImageTk.PhotoImage(img5)

        bg=Label(bg,image=self.photoimg5)
        bg.place(x=700,y=200,width=570,height=334)

        self.update(self.root)

    # buttons  function

    def face_details(self):
        self.new_window=Toplevel(self.root)
        self.app=Face(self.new_window)


    def train_data(self):
        self.new_window=Toplevel(self.root)
        self.app=Train(self.new_window)

    def Face_Recognition(self):
        self.new_window=Toplevel(self.root)
        self.app=Face_Recognition(self.new_window)

    def attendance(self):
        self.new_window=Toplevel(self.root)
        self.app=attendance(self.new_window)

    # Function to update the date and time

    def update(self, root):
        subtitlelabel = Label(self.root, text=" ",font=('times now roman', 12,"bold"),bg="#1060B7", fg="#ffffff")
        subtitlelabel.place(x=0,y=60,width=1300,height=30)
        date_time=time.strftime(' %B %d, %Y \t\t\t  %I:%M:%S %p on %A ')
        subtitlelabel.config(text=f"{date_time}" )
        subtitlelabel.after(1000,self.update, root)



if __name__ == "__main__":
    root=Tk()
    obj=Face_recognition_System(root)
    root.mainloop()
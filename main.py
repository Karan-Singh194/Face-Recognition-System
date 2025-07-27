from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import time
from face import Face
import os

class Face_recognition_System:
    def __init__(self,root):
        self.root=root
        # Create login root
        self.root.title("Admin Page")
        self.root.geometry("1300x734+0+0")
        self.root.resizable(0,0)

        heading = Label(self.root, text="Face Recognition Attendance System",font=('times now roman', 35,"bold"),bg="#CFE4FA", fg="blue")
        heading.place(x=0,y=0,width=1300,height=60)

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

        # b1=Button(self.root,image=self.photoimg1,cursor="hand2")
        b1 = Button(self.root, image=self.photoimg1, cursor="hand2", command=self.face_details)
        b1.place(x=120,y=100,width=220,height=220)

        L1=Label(self.root,text="Face Detail",font=('times now roman', 12,"bold"))
        L1.place(x=120,y=295,width=218,height=25)


        img2=Image.open(r"photos\attendance.png")
        img2=img2.resize((170,170), Image.Resampling.LANCZOS)
        self.photoimg2=ImageTk.PhotoImage(img2)

        b2=Button(self.root,image=self.photoimg2,cursor="hand2")
        b2.place(x=380,y=100,width=220,height=220)

        L2=Label(self.root,text="Attandance",font=('times now roman', 12,"bold"))
        L2.place(x=380,y=295,width=218,height=25)

        
        img3=Image.open(r"photos\computer.png")
        img3=img3.resize((120,110), Image.Resampling.LANCZOS)
        self.photoimg3=ImageTk.PhotoImage(img3)

        b3=Button(self.root,image=self.photoimg3,cursor="hand2")
        b3.place(x=120,y=350,width=220,height=220)

        L3=Label(self.root,text="Settings",font=('times now roman', 12,"bold"))
        L3.place(x=120,y=545,width=218,height=25)


        img4=Image.open(r"photos\exit.png")
        img4=img4.resize((120,120), Image.Resampling.LANCZOS)
        self.photoimg4=ImageTk.PhotoImage(img4)

        b4=Button(self.root,image=self.photoimg4,cursor="hand2",command=lambda: exit(self.root))
        b4.place(x=380,y=350,width=220,height=220)

        L4=Label(self.root,text="Exit",font=('times now roman', 12,"bold"))
        L4.place(x=380,y=545,width=218,height=25)

        img5=Image.open(r"photos\cat2.png")
        img5=img5.resize((170,170), Image.Resampling.LANCZOS)
        self.photoimg5=ImageTk.PhotoImage(img5)

        b5=Button(self.root,image=self.photoimg5,cursor="hand2",command=self.open_img)
        b5.place(x=640,y=100,width=220,height=220)

        L5=Label(self.root,text="Data store",font=('times now roman', 12,"bold"))
        L5.place(x=640,y=295,width=218,height=25)

        img6=Image.open(r"photos\image.png")
        img6=img6.resize((170,170), Image.Resampling.LANCZOS)
        self.photoimg6=ImageTk.PhotoImage(img6)

        b6=Button(self.root,image=self.photoimg6,cursor="hand2")
        b6.place(x=900,y=100,width=220,height=220)

        L6=Label(self.root,text="Face Train",font=('times now roman', 12,"bold"))
        L6.place(x=900,y=295,width=218,height=25)


        # bg2
        # img5=Image.open(r"photos\img5.png")
        # img5=img5.resize((570,334), Image.Resampling.LANCZOS)
        # self.photoimg5=ImageTk.PhotoImage(img5)

        # bg=Label(bg,image=self.photoimg5)
        # bg.place(x=700,y=200,width=570,height=334)

        update(self.root)


    # oprn data store window
    def open_img(self):
        os.startfile("data")


        # function buttons

    def face_details(self):
        self.new_window=Toplevel(self.root)
        self.app=Face(self.new_window)




def update(a):
    subtitlelabel = Label(a, text=" ",font=('times now roman', 12,"bold"),bg="#1060B7", fg="#ffffff")
    subtitlelabel.place(x=0,y=60,width=1300,height=30)
    date_time=time.strftime(' %B %d, %Y \t\t\t  %I:%M:%S %p on %A ')
    subtitlelabel.config(text=f"{date_time}" )
    subtitlelabel.after(1000,update,a)



if __name__ == "__main__":
    root=Tk()
    obj=Face_recognition_System(root)
    root.mainloop()
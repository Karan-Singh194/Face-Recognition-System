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
import numpy as np
from face import Face 


class Face_Recognition:
    def __init__(self,root):
        self.root=root
        self.root.title("Face Recognition")
        self.root.geometry("1300x734+0+0")
        self.root.resizable(0,0)

        title_label=Label(self.root,text="Face Recognitaion",font=("times new roman",30,"bold"),bg="black",fg="white")
        title_label.place(x=0,y=0,width=1300,height=50)

        train_button=Button(self.root,text="Face Detection",cursor="hand2",
                            font=("times new roman",20,"bold"),bg="black",fg="white")
        train_button.place(x=0,y=600,width=1300,height=50)


        # face detection



        
if __name__ == "__main__":
    root=Tk()
    obj=Face_Recognition(root)
    root.mainloop()
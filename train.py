from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess
import time
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np


class Train:
    def __init__(self,root):
        self.root=root
        self.root.title("Train Data")
        self.root.geometry("1300x734+0+0")
        self.root.resizable(0,0)

        title_label=Label(self.root,text="Face Detail",font=("times new roman",30,"bold"),bg="black",fg="white")
        title_label.place(x=0,y=0,width=1300,height=50)

        train_button=Button(self.root,text="Train Data",cursor="hand2",command=self.train_classifier,
                            font=("times new roman",20,"bold"),bg="black",fg="white")
        train_button.place(x=0,y=600,width=1300,height=50)

    def train_classifier(self):
        data_dir = ("data")
        path=[os.path.join(data_dir, file) for file in os.listdir(data_dir)]
        faces = []
        ids = []

        for image_path in path:
            img = Image.open(image_path).convert('L') # Convert image to grayscale
            imageNp=np.array(img,'uint8')
            id = int(os.path.split(image_path)[1].split('.')[1])
            
            faces.append(imageNp)
            ids.append(id)
            cv2.imshow("Training", imageNp)
            cv2.waitKey(1)==13  # Press Enter to continue
        ids=np.array(ids)

        # train classifier face recognizer
        clf=cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("classifier.xml")
        # Save the model
        cv2.destroyAllWindows()
        messagebox.showinfo("Success", "Training data saved successfully")

        
if __name__ == "__main__":
    root=Tk()
    obj=Train(root)
    root.mainloop()
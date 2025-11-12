import tkinter as tk
from tkinter import ttk, messagebox, Label, Button, Toplevel
from PIL import Image, ImageTk
import time
import os

# --- Import all application modules ---
try:
    from face_detail import Face
    from capture_image import PhotoCapture
    from fe import FaceRecognition
    from attendance import attendance
    from developer import Developer
except ImportError as e:
    messagebox.showerror("Fatal Error", f"Failed to import a required module: {e}.\nPlease ensure all .py files are in the same directory.")
    # We can't continue if modules are missing
    # In a real app, we might exit here
    print(f"Import Error: {e}")


class Face_recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Page")
        self.root.geometry("1300x734+0+0")
        self.root.resizable(0, 0)
        
        # --- FIXED: Added try...except for icon ---
        try:
            self.root.wm_iconbitmap("face-icon.ico")
        except tk.TclError:
            print("Icon 'face-icon.ico' not found.")

        self.heading = Label(self.root, text="Face Recognition Attendance System", font=('times now roman', 35, "bold"), bg="#CFE4FA", fg="blue")
        self.heading.place(x=0, y=0, width=1300, height=60)

        b = Button(self.root, text="Exit", cursor="hand2", font=('times now roman', 20, "bold"), bg="#EF2A2A", fg="white", command=self.i_exit)
        b.place(x=1180, y=12, width=100, height=35)

        # --- FIXED: Clock Label (Created once) ---
        self.subtitlelabel = Label(self.root, text=" ", font=('times now roman', 12, "bold"), bg="#1060B7", fg="#ffffff")
        self.subtitlelabel.place(x=0, y=60, width=1300, height=30)
        self._update_clock_text() # Start the clock loop

        # --- FIXED: Background Image with safety check ---
        self.photoimg = self._load_image(r"photos\bg1.png", (1300, 734))
        bg = Label(self.root, image=self.photoimg)
        bg.place(x=0, y=90, width=1300, height=734)

        # --- All other buttons and images with safety checks ---

        # Face Detection Button
        self.photoimg1 = self._load_image(r"photos\bg4.png", (220, 220))
        b1 = Button(self.root, image=self.photoimg1, cursor="hand2", command=self.Face_Recognition, borderwidth=0, bg="#F7EAF8")
        b1.place(x=120, y=100, width=220, height=220)
        L1 = Label(self.root, text="Face Detection", font=('times now roman', 12, "bold"))
        L1.place(x=120, y=295, width=218, height=25)

        # Attendance Button
        self.photoimg2 = self._load_image(r"photos\attendance.png", (170, 170))
        b2 = Button(self.root, image=self.photoimg2, cursor="hand2", command=self.attendance, borderwidth=0, bg="#F7EAF8")
        b2.place(x=380, y=100, width=220, height=220)
        L2 = Label(self.root, text="Attendance", font=('times now roman', 12, "bold"))
        L2.place(x=380, y=295, width=218, height=25)

        # Face Detail Button
        self.photoimg3 = self._load_image(r"photos\computer.png", (120, 110))
        b3 = Button(self.root, image=self.photoimg3, cursor="hand2", command=self.face_details, borderwidth=0, bg="#F7EAF8")
        b3.place(x=120, y=350, width=220, height=220)
        L3 = Label(self.root, text="Face Detail", font=('times now roman', 12, "bold"))
        L3.place(x=120, y=545, width=218, height=25)

        # Photo Capture Button
        self.photoimg4 = self._load_image(r"photos\image.png", (170, 170))
        b4 = Button(self.root, image=self.photoimg4, cursor="hand2", command=self.PhotoCapture, borderwidth=0, bg="#F7EAF8")
        b4.place(x=380, y=350, width=220, height=220)
        L4 = Label(self.root, text="Photo Capture", font=('times now roman', 12, "bold"))
        L4.place(x=380, y=545, width=218, height=25)

        # Contact Us / Developer Button
        L5 = Label(self.root, text="Contact us", font=('times now roman', 12, "bold"), fg="blue", bg="#F7EAF8", cursor="hand2")
        L5.place(x=1110, y=705, width=218, height=25)
        L5.bind("<Button-1>", self.on_click)

        # Decorative Image
        self.photoimg5 = self._load_image(r"photos\img5.png", (570, 334))
        bg_deco = Label(bg, image=self.photoimg5) # Placed on 'bg' label
        bg_deco.place(x=700, y=200, width=570, height=334)

    def _load_image(self, path, size):
        """Helper function to load images safely."""
        if os.path.exists(path):
            try:
                img = Image.open(path)
                img = img.resize(size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading image {path}: {e}")
        else:
            print(f"Warning: Could not find image: {path}")
            # Return a 1x1 transparent pixel as a placeholder
            return ImageTk.PhotoImage(Image.new("RGBA", (1, 1), (0, 0, 0, 0)))

    # --- Button functions ---
    
    def _open_window(self, WindowClass):
        """Helper to open new Toplevel windows."""
        try:
            self.new_window = Toplevel(self.root)
            self.app = WindowClass(self.new_window)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open window: {e}", parent=self.root)

    def face_details(self):
        self._open_window(Face)

    def PhotoCapture(self):
        self._open_window(PhotoCapture)

    def Face_Recognition(self):
        self._open_window(FaceRecognition)

    def attendance(self):
        self._open_window(attendance)

    def on_click(self, event):
        self._open_window(Developer)

    def i_exit(self):
        # --- FIXED: Uses a local variable to avoid overwriting the function ---
        confirm_exit = messagebox.askyesno("Face Recognition", "Are you sure you want to exit?", parent=self.root)
        if confirm_exit:
            self.root.destroy()
        else:
            return

    # --- FIXED: Function to update the clock text (no memory leak) ---
    def _update_clock_text(self):
        date_time = time.strftime(' %B %d, %Y \t\t\t \t%I:%M:%S %p on %A ')
        self.subtitlelabel.config(text=f"{date_time}")
        self.subtitlelabel.after(1000, self._update_clock_text)

def run_main():
    """This function is called by login.py to start the dashboard."""
    root = tk.Tk()
    obj = Face_recognition_System(root)
    root.mainloop()

# Note: The if __name__ == "__main__": block is removed
# This file is now intended to be run via login.py
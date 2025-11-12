import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import time
import webbrowser
# Removed unused 'subprocess' import

class Developer:
    def __init__(self, root):
        self.root = root
        self.root.title("Developer Detail")
        self.root.geometry("1300x734+0+0")
        self.root.resizable(0, 0)
        self.root.configure(bg="#F8FAFD")
        
        # --- FIXED: Added try/except for missing icon ---
        try:
            self.root.wm_iconbitmap("face-icon.ico")
        except tk.TclError:
            print("Icon 'face-icon.ico' not found.")

        # Heading
        heading = tk.Label(self.root, text="Developer Detail",
                                font=('times new roman', 35, "bold"),
                                bg="#CFE4FA", fg="blue")
        heading.place(x=0, y=0, width=1300, height=60)

        # Back button
        b = tk.Button(self.root, text="Back", cursor="hand2",
                       font=('times new roman', 20, "bold"),
                       bg="#EF2A2A", fg="white", command=self.root.destroy)
        b.place(x=1180, y=12, width=100, height=35)

        # Developer photo (optional - replace image)
        # try:
        #     img = Image.open("developer.jpg") # Replace with your image path
        #     img = img.resize((200, 200))
        #     self.photo = ImageTk.PhotoImage(img)
        #     tk.Label(self.root, image=self.photo, bg="#F8FAFD").place(x=50, y=120)
        # except:
        #     tk.Label(self.root, text="[Your Photo]", font=("Arial", 14),
        #             bg="#F8FAFD", fg="gray").place(x=100, y=200)

        # About Me Section
        about_title = tk.Label(self.root, text="About Me",
                                font=('times new roman', 25, "bold"),
                                bg="#F8FAFD", fg="#1060B7")
        about_title.place(x=300, y=120)

        about_text = (
            "Hello! I am Karan Singh, a passionate developer currently pursuing B-Tech IT.\n"
            "I specialize in Python development and have created a Face Recognition System\n"
            "that can identify individuals with high accuracy using OpenCV and machine learning.\n"
            "I enjoy working with AI/ML, computer vision, and developing user-friendly interfaces."
        )

        about_label = tk.Label(self.root, text=about_text,
                                font=('times new roman', 14),
                                bg="#F8FAFD", justify=tk.LEFT, anchor="w") # <-- FIXED: tk.LEFT
        about_label.place(x=300, y=170)

        # Clickable portfolio link
        l1 = tk.Label(self.root, text="GitHub",
                       font=('times new roman', 14, "underline"),
                       fg="blue", bg="#F8FAFD", cursor="hand2")
        l1.place(x=300, y=300)
        l2 = tk.Label(self.root, text="LinkedIn",
                       font=('times new roman', 14, "underline"),
                       fg="blue", bg="#F8FAFD", cursor="hand2")
        l2.place(x=380, y=300)
        l3 = tk.Label(self.root, text="Any Query Email <contactkaransingh194@gmail.com>",
                       font=('times new roman', 14),
                        bg="#F8FAFD")
        l3.place(x=300, y=270)
        l1.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/Karan-Singh194"))
        l2.bind("<Button-1>", lambda e: webbrowser.open("https://www.linkedin.com/in/karan-singh-contact194/"))

        # --- FIXED: Clock Memory Leak ---
        # 1. Create the label ONCE
        self.subtitlelabel = tk.Label(self.root, text=" ",
                                      font=('times new roman', 12, "bold"),
                                      bg="#1060B7", fg="#ffffff")
        self.subtitlelabel.place(x=0, y=60, width=1300, height=30)
        
        # 2. Start the update loop
        self._update_clock_text()

    def _update_clock_text(self):
        """Updates the clock label text every second."""
        # --- FIXED: This function now ONLY updates the text ---
        date_time = time.strftime(' %B %d, %Y \t\t\t \t%I:%M:%S %p on %A ')
        self.subtitlelabel.config(text=f"{date_time}")
        # 3. Schedule itself to run again
        self.subtitlelabel.after(1000, self._update_clock_text)


if __name__ == "__main__":
    root = tk.Tk() # <-- FIXED: tk.Tk
    obj = Developer(root)
    root.mainloop()
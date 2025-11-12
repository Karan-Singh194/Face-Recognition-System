import tkinter as tk
# --- MODIFIED: Added filedialog ---
from tkinter import ttk, messagebox, Label, Button, Frame, Entry, StringVar, filedialog
from PIL import Image, ImageTk
import cv2
import os
import mysql.connector
from mysql.connector import Error

class PhotoCapture:
    """
    A GUI to capture, confirm, and save student photos,
    integrated with a MySQL database.
    """

    def __init__(self, root):
# ... (rest of __init__ is unchanged) ...
        self.root = root
        self.root.title("Add New Student Photo")
        self.root.geometry("700x650+300+50") # Set size and position
        self.root.resizable(False, False)

        # --- Database Configuration ---
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "1234", # From your example
            "database": "face_system"
        }
        self.student_name_map = {} # Stores {id: name} mapping
        
        # --- TKinter Variables ---
        self.student_name_var = StringVar()

        # --- Internal State Variables ---
        self.video_capture = None
        self.photo = None
        self.is_running = True
        self.image_dir = "student_images"
        self.state = "live_feed"
        self.captured_face_roi = None
        self.stored_id = ""
        self.stored_name = ""

        # Load Haar Cascade
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        if self.face_cascade.empty():
            messagebox.showerror("Cascade Error", "Could not load face cascade model.")
            self.on_close()
            return

        os.makedirs(self.image_dir, exist_ok=True)

        # --- GUI Setup ---
        self._setup_gui()
        
        # --- Camera & Database Setup ---
        self.start_camera()
        self.load_pending_students() # <--- NEW: Load students from DB

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _setup_gui(self):
        """Creates and places all the GUI widgets."""
        main_frame = Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.video_label = Label(main_frame, bg="black")
        # We move the .pack() call for video_label later

        # --- 'Live Feed' controls ---
        self.capture_controls_frame = Frame(main_frame, bg="#f0f0f0")
        # We move the .pack() call for capture_controls_frame later

        input_frame = Frame(self.capture_controls_frame, bg="#f0f0f0")
        input_frame.pack(fill=tk.X)

        # --- Student ID (Combobox) ---
        Label(input_frame, text="Student ID:", font=('Helvetica', 12)).pack(side=tk.LEFT, padx=(0, 5))
        self.student_id_combo = ttk.Combobox(
            input_frame, 
            font=('Helvetica', 12), 
            width=13, 
            state='readonly'
        )
        self.student_id_combo.pack(side=tk.LEFT, padx=5)
        self.student_id_combo.bind("<<ComboboxSelected>>", self.on_student_selected)

        # --- Student Name (Read-only) ---
        Label(input_frame, text="Student Name:", font=('Helvetica', 12)).pack(side=tk.LEFT, padx=(20, 5))
        name_entry = Entry(
            input_frame, 
            textvariable=self.student_name_var, 
            font=('Helvetica', 12), 
            width=25, 
            state='readonly'
        )
        name_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # --- MODIFIED: Button Frame ---
        # This new frame will hold the two buttons
        button_frame = Frame(self.capture_controls_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=10)

        # Capture Button
        self.capture_button = Button(
            button_frame, # <--- Added to new frame
            text="Capture Photo",
            font=('Helvetica', 14, 'bold'), 
            bg="#007bff", 
            fg="white",
            command=self.capture_photo
        )
        self.capture_button.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 5))
        
        # --- NEW: Upload Button ---
        self.upload_button = Button(
            button_frame, # <--- Added to new frame
            text="Upload from Drive",
            font=('Helvetica', 14, 'bold'), 
            bg="#17a2b8", # A teal color
            fg="white",
            command=self.upload_photo
        )
        self.upload_button.pack(side=tk.RIGHT, fill=tk.X, expand=True, ipady=8, padx=(5, 0))

        
        # --- 'Confirmation' controls ---
        self.confirm_controls_frame = Frame(main_frame, bg="#f0f0f0")

        retake_button = Button(
            self.confirm_controls_frame, text="Retake", font=('Helvetica', 14),
            bg="#ffc107", fg="black", command=self.retake_photo
        )
        retake_button.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 5))

        self.save_button = Button(
            self.confirm_controls_frame, text="Confirm & Save", font=('Helvetica', 14, 'bold'),
            bg="#28a745", fg="white", command=self.save_photo
        )
        self.save_button.pack(side=tk.RIGHT, fill=tk.X, expand=True, ipady=8, padx=(5, 0))
        
        # --- Bottom frame for Status and Close button ---
        bottom_frame = Frame(main_frame, bg="#f0f0f0")
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(5,0)) # <--- PACK THIS FIRST (at the bottom)

        # --- Status label ---
        self.status_label = Label(bottom_frame, text="Loading student data...", font=('Helvetica', 10, 'italic'), fg="gray", anchor='w')
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=5, padx=(0,10))
        
        # --- Close Button ---
        self.close_button = Button(
            bottom_frame,
            text="Close",
            font=('Helvetica', 10, 'bold'),
            bg="#dc3545", # Red color
            fg="white",
            command=self.on_close,
            width=10
        )
        self.close_button.pack(side=tk.RIGHT, padx=(0, 5), ipady=2)

        # --- Now pack the expanding and top-aligned widgets ---
        self.video_label.pack(pady=10, fill=tk.BOTH, expand=True) # <--- PACK VIDEO SECOND
        self.capture_controls_frame.pack(fill=tk.X, pady=10)     # <--- PACK CAPTURE CONTROLS THIRD


    def load_pending_students(self):
        """Fetches students with 'No' photo status from the DB."""
# ... (this function is unchanged) ...
        self.status_label.config(text="Connecting to database...", fg="gray")
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Select students from 'face' table where 'photo' column is 'No'
            cursor.execute("SELECT id, name FROM face WHERE photo = 'No'")
            students = cursor.fetchall()
            
            # Clear previous data
            self.student_name_map.clear()
            student_ids = []
            
            if students:
                for student_id, student_name in students:
                    student_ids.append(student_id)
                    self.student_name_map[student_id] = student_name
                
                self.student_id_combo['values'] = student_ids
                self.student_id_combo.set('') # Clear selection
                self.student_name_var.set('')
                self.status_label.config(text=f"Loaded {len(student_ids)} pending students.", fg="blue")
                self.capture_button.config(state=tk.NORMAL)
                self.upload_button.config(state=tk.NORMAL) # <--- NEW: Enable upload button
            else:
                self.student_id_combo['values'] = []
                self.student_id_combo.set('')
                self.student_name_var.set('')
                self.status_label.config(text="All student photos are already captured.", fg="green")
                self.capture_button.config(state=tk.DISABLED) # No students to capture
                self.upload_button.config(state=tk.DISABLED) # <--- NEW: Disable upload button

        except Error as e:
            messagebox.showerror("Database Error", f"Could not connect or fetch data: {e}", parent=self.root)
            self.status_label.config(text="Database connection failed.", fg="red")
            self.capture_button.config(state=tk.DISABLED)
            self.upload_button.config(state=tk.DISABLED) # <--- NEW: Disable upload button
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def on_student_selected(self, event):
# ... (this function is unchanged) ...
        """Updates the name field when a student ID is selected."""
        selected_id = self.student_id_combo.get()
        name = self.student_name_map.get(selected_id, "")
        self.student_name_var.set(name)
        self.status_label.config(text=f"Ready to capture photo for {name}.", fg="gray")

    def start_camera(self):
# ... (this function is unchanged) ...
        self.video_capture = cv2.VideoCapture(0)
        if not self.video_capture.isOpened():
            messagebox.showerror("Camera Error", "Could not open webcam.", parent=self.root)
            self.on_close()
            return
        self.update_video_feed()

    def update_video_feed(self):
# ... (this function is unchanged) ...
        if self.state != "live_feed" or not self.is_running:
            return

        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
            )
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            self.photo = ImageTk.PhotoImage(image=img)
            self.video_label.configure(image=self.photo)

        self.video_label.after(15, self.update_video_feed)

    def capture_photo(self):
        """Captures a photo from the webcam, finds a face, and switches to confirmation mode."""
        student_id = self.student_id_combo.get()
        student_name = self.student_name_var.get()

        if not student_id or not student_name:
            messagebox.showwarning("Input Required", "Please select a student from the list.", parent=self.root)
            return

        ret, frame = self.video_capture.read()
        if not ret:
            messagebox.showerror("Capture Error", "Failed to capture image.", parent=self.root)
            return
        
        frame = cv2.flip(frame, 1)
        
        # --- Start of refactored logic ---
        self._process_frame_for_confirmation(frame, student_id, student_name)
        # --- End of refactored logic ---

    # --- NEW: Function to upload a photo from drive ---
    def upload_photo(self):
        """Uploads a photo from disk, finds a face, and switches to confirmation mode."""
        student_id = self.student_id_combo.get()
        student_name = self.student_name_var.get()

        if not student_id or not student_name:
            messagebox.showwarning("Input Required", "Please select a student *before* uploading.", parent=self.root)
            return

        # Open file dialog to select an image
        filepath = filedialog.askopenfilename(
            title="Select a Student Photo",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png"), ("All Files", "*.*")]
        )
        if not filepath: # User cancelled
            return
            
        # Load the image using OpenCV
        try:
            frame = cv2.imread(filepath)
            if frame is None:
                raise Exception(f"Could not read image file: {filepath}")
        except Exception as e:
            messagebox.showerror("File Error", f"Failed to load image: {e}", parent=self.root)
            return
            
        # --- Process the loaded frame ---
        # Note: We do NOT flip the image from the drive
        self._process_frame_for_confirmation(frame, student_id, student_name)

    # --- NEW: Helper function to process a frame (from webcam or upload) ---
    def _process_frame_for_confirmation(self, frame, student_id, student_name):
        """Runs face detection on a frame and switches to confirmation screen."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
        )
        
        if len(faces) == 0:
            messagebox.showwarning("Face Error", "No face detected in the image.", parent=self.root)
            return
        elif len(faces) > 1:
            messagebox.showwarning("Face Error", "Multiple faces detected. Please use an image with only one face.", parent=self.root)
            return
        
        # --- Success: A single face was found ---
        (x, y, w, h) = faces[0]
        face_roi = frame[y:y+h, x:x+w]
        
        # --- Call the new helper to show the confirmation screen ---
        self._show_confirmation_screen(face_roi, student_id, student_name)

    # --- NEW: Helper function to switch to confirmation mode ---
    def _show_confirmation_screen(self, face_roi, student_id, student_name):
        """Displays the cropped face and confirmation buttons."""
        
        self.captured_face_roi = face_roi
        self.stored_id = student_id
        self.stored_name = student_name.replace(" ", "_")
        
        self.state = "confirm_photo"
        
        # Stop the camera feed (if it's running)
        # This is handled by self.state check in update_video_feed
        
        # Create a displayable image for the confirmation screen
        face_rgb = cv2.cvtColor(self.captured_face_roi, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(face_rgb).resize((400, 400), Image.Resampling.LANCZOS)
        
        self.photo_confirm = ImageTk.PhotoImage(image=img_pil)
        self.video_label.configure(image=self.photo_confirm)
        
        # Swap the control frames
        self.capture_controls_frame.pack_forget()
        self.confirm_controls_frame.pack(fill=tk.X, pady=10)
        self.status_label.config(text=f"Confirm photo for {student_name} (ID: {student_id})?", fg="blue")


    def retake_photo(self):
# ... (this function is unchanged) ...
        """Discards the photo and returns to the live feed."""
        self.state = "live_feed"
        self.captured_face_roi = None
        self.stored_id = ""
        self.stored_name = ""
        
        self.confirm_controls_frame.pack_forget()
        self.capture_controls_frame.pack(fill=tk.X, pady=10)
        
        # Restore status label text
        selected_id = self.student_id_combo.get()
        if selected_id:
            name = self.student_name_map.get(selected_id, "")
            self.status_label.config(text=f"Ready to capture photo for {name}.", fg="gray")
        else:
            self.status_label.config(text=f"Loaded {len(self.student_name_map)} pending students.", fg="blue")

        self.update_video_feed() # Restart the video feed

    def save_photo(self):
# ... (this function is unchanged) ...
        """Saves the photo and updates the database."""
        # Disable save button to prevent double-click
        self.save_button.config(state=tk.DISABLED)
        
        # 1. Save the image file
        filename = f"{self.stored_id}_{self.stored_name}.jpg"
        filepath = os.path.join(self.image_dir, filename)
        
        try:
            cv2.imwrite(filepath, self.captured_face_roi)
        except Exception as e:
            messagebox.showerror("File Error", f"Failed to save image: {e}", parent=self.root)
            self.save_button.config(state=tk.NORMAL) # Re-enable button
            return

        # 2. Update the database
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Update 'face' table, set 'photo' column to 'Yes'
            sql_query = "UPDATE face SET photo = 'Yes' WHERE id = %s"
            cursor.execute(sql_query, (self.stored_id,))
            conn.commit()
            
            self.status_label.config(text=f"Success! Image saved and database updated.", fg="green")
            
            # 3. Reload student list (removes the student just processed)
            self.load_pending_students()

        except Error as e:
            conn.rollback() # Rollback changes on error
            messagebox.showerror("Database Error", f"Image saved, but DB update failed: {e}", parent=self.root)
            self.status_label.config(text="Error updating database. Photo saved locally.", fg="red")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

        # 4. Reset the UI back to live mode
        self.save_button.config(state=tk.NORMAL) # Re-enable button
        self.retake_photo()

    def on_close(self):
# ... (this function is unchanged) ...
        """Safely closes the window and releases the camera."""
        self.is_running = False
        if self.video_capture:
            self.video_capture.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoCapture(root)
    root.mainloop()
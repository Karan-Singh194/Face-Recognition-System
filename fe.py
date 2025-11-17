import tkinter as tk
from tkinter import ttk, messagebox, Label, Button, Frame, LabelFrame, BOTH, RIDGE, X, BOTTOM
from PIL import Image, ImageTk
import cv2
import os
import sys
import time
import csv
import threading
import logging
from datetime import datetime
from pathlib import Path
from tkinter import filedialog
from typing import Optional, List, Tuple
import numpy as np
import mysql.connector

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.db_config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }
        self.conn = None
        self.connect()

    def connect(self):
        """Establishes a persistent connection to the database."""
        try:
            self.conn = mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to database: {err}")
            self.conn = None

    def get_connection(self):
        """Returns the current connection, reconnects if necessary."""
        try:
            if self.conn is None or not self.conn.is_connected():
                self.connect()
            self.conn.ping(reconnect=True, attempts=1, delay=1)
        except mysql.connector.Error as err:
            self.conn = None
            messagebox.showerror("Database Connection Lost", f"Lost connection to database: {err}. Please restart.")
        return self.conn

    def fetch_all_attendance(self):
        """Fetches all attendance records, joined with student info."""
        conn = self.get_connection()
        if conn is None:
            return []
        
        # This query JOINS the new attendance table with the existing face table
        sql = """
            SELECT
                ar.record_id,         -- The unique key for the attendance record
                f.id,                 -- The student's ID
                f.roll,
                f.name,
                f.dep,
                f.course,
                f.div,
                ar.attendance_time,
                ar.attendance_date,
                ar.attendance_status
            FROM attendance_records AS ar
            JOIN face AS f ON ar.student_id = f.id
            ORDER BY ar.attendance_date DESC, ar.attendance_time DESC
        """
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch attendance data: {err}")
            return []

    def update_attendance(self, record_id, new_status):
        """Updates ONLY the attendance status for a specific record."""
        conn = self.get_connection()
        if conn is None:
            return False
        
        sql = "UPDATE attendance_records SET attendance_status = %s WHERE record_id = %s"
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (new_status, record_id))
                conn.commit()
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to update status: {err}")
            return False

    def delete_attendance(self, record_id):
        """Deletes a specific attendance record by its unique record_id."""
        conn = self.get_connection()
        if conn is None:
            return False
        
        sql = "DELETE FROM attendance_records WHERE record_id = %s"
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (record_id,))
                conn.commit()
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to delete record: {err}")
            return False

    def close(self):
        """Closes the database connection if it's open."""
        if self.conn and self.conn.is_connected():
            self.conn.close()

    def fetch_attendance_for_display(self):
        conn = self.get_connection()
        if conn is None: return []

        # This query gets exactly what your table needs
        sql = """
            SELECT f.id, f.roll, f.name, f.dep, f.course, f.div, 
                ar.attendance_time, ar.attendance_date, ar.attendance_status
            FROM attendance_records AS ar
            JOIN face AS f ON ar.student_id = f.id
            ORDER BY ar.attendance_date DESC, ar.attendance_time DESC
            LIMIT 100 
        """
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error fetching attendance for display: {e}")
            return []
        

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Try to import DeepFace with fallback
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except ImportError:
    logging.warning("DeepFace not installed. Install with: pip install deepface")
    DEEPFACE_AVAILABLE = False

class FaceRecognition:
    """Robust Face Recognition Attendance System"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("1300x734+0+0")
        self.root.resizable(False, False)
        


        # System state
        self.is_running = False
        self.video_capture: Optional[cv2.VideoCapture] = None
        self.photo = None
        self.recognition_thread: Optional[threading.Thread] = None
        self.last_recognition_time = {}
        self.recognition_cooldown = 10  # seconds between recognitions for same person
        
        self.db = DatabaseManager(
            host="localhost",
            user="root",
            password="1234",
            database="face_system"
        )

        # Paths
        self.student_images_path = Path("student_images")
        
        # Data storage
        self.attendance_data: List[List[str]] = []
        self.known_faces_cache = {}
        
        
        # Check dependencies
        if not self._check_dependencies():
            messagebox.showwarning(
                "Dependencies Missing",
                "Some dependencies are missing. The application may not work properly.\n"
                "Please install: pip install deepface opencv-python pillow"
            )
        
        # Setup GUI
        self._setup_gui()
        self._update_clock()
        
        # Load initial data
        self._load_attendance_data()
        
        logging.info("Face Recognition System initialized successfully")

    def _check_dependencies(self) -> bool:
        """Check if all required dependencies are available"""
        dependencies_ok = True
        
        if not DEEPFACE_AVAILABLE:
            dependencies_ok = False
            
        try:
            import cv2
        except ImportError:
            logging.error("OpenCV not installed")
            dependencies_ok = False
            
        return dependencies_ok

    def _setup_gui(self):
        """Setup the GUI components"""
        try:
            # Main Heading
            heading = Label(
                self.root, 
                text="Face Recognition Attendance", 
                font=('Helvetica', 30, "bold"), 
                bg="#cfe4fa", 
                fg="#002D62"
            )
            heading.place(x=0, y=0, width=1300, height=60)

            # Date/Time Bar
            self.datetime_label = Label(
                self.root, 
                text="", 
                font=('Helvetica', 12, "bold"), 
                bg="#1060B7", 
                fg="white"
            )
            self.datetime_label.place(x=0, y=60, width=1300, height=30)

            # Back Button
            back_button = Button(
                self.root, 
                text="Back", 
                cursor="hand2", 
                font=('Helvetica', 17, "bold"), 
                bg="#FF0C0C", 
                fg="white", 
                activebackground="#FF022C", 
                command=self.i_exit
            )
            back_button.place(x=1180, y=10, width=100, height=40)

            # Right Frame for Video Feed
            video_frame = Frame(self.root, bg="black", bd=2, relief=RIDGE)
            video_frame.place(x=640, y=95, width=650, height=490)
            
            self.video_label = Label(
                video_frame, 
                text="CAMERA OFF", 
                font=('Arial', 20, 'bold'), 
                fg='white', 
                bg='black'
            )
            self.video_label.pack(fill=BOTH, expand=True)

            # Left Frame with Attendance Table
            self._setup_table()

            # Control and Status Area
            control_frame = Frame(self.root, bg="#CFE4FA", bd=2, relief=RIDGE)
            control_frame.place(x=640, y=590, width=650, height=130)

            self.face_detection_button = Button(
                control_frame, 
                text="Start Face Detection", 
                cursor="hand2", 
                command=self.toggle_face_recognition,
                font=("Helvetica", 18, "bold"), 
                bg="#0147bf", 
                fg="white",
                activebackground="#002D62", 
                activeforeground="white"
            )
            self.face_detection_button.pack(pady=10, ipady=10, fill=X, padx=20)

            # Status labels
            self.status_label = Label(
                control_frame, 
                text="System ready. Click Start to begin.", 
                fg="green", 
                bg="#CFE4FA", 
                font=("Helvetica", 11, 'italic')
            )
            self.status_label.pack(fill=X, side=BOTTOM, pady=(0, 5))
            
            self.status_label_1 = Label(
                self.left_frame, 
                text="", 
                fg="blue", 
                bg="#CFE4FA", 
                font=("Helvetica", 11, 'bold')
            )
            self.status_label_1.place(x=5, y=420)
            
            # FPS label
            self.fps_label = Label(
                self.left_frame,
                text="FPS: 0",
                fg="gray",
                bg="#CFE4FA",
                font=("Helvetica", 10)
            )
            self.fps_label.place(x=550, y=420)
            
        except Exception as e:
            logging.error(f"Error setting up GUI: {e}")
            messagebox.showerror("GUI Error", f"Failed to setup interface: {e}")

    def _setup_table(self):
        """Setup the attendance table"""
        self.left_frame = LabelFrame(
            self.root, 
            text="Attendance List", 
            font=('Times New Roman', 15, "bold"), 
            bg="#CFE4FA", 
            fg="blue",
            bd=2,
            relief=RIDGE
        )
        self.left_frame.place(x=10, y=100, width=620, height=500)
        
        # Table frame
        table_frame = Frame(self.left_frame, bd=2, relief=RIDGE)
        table_frame.place(x=3, y=0, width=610, height=400)

        # Scrollbars
        scrollx = ttk.Scrollbar(table_frame, orient='horizontal')
        scrolly = ttk.Scrollbar(table_frame, orient='vertical')

        # Treeview
        self.attendance_table = ttk.Treeview(
            table_frame,
            columns=("id", "roll", 'name', 'dep', 'course', "div", "time", "date", "attendance"),
            show='headings',
            yscrollcommand=scrolly.set,
            xscrollcommand=scrollx.set
        )

        scrollx.pack(side='bottom', fill='x')
        scrolly.pack(side='right', fill='y')
        scrollx.config(command=self.attendance_table.xview)
        scrolly.config(command=self.attendance_table.yview)

        # Configure columns
        columns_config = {
            'id': ('ID', 50),
            'roll': ('Roll No.', 70),
            'name': ('Name', 120),
            'dep': ('Department', 80),
            'course': ('Course', 70),
            'div': ('Division', 60),
            'time': ('Time', 70),
            'date': ('Date', 80),
            'attendance': ('Status', 70)
        }
        
        for col, (heading, width) in columns_config.items():
            self.attendance_table.heading(col, text=heading)
            self.attendance_table.column(col, width=width)
        
        self.attendance_table.pack(fill=BOTH, expand=1)

    def toggle_face_recognition(self):
        """Toggle face recognition on/off"""
        if self.is_running:
            self.stop_face_recognition()
        else:
            self.start_face_recognition()
    
    def start_face_recognition(self):
        """Start the face recognition system"""
        try:
            # Check for DeepFace
            if not DEEPFACE_AVAILABLE:
                messagebox.showerror(
                    "Missing Dependency",
                    "DeepFace is not installed. Please install it:\npip install deepface",
                    parent=self.root
                )
                return
            
            # Check for student images
            if not self.student_images_path.exists():
                self.student_images_path.mkdir(exist_ok=True)
                
            image_files = list(self.student_images_path.glob("*.jpg")) + \
                         list(self.student_images_path.glob("*.png")) + \
                         list(self.student_images_path.glob("*.jpeg"))
            
            if not image_files:
                messagebox.showerror(
                    "No Student Images",
                    f"No student images found in '{self.student_images_path}'.\n"
                    "Please add student images in format: ID_Name.jpg",
                    parent=self.root
                )
                return

            self.status_label.config(text="Initializing camera and AI model...", fg="orange")
            self.root.update_idletasks()

            # Initialize camera
            self.video_capture = cv2.VideoCapture(0)
            if not self.video_capture.isOpened():
                # Try alternative camera indices
                for i in range(1, 4):
                    self.video_capture = cv2.VideoCapture(i)
                    if self.video_capture.isOpened():
                        break
                
                if not self.video_capture.isOpened():
                    messagebox.showerror(
                        "Camera Error",
                        "Could not open webcam. Please check your camera.",
                        parent=self.root
                    )
                    self.status_label.config(text="Camera initialization failed", fg="red")
                    return
            
            # Set camera properties for better performance
            self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.video_capture.set(cv2.CAP_PROP_FPS, 30)
            
            self.is_running = True
            self.face_detection_button.config(
                text="Stop Face Detection",
                bg="#D2042D",
                activebackground="#A50021"
            )
            self.status_label.config(text="Face detection active", fg="#002D62")
            self.status_label_1.config(text="")
            self.video_label.config(text="")
            
            # Start video feed
            self.update_video_feed()
            
            logging.info("Face recognition started successfully")
            
        except Exception as e:
            logging.error(f"Error starting face recognition: {e}")
            messagebox.showerror("Error", f"Failed to start face recognition: {e}")
            self.stop_face_recognition()
    
    def stop_face_recognition(self):
        """Stop the face recognition system"""
        try:
            self.is_running = False
            
            # Release camera
            if self.video_capture:
                self.video_capture.release()
                self.video_capture = None
            
            # Clear video display
            self.video_label.config(image='')
            self.photo = None
            self.video_label.config(
                text="CAMERA OFF",
                font=('Arial', 20, 'bold'),
                fg='white',
                bg='black'
            )

            # Update UI
            self.face_detection_button.config(
                text="Start Face Detection",
                bg="#0147bf",
                activebackground="#002D62"
            )
            self.status_label.config(text="System ready. Click Start to begin.", fg="green")
            self.status_label_1.config(text="")
            self.fps_label.config(text="FPS: 0")
            
            logging.info("Face recognition stopped")
            
        except Exception as e:
            logging.error(f"Error stopping face recognition: {e}")

    def _recognize_and_mark(self, img: np.ndarray) -> np.ndarray:
        """Recognize faces and mark attendance"""
        try:
            # Skip if DeepFace not available
            if not DEEPFACE_AVAILABLE:
                return img
            
            # Perform face recognition
            results = DeepFace.find(
                img_path=img,
                db_path=str(self.student_images_path),
                enforce_detection=False,
                model_name='VGG-Face',  # Use a faster model
                distance_metric='cosine',
                silent=True
            )
            
            if results and len(results) > 0 and not results[0].empty:
                for index, row in results[0].iterrows():
                    try:
                        matched_path = row['identity']
                        confidence = 1 - row.get('distance', 0)  # Convert distance to confidence
                        
                        # Only process if confidence is high enough
                        if confidence < 0.58:  # Adjust threshold as needed
                            continue
                        
                        # Extract face coordinates
                        x = int(row.get('source_x', 0))
                        y = int(row.get('source_y', 0))
                        w = int(row.get('source_w', 100))
                        h = int(row.get('source_h', 100))
                        
                        # Draw bounding box
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        
                        # Parse filename for student info
                        filename = Path(matched_path).stem
                        parts = filename.split('_', 1)
                        
                        if len(parts) >= 2:
                            student_id = parts[0]
                            student_name = parts[1].replace('_', ' ')
                            
                            # Draw name and ID label on the box
                            label = f"{student_name} | ID: {student_id}"
                            
                            # Calculate text size for background
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            font_scale = 0.6
                            thickness = 2
                            (text_width, text_height), baseline = cv2.getTextSize(label, font, font_scale, thickness)
                            
                            # Draw background rectangle for text
                            cv2.rectangle(img, 
                                        (x, y + h - 35), 
                                        (x + text_width + 10, y + h), 
                                        (0, 255, 0), 
                                        cv2.FILLED)
                            
                            # Draw text
                            cv2.putText(img, 
                                      label, 
                                      (x + 5, y + h - 10), 
                                      font, 
                                      font_scale, 
                                      (0, 0, 0), 
                                      thickness=2)
                            
                            # Check cooldown period for marking attendance
                            current_time = time.time()
                            last_time = self.last_recognition_time.get(student_id, 0)
                            
                            try:
                                conn = self.db.get_connection()  # <-- Use the fast connection
                                if conn is None:
                                    raise Exception("Database connection failed")

                                my_cursor = conn.cursor()
                                id_num = student_id

                                # Fetch student data based on predicted ID
                                
                                my_cursor.execute("SELECT name, roll, dep, id, course, `div` FROM face WHERE id=%s", (id_num,))
                                result = my_cursor.fetchone()
                            except Exception as e:
                                logging.error(f"Database error: {e}")

                            if current_time - last_time > self.recognition_cooldown:
                                # Mark attendance
                                n, r, d, i, c, div = result
                                self.mark_attendance(
                                    student_id=student_id,
                                    name=student_name,
                                    roll=r,
                                    dept=d,
                                    div=div,
                                    course=c
                                )
                                
                                self.last_recognition_time[student_id] = current_time
                                


                    except Exception as e:
                        logging.warning(f"Error processing recognition result: {e}")
                        continue
                        
        except Exception as e:
            # Log error but don't crash
            logging.debug(f"Recognition error (may be normal): {e}")
            
        return img

    def update_video_feed(self):
        """Update the video feed display"""
        if not self.is_running or not self.video_capture:
            return

        try:
            # Calculate FPS
            start_time = time.time()
            
            ret, frame = self.video_capture.read()
            if ret and frame is not None:
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Perform recognition
                processed_frame = self._recognize_and_mark(frame)
                
                # Convert to RGB for display
                frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                
                # Resize if needed
                img = Image.fromarray(frame_rgb)
                img = img.resize((640, 480), Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                self.photo = ImageTk.PhotoImage(image=img)
                self.video_label.configure(image=self.photo)
                
                # Update FPS
                fps = 1.0 / (time.time() - start_time)
                self.fps_label.config(text=f"FPS: {fps:.1f}")
            else:
                logging.warning("Failed to read frame from camera")
                
        except Exception as e:
            logging.error(f"Error updating video feed: {e}")
            
        # Schedule next update
        if self.is_running:
            self.video_label.after(30, self.update_video_feed)  # ~33 FPS

    def mark_attendance(self, student_id: str, name: str, roll: str, dept: str, div: str, course: str):
        try:
            # 1. Get current date and time in MySQL format
            current_dt = datetime.now()
            time_str = current_dt.strftime('%H:%M:%S')
            date_str_mysql = current_dt.strftime('%Y-%m-%d') # <--- MySQL format
            date_str_display = current_dt.strftime('%d/%m/%Y') # <--- Old format for display

            # 2. Check if already marked in the DATABASE
            already_marked = False
            conn = self.db.get_connection()
            if conn is None:
                self.status_label_1.config(text="Database connection lost!", fg="red")
                return

            with conn.cursor() as cursor:
                sql_check = "SELECT record_id FROM attendance_records WHERE student_id = %s AND attendance_date = %s"
                cursor.execute(sql_check, (student_id, date_str_mysql))
                if cursor.fetchone():
                    already_marked = True

            # 3. If not marked, INSERT into the database
            if not already_marked:
                with conn.cursor() as cursor:
                    sql_insert = """
                        INSERT INTO attendance_records 
                        (student_id, attendance_date, attendance_time, attendance_status) 
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(sql_insert, (student_id, date_str_mysql, time_str, 'Present'))
                    conn.commit()

                self.status_label_1.config(
                    text=f"✓ Attendance marked: {name}",
                    fg="green"
                )
                # Reload table data from DB
                self._load_attendance_data()
                logging.info(f"Attendance marked for {name} (ID: {student_id})")

            else:
                self.status_label_1.config(
                    text=f"Already marked today: {name}",
                    fg="orange"
                )

        except Exception as e:
            logging.error(f"Error marking attendance: {e}")
            self.status_label_1.config(text=f"Error marking attendance", fg="red")



    def _load_attendance_data(self):
        try:
            self.attendance_data = self.db.fetch_attendance_for_display()
            self._update_table()
        except Exception as e:
            logging.error(f"Error loading attendance data: {e}")

    def _update_table(self):
        """Update the attendance table display"""
        try:
            # Clear existing items
            self.attendance_table.delete(*self.attendance_table.get_children())
            
            # Insert data (show most recent first)
            for row in reversed(self.attendance_data[-100:]):  # Show last 100 records
                if len(row) >= 9:  # Ensure row has all columns
                    self.attendance_table.insert("", 0, values=row)
                    
        except Exception as e:
            logging.error(f"Error updating table: {e}")



    def _update_clock(self):
        """Update the date/time display"""
        try:
            date_time = datetime.now().strftime(' %B %d, %Y \t\t\t  %I:%M:%S %p on %A ')
            self.datetime_label.config(text=date_time)
            self.datetime_label.after(1000, self._update_clock)
        except Exception as e:
            logging.error(f"Error updating clock: {e}")

    def i_exit(self): 
        self.stop_face_recognition()
        if hasattr(self, 'db') and self.db:  # <--- NEW
            self.db.close() # <--- NEW
        self.root.destroy()
        logging.info("Application closed successfully")

def main():
    root = tk.Tk()
    obj = FaceRecognition(root)
    root.protocol("WM_DELETE_WINDOW", obj.i_exit)
    root.mainloop()

if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import subprocess
import time
import datetime
import mysql.connector
import cv2
import threading
import csv
import os
import logging
from typing import Optional, Tuple, Dict
import win32con
import win32gui

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FaceRecognition:
    """Face Recognition System for attendance management."""
    
    def __init__(self, root: tk.Tk):
        """Initialize the Face Recognition GUI and components."""
        self.root = root
        self.root.title("Face Recognition")
        self.root.geometry("1300x734+0+0")
        self.root.resizable(0, 0)
        
        # Try to set icon, but don't crash if it doesn't exist
        try:
            self.root.wm_iconbitmap("face.ico")
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
        
        # Attendance tracking to prevent duplicates in same session
        self.session_attendance = set()
        
        # Setup GUI
        self._setup_gui()
        
        # Load face detection models
        self._load_models()
        
        # Start clock update
        self._update_clock()

    def _setup_gui(self):
        """Setup the GUI components."""
        # Heading
        heading = tk.Label(
            self.root, 
            text="Face Recognition",
            font=('times new roman', 35, "bold"),
            bg="#cfe4fa", 
            fg="blue"
        )
        heading.place(x=0, y=0, width=1300, height=60)

        # Back button
        back_btn = tk.Button(
            self.root,
            text="Back",
            cursor="hand2",
            font=('times new roman', 20, "bold"),
            bg="#EF2A2A", 
            fg="white",
            command=self.close_application
        )
        back_btn.place(x=1180, y=12, width=100, height=35)

        # Date/Time label
        self.datetime_label = tk.Label(
            self.root, 
            text="",
            font=('times new roman', 12, "bold"),
            bg="#1060B7", 
            fg="#ffffff"
        )
        self.datetime_label.place(x=0, y=60, width=1300, height=30)

        # Main frame
        frame_box = tk.Frame(self.root, bg="#61BAEE")
        frame_box.place(x=337, y=93, width=650, height=520)
        
        # Status label inside frame
        self.status_label = tk.Label(
            frame_box,
            text="System Ready",
            font=('times new roman', 16),
            bg="#61BAEE",
            fg="white"
        )
        self.status_label.pack(pady=20)

        # Start/Stop button
        self.control_button = tk.Button(
            self.root,
            text="Start Face Detection",
            cursor="hand2",
            command=self.toggle_face_recognition,
            font=("times new roman", 20, "bold"),
            bg="#0147bf", 
            fg="#f1f1f1"
        )
        self.control_button.place(x=500, y=620, width=300, height=50)

    def _load_models(self):
        """Load face detection and recognition models."""
        try:
            # Load Haar Cascade
            cascade_path = "haarcascade_frontalface_default.xml"
            if not os.path.exists(cascade_path):
                logging.error(f"Haar cascade file not found: {cascade_path}")
                messagebox.showerror("Error", f"Haar cascade file not found: {cascade_path}")
                return False
            
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            
            # Load trained recognizer
            classifier_path = "classifier.xml"
            if not os.path.exists(classifier_path):
                logging.error(f"Classifier file not found: {classifier_path}")
                messagebox.showerror("Error", f"Classifier file not found: {classifier_path}")
                return False
            
            self.recognizer = cv2.face.LBPHFaceRecognizer_create()
            self.recognizer.read(classifier_path)
            
            logging.info("Models loaded successfully")
            return True
            
        except Exception as e:
            logging.error(f"Error loading models: {e}")
            messagebox.showerror("Error", f"Failed to load models: {e}")
            return False

    def _update_clock(self):
        """Update the date/time display."""
        date_time = time.strftime(' %B %d, %Y \t\t\t  %I:%M:%S %p on %A ')
        self.datetime_label.config(text=date_time)
        self.datetime_label.after(1000, self._update_clock)

    def toggle_face_recognition(self):
        """Toggle face recognition on/off."""
        if not self.is_running:
            self.start_face_recognition()
        else:
            self.stop_face_recognition()

    def start_face_recognition(self):
        """Start face recognition in a separate thread."""
        if not self.face_cascade or not self.recognizer:
            if not self._load_models():
                return
        
        self.is_running = True
        self.control_button.config(text="Stop Face Detection", bg="#ff4444")
        self.status_label.config(text="Face Detection Running...")
        
        # Clear session attendance for new session
        self.session_attendance.clear()
        
        # Start recognition in thread
        self.recognition_thread = threading.Thread(target=self.face_recognition_loop, daemon=True)
        self.recognition_thread.start()

    def stop_face_recognition(self):
        """Stop face recognition."""
        self.is_running = False
        self.control_button.config(text="Start Face Detection", bg="#0147bf")
        self.status_label.config(text="Face Detection Stopped")
        
        # Release video capture if it exists
        if self.video_capture:
            self.video_capture.release()
            cv2.destroyAllWindows()

    def get_student_info(self, student_id: int) -> Optional[Dict]:
        """Fetch student information from database."""
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT id, name, roll, dep, course, `div` 
                FROM face 
                WHERE id = %s
            """
            cursor.execute(query, (student_id,))
            result = cursor.fetchone()
            
            return result
            
        except mysql.connector.Error as e:
            logging.error(f"Database error: {e}")
            return None
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def mark_attendance(self, student_info: Dict) -> bool:
        """Mark attendance for a student."""
        try:
            # Check if already marked in this session
            student_id = student_info['id']
            if student_id in self.session_attendance:
                logging.info(f"Attendance already marked for ID {student_id} in this session")
                return False
            
            # Create attendance directory if it doesn't exist
            os.makedirs("attendance", exist_ok=True)
            
            attendance_file = "attendance/attendance.csv"
            
            # Check if file exists, if not create with headers
            file_exists = os.path.exists(attendance_file)
            
            with open(attendance_file, "a", newline='') as f:
                writer = csv.writer(f)
                
                # Write headers if new file
                if not file_exists:
                    writer.writerow(['ID', 'Roll', 'Name', 'Department', 'Course', 
                                   'Division', 'Time', 'Date', 'Status'])
                
                # Write attendance record
                now = time.strftime('%H:%M:%S')
                date = time.strftime('%d/%m/%Y')
                
                writer.writerow([
                    student_info['id'],
                    student_info['roll'],
                    student_info['name'],
                    student_info['dep'],
                    student_info['course'],
                    student_info['div'],
                    now,
                    date,
                    'Present'
                ])
            
            # Add to session tracking
            self.session_attendance.add(student_id)
            
            # Show success message
            self.root.after(0, lambda: messagebox.showinfo(
                "Success", 
                f"Attendance marked for {student_info['name']} (ID: {student_id})"
            ))
            
            logging.info(f"Attendance marked for {student_info['name']} (ID: {student_id})")
            return True
            
        except Exception as e:
            logging.error(f"Error marking attendance: {e}")
            return False

    def process_frame(self, img):
        """Process a single frame for face recognition."""
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray_image, 
            scaleFactor=1.1, 
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        for (x, y, w, h) in faces:
            # Draw rectangle around face
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            
            # Predict face
            face_roi = gray_image[y:y + h, x:x + w]
            student_id, confidence = self.recognizer.predict(face_roi)
            
            # Calculate confidence percentage
            confidence_percent = int(100 * (1 - confidence / 300))
            
            if confidence_percent > 77:
                # Fetch student information
                student_info = self.get_student_info(student_id)
                
                if student_info:
                    # Display student information
                    cv2.putText(img, f"ID: {student_info['id']}", 
                              (x, y - 65), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.putText(img, f"Name: {student_info['name']}", 
                              (x, y - 45), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.putText(img, f"Roll: {student_info['roll']}", 
                              (x, y - 25), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.putText(img, f"Dept: {student_info['dep']}", 
                              (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    
                    # Mark attendance
                    self.mark_attendance(student_info)
                else:
                    cv2.putText(img, "Database Error", 
                              (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
            else:
                cv2.putText(img, f"Unknown Face ({confidence_percent}%)", 
                          (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
        
        return img

    def face_recognition_loop(self):
        """Main face recognition loop."""
        try:
            # Initialize video capture
            self.video_capture = cv2.VideoCapture(0)
            
            if not self.video_capture.isOpened():
                raise Exception("Cannot open camera")
            
            # # Create window
            # cv2.namedWindow("Face Recognition", cv2.WINDOW_NORMAL)
            # cv2.resizeWindow("Face Recognition", 640, 480)
            
            # Small delay to let window appear
            time.sleep(0.5)
            
            try:
                # Get handle for OpenCV window and set always on top
                hwnd = win32gui.FindWindow(None, "Face Recognition")
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST,
                                     0, 0, 0, 0,
                                     win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            except Exception as e:
                logging.warning(f"Could not set window on top: {e}")
            
            while self.is_running:
                ret, frame = self.video_capture.read()
                
                if not ret:
                    logging.error("Failed to grab frame")
                    break
                
                # Process frame
                processed_frame = self.process_frame(frame)
                
                # Display frame
                cv2.imshow("Face Recognition", processed_frame)
                
                # Check for ESC key (27) or Enter key (13)
                key = cv2.waitKey(1) & 0xFF
                if key == 27 or key == 13:
                    break
            
        except Exception as e:
            logging.error(f"Error in face recognition loop: {e}")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Camera error: {e}"))
            
        finally:
            self.stop_face_recognition()

    def close_application(self):
        """Properly close the application."""
        self.stop_face_recognition()
        self.root.destroy()

def main():
    """Main entry point."""
    root = tk.Tk()
    app = FaceRecognition(root)
    root.protocol("WM_DELETE_WINDOW", app.close_application)
    root.mainloop()

if __name__ == "__main__":
    main()
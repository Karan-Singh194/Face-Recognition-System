import cx_Freeze
import sys
import os
import cv2  # We need this to find the haarcascade file
import mysql.connector # Ensures this is found
import deepface # Ensures this is found
import tkcalendar # Ensures this is found

# --- Set the base for the GUI application ---
base = None
if sys.platform == 'win32':
    base = "Win32GUI"  # This hides the console window on Windows

# --- Find the path to the OpenCV cascade file (the robust way) ---
cascade_file = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')

# --- List of files and folders to include in the build ---
include_files = [
    (cascade_file, 'haarcascade_frontalface_default.xml'), # The face detector
    'photos',           # The entire folder of UI images
    'face-icon.ico'     # The application icon
]

# --- List of packages to include ---
packages = [
    "tkinter",
    "mysql.connector",
    "cv2",
    "PIL",
    "deepface",
    "numpy",
    "tkcalendar"
]

# --- List of modules to explicitly include ---
includes = [
    "PIL.ImageTk",
    "login",            # Our main file
    "main_dashboard",   # Our dashboard
    "fe",               # Our face recognition app
    "face_detail",      # Our student management app (imported by main_dashboard)
    "capture_image",    # Our photo capture app (imported by main_dashboard)
    "attendance",       # Our attendance management app
    "developer"         # Our developer info app
]

# --- Executable setup ---
executables = [
    cx_Freeze.Executable(
        "login.py",
        base=base,
        icon="face-icon.ico"
    )
]

# --- Main setup configuration ---
cx_Freeze.setup(
    name="Face Recognition Attendance System",
    version="1.0",
    description="Face Recognition Automatic Attendance System using MySQL",
    options={
        "build_exe": {
            "packages": packages,
            "includes": includes,
            "include_files": include_files,
            "excludes": ["cv2.gapi"]  # <--- THIS IS THE FIX
        }
    },
    executables=executables
)
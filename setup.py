import cx_Freeze
import sys
import os 
base = None

if sys.platform == 'win32':
    base = "Win32GUI"

os.environ['TCL_LIBRARY'] = r"C:\Users\rs966\AppData\Local\Programs\Python\Python39\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\rs966\AppData\Local\Programs\Python\Python39\tcl\tk8.6"

executables = [cx_Freeze.Executable("Face_Recognition_System.py", base=base, icon="face-icon.ico")]


cx_Freeze.setup(
    name = "Facial Recognition System",
    options = {"build_exe": {"packages":["tkinter","os"], "include_files":["face-icon.ico",'tcl86t.dll','tk86t.dll', 'photos','data','database','attendance',"haarcascade_frontalface_default.xml",   # <-- add this
            "classifier.xml"]}},
    version = "1.0",
    description = "Face Recognition Automatic Attendace System ",
    executables = executables
    )

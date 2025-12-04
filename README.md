# Face Attendance System 🎓📸

A desktop-based **Face Recognition Attendance System** built with **Python, Tkinter, OpenCV, and MySQL**.  
It allows you to:

- Manage student records (department, course, year, division, contact details, etc.)
- Capture and store face images for each student
- Mark attendance automatically using face recognition
- View, filter, and manage attendance records from a modern GUI
- Maintain developer/contact details inside the app

---

## 🧰 Tech Stack

- **Language:** Python
- **GUI:** Tkinter
- **Database:** MySQL (`face_system` schema)
- **Computer Vision:** OpenCV (Haar Cascade for face detection)
- **Image Handling:** Pillow (PIL)
- **Calendar Widget:** tkcalendar
- **Others:** `mysql-connector-python`, `numpy`, `csv`, `logging`, `threading`

---

## 📁 Project Structure

```text
Face Attendance System/
├── attendance.py          # Attendance management UI + DB layer for attendance_records
├── capture_image.py       # Capture & save student face images from webcam
├── developer.py           # "Developer / Contact" information window
├── face_detail.py         # Student details management (CRUD on 'face' table)
├── fe.py                  # FaceRecognition: main face recognition + attendance logic
├── login.py               # Login screen and entry point for the app
├── main_dashboard.py      # Main admin dashboard (navigation to all modules)
├── photos/                # UI images (backgrounds, icons, buttons, etc.)
│   ├── attendance.png
│   ├── bg1.png
│   ├── bg2.png
│   ├── ...
│   └── total_emp.png
└── student_images/        # Sample/Stored face images & model files
    ├── 9_SRK.jpg
    ├── 10_Amir_Khan.jpg
    ├── 11_Akshay_Kumar.jpg
    ├── 12_Amitab_Bachchan.jpg
    └── ds_model_vggface_detector_opencv_aligned_normalization_base_expand_0.pkl (model file)
```
## ✨ Main Features

### 🔐 1. Secure Login
- Login screen (`login.py`) with username & password.
- Connects to MySQL (default DB: `face_system`).
- On successful login, the **Admin Dashboard** opens automatically.
 ![screenshot](login.png)


---

### 🖥️ 2. Admin Dashboard (`main_dashboard.py`)
A central control hub providing access to all system modules:

- 👨‍🎓 **Student Details** (`face_detail.py`)
- 🤖 **Face Recognition / Attendance** (`fe.py`)
- 📸 **Photo Capture** (`capture_image.py`)
- 📊 **Attendance Management** (`attendance.py`)
- 👤 **Developer / Contact Info** (`developer.py`)
  ![screenshot](main.png)

All navigation buttons use images from the `photos/` folder and open modules in separate windows.

---

### 📚 3. Student Management (`face_detail.py`)
Manage complete student information stored in the `face` table.

**Features include:**
- ➕ Add, ✏️ Update, ❌ Delete student entries.
- Student fields:
  - Department, Course, Year, Semester  
  - Student ID, Name, Division, Roll No.  
  - Gender, Date of Birth  
  - Email, Phone, Address  
  - Photo Status (Yes/No)
- 🔍 Multi-field search functionality.
- 🗂️ Data displayed using Tkinter **Treeview** table.
- 📅 Date picker using **tkcalendar.DateEntry**.
- 🗃️ All DB operations managed via a **DatabaseManager** helper class.
![screenshot](detail.png)
---

### 📸 4. Photo Capture (`capture_image.py`)
Capture clear face images for training the system.

**Includes:**
- 🎥 Webcam access via OpenCV.
- 😀 Face detection using:
  - `haarcascade_frontalface_default.xml`
- 💾 Saves captured images to the `student_images/` folder.
- 🔄 Updates `photo` field in the database (No → Yes).
![screenshot](capture.png)
---

### 🤖 5. Face Recognition & Auto Attendance (`fe.py`)
Real-time face recognition + automated attendance logging.

**How it works:**
- Loads known student images from `student_images/`.
- Detects & recognizes faces using computer vision.
- On recognition:
  - Retrieves student info from DB.
  - Inserts or updates attendance in `attendance_records`.
  - Avoids repeated marking with a **cooldown system**.
![screenshot](fe.png)

**UI Displays:**
- 🎥 Live camera feed  
- 🟢 Recognition status  
- ✔️ Attendance success message  

Uses **threading** for smooth UI + camera operations.

---

### 📊 6. Attendance Management (`attendance.py`)
Complete attendance record management system.

**Features:**
- 📄 View all attendance logs.
- 🔍 Search & filter (by date, student, etc.).
- ✏️ Update attendance status (Present / Absent / Late).
- 🗑️ Delete attendance entries.
- 📤 Export / 📥 Import attendance using CSV.
- 🗃️ Powered by **DatabaseManager** for SQL operations.
![screenshot](attendance.png)
---

### 👤 7. Developer / Contact Info (`developer.py`)
Provides a simple information page with:

- 🧑‍💻 Developer name (e.g., **Karan Singh**)
- 📝 Short bio or project details
- 🔗 Optional links (GitHub, LinkedIn, Email, etc.)
![screenshot](developer.png)
---

## 🗄️ Database Setup (MySQL)

By default, the application connects to MySQL using:

```python
mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="face_system"
)
```

### 🔧 1. Create the Database

```MYSQL 
CREATE DATABASE face_system;
USE face_system;

```
### 🧱 2. Create Required Tables

Below are example table schemas based on how the system uses the database.
You may modify sizes/types as needed.

```🧍‍♂️ face – Student Details Table
CREATE TABLE face (
    id INT PRIMARY KEY,
    dep        VARCHAR(100),
    course     VARCHAR(100),
    year       VARCHAR(20),
    sem        VARCHAR(20),
    name       VARCHAR(100),
    `div`      VARCHAR(10),
    roll       VARCHAR(50),
    gender     VARCHAR(20),
    dob        DATE,
    email      VARCHAR(100),
    phone      VARCHAR(20),
    address    VARCHAR(255),
    photo      ENUM('Yes','No') DEFAULT 'No'
);

```

```📊 attendance_records – Attendance Logs Table
CREATE TABLE attendance_records (
    record_id         INT AUTO_INCREMENT PRIMARY KEY,
    student_id        INT NOT NULL,
    attendance_date   DATE NOT NULL,
    attendance_time   TIME NOT NULL,
    attendance_status ENUM('Present', 'Absent', 'Late') DEFAULT 'Present',
    
    CONSTRAINT fk_attendance_student
        FOREIGN KEY (student_id) REFERENCES face(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
```

### ⚙️ Installation & Setup
🧩 1. Clone the Repository
```
git clone https://github.com/<your-username>/<your-repo-name>.git
cd "<your-repo-name>/Face Attendance System"

```

### 💻 2. Create & Activate Virtual Environment (Recommended)
```
python -m venv venv

Windows:
venv\Scripts\activate

Linux/Mac:
source venv/bin/activate
```
### 📦 3. Install Dependencies

```Your requirements.txt should include:
opencv-python
Pillow
mysql-connector-python
tkcalendar
numpy

pip install -r requirements.txt
```

### 🗃️ 4. Configure MySQL Database

Ensure MySQL server is running.
Create the face_system database and tables (SQL above).
Update the database credentials in your Python files if necessary.

### 📁 5. Ensure Required Folders Exist

These folders must be present:
```
photos/          → UI images & icons  
student_images/  → Captured student face images  
```

## ▶️ Running the Application

Navigate inside the Face Attendance System folder:
```
python login.py
```
### 📌 Application Flow

- Login with valid MySQL user credentials.
- Access the Admin Dashboard.
- Add student details via Face Detail module.
- Capture student images using Photo Capture.
- Start Face Recognition to auto-mark attendance.
- Review and manage records through Attendance Management.


### 🧪 Sample Data

The student_images/ folder includes example images:

- **9_SRK.jpg**
- **10_Amir_Khan.jpg**
- **11_Akshay_Kumar.jpg**
- **12_Amitab_Bachchan.jpg**

🚀 Possible Improvements

Here are some enhancements you can add in the future:

- **Upgrade Haar Cascade → Deep Learning face recognition (e.g., FaceNet, Dlib, InsightFace)**
- **Add role-based access:**
- **Admin / Teacher / Student**
- **Generate attendance analytics (daily, monthly, student reports)**
- **Move DB credentials to a separate configurable file**
- **Add support for multiple webcams or IP cameras**

## 🙋‍♂️ Author

Karan Singh
B-Tech IT – Face Recognition Attendance System

Feel free to open issues or pull requests to improve the project!

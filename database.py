from tkinter import *
from tkinter import messagebox
import pymysql


def create_database_table():
    cursor,connection=connect_database()
    cursor.execute("CREATE DATABASE IF NOT EXISTS face_system")
    cursor.execute("USE face_system")
    cursor.execute("CREATE Table IF NOT EXISTS employee_data (empid INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), "
                   "gender  VARCHAR(50), dob  VARCHAR(30), contact  VARCHAR(30), employment_type  VARCHAR(50),education VARCHAR(50),"
                   " work_shift  VARCHAR(50),address  VARCHAR(100), doj  VARCHAR(50), salary  VARCHAR(50), user_type  VARCHAR(50),"
                    " password  VARCHAR(50))" )
    
def connect_database():
    try:
        connection=pymysql.connect(host="localhost", user="root", password="1234")
        cursor = connection.cursor()
    except:
        messagebox.showerror('Error', 'Database connectivity issue , open mysql command line client')
        return None, None

    return cursor,connection

create_database_table()
connect_database()
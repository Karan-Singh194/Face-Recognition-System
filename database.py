import mysql.connector
import pymysql
from tkinter import messagebox




def connect_database():
    try:
        connection=pymysql.connect(host="localhost", user="root", password="1234")
        cursor = connection.cursor()
    except:
        messagebox.showerror('Error', 'Database connectivity issue , open mysql command line client')
        return None, None

    return cursor,connection
    
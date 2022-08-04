import tkinter as tk
from tkinter import *
from tkinter import StringVar
from tkinter import messagebox
import mysql.connector
import time

frame = tk.Tk()
frame.geometry("500x500")
frame.title("Email Sender ")
frame.config(background = "Slateblue")
frame.focus_force()
frame.pack_propagate(0)

def open_frame():
    if var.get() == "Upload CSV File":
        frame.destroy()
        import Bulkemail_Csvupload
    elif var.get() == "Enter Email Addresses Manually":
        frame.destroy()
        import Bulkemail_enterManually
    elif var.get() == "Show Recent Details":
        frame.destroy()
        import recent_details
    else:
        messagebox.showwarning(title = "Warning!" , message = "Please Choose an Option First!")

def close_frame():
    exit = messagebox.askyesno(title = "STATUS" , message = "Are You Sure You Want To Exit?")
    if exit == True:
        try:
            connection = mysql.connector.connect(
                host = "localhost" , 
                user = "root" , 
                password = "123456"  , 
                database = "email_client"
            )

            mycursor = connection.cursor()

            sql = "DELETE FROM admin_details"
            mycursor.execute(sql)

            connection.commit()
        except mysql.connector.Error as err:
            messagebox.showerror(title = "STATUS" , message = err)
        finally:
            if connection.is_connected():
                mycursor.close()
                connection.close()
        time.sleep(2)
        frame.destroy()

l = tk.Label(frame , text = "Please Select an Option To Send Email: " , background="blue")
l.place(x=150 , y=150)

options  = ["Upload CSV File" ,  "Enter Email Addresses Manually" , "Show Recent Details"]
var = StringVar(frame)
var.set("Please Select An Option")

# global list
list = tk.OptionMenu(frame , var , *options)
list.place(x=170 , y=200)

b = tk.Button(frame , text = "OPEN" , command = open_frame)
b.place(width = 100 , x=200 , y=300)





frame.protocol('WM_DELETE_WINDOW' , close_frame)
frame.mainloop()
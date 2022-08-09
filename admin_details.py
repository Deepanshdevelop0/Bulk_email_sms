from configparser import Error
import tkinter as tk
import mysql.connector
from tkinter import messagebox
from tkinter import *
import mysql.connector
import time
import smtplib , ssl

frame = tk.Tk()
frame.geometry("1000x600")
frame.title("Admin Details")
frame.configure(bg = "#9f3ae7")
canvas = Canvas(
    frame,
    bg = "#9f3ae7",
    height = 600,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    500.0, 300.0,
    image=background_img)
frame.focus_force()
frame.pack_propagate(0)

def mysql_connection(admin_email , admin_password):
    # print(admin_email , admin_password)
    try:
        connection = mysql.connector.connect(
            host = "localhost" ,
            user = "root" ,
            password = "123456" ,
            database = "email_client"
        )

        mycursor = connection.cursor()

        sql = "INSERT INTO admin_details(email_address , password) VALUES (%s , %s)"
        val = (admin_email , admin_password)
        mycursor.execute(sql , val)
        connection.commit()
        mysql_connection.connection_bool = True

    except mysql.connector.Error as error:
        messagebox.showerror(title = "SOMETHING WENT WRONG!" , message = "Couldn't Store Data :".format(error))
    finally:
        # print(mycursor.rowcount , "Record Inserted!")
        if connection.is_connected():
            mycursor.close()
            connection.close()

def mysql_connection1(sql):
    try:
        connection = mysql.connector.connect(
            host = "localhost" , 
            user = "root" , 
            password = "123456" , 
            database = "email_client"
        )

        mycursor = connection.cursor()

        mycursor.execute(sql)

        connection.commit()
    except mysql.connector.Error as err:
        messagebox.showwarning(title = "WARNING" , message = err)

    finally:
        if connection.is_connected():
            mycursor.close()
            connection.close()



def login():
    admin_email = enter_email_entry.get()
    admin_password = enter_password_entry.get()
    log = False
    if admin_email.endswith("@gmail.com") and len(admin_password) != 0:
            
            server = "smtp.gmail.com"
            port = 465
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL(server , port , context = context) as Server:
                try:
                    Server.login(admin_email , admin_password)
                    log = True
                except :
                    messagebox.showwarning(title = "SOMETHING WENT WRONG" , message = " Incorect Email Address Or Password ! \n Please Check it Once again .")
            if (log == True):
                mysql_connection(admin_email , admin_password)
                if mysql_connection.connection_bool == True:
                    messagebox.showinfo(title = "STATUS" , message = "Email Address and Password Stored Successfully!")
                    time.sleep(5)
                    frame.destroy()
                    import Emailmainframe
    else:
        messagebox.showwarning(title = "WARNING" , message = "Please Enter Valid Email Address And Password")


def close_frame():
    exit = messagebox.askyesno(title = "STATUS" , message = "Are You Sure You Want To Exit?")
    if exit == True:
        sql = "DELETE FROM admin_details"
        mysql_connection1(sql)
        messagebox.showinfo(title = "STATUS" , message = "Press OK To Exit.....")
        time.sleep(2)
        frame.destroy()
    else:
        pass


def show_password():
    if (enter_password_entry.cget('show') == '*'):
        enter_password_entry.config(show = '')
    else:
        enter_password_entry.config(show = "*")


enter_email_entry = tk.Entry(frame , bd = 2 , fg = "black" , highlightthickness= 1 , highlightbackground= "#884dff")
enter_email_entry.place(width = 200 , x=560 , y=272)
enter_password_entry = tk.Entry(frame , bd = 2 , fg = "black" , highlightthickness= 1 , highlightbackground= "#884dff" , show = "*")
enter_password_entry.place(width = 200 , x=560 , y=368)
login = tk.Button(frame , text = "LOGIN" , bd = 1 , highlightthickness= 1 , highlightbackground= "#110033" , background = "#aa80ff" , command = login)
login.place(width = 100 , x=610 , y=440)
check_button = tk.Checkbutton(frame , text = "Show Password" ,  command = show_password)
check_button.place(width = 100 , x = 660 , y = 392)
# icon_image = tk.PhotoImage(file = r"contact_number12.png")
# label = tk.Label(frame , bd = 2 , image=icon_image, highlightthickness= 1)
# label.place(height = 20 , width = 28 , x= 770 , y = 271)



frame.protocol('WM_DELETE_WINDOW' , close_frame)
frame.mainloop()
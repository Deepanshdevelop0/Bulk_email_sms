import tkinter as tk
from tkinter.constants import END
from tkinter import messagebox
import mysql.connector
import time

show = tk.Tk()

show.geometry('1000x1000')
show.config(background = "slateblue" )
show.title("STORED EMAIL ADDRESSES")
show.focus_force()
show.pack_propagate(0)  


def mysql_connection(sql , val):
    try: 
        connection = mysql.connector.connect(
            host = "localhost" , 
            user = "root" , 
            password = "123456" , 
            database = "email_client"
        )

        mycursor = connection.cursor()

        mycursor.execute(sql , val)
        connection.commit()
    except mysql.connector.Error as err:
        messagebox.showerror(title = "STATUS" , message = err)
        mysql_connection.error = err

    finally:
        if connection.is_connected():
            mycursor.close()
            connection.close()
            mysql_connection.connection_bool = True

def mysql_selection(sql):
    connection = mysql.connector.connect(
        host = "localhost" , 
        user = "root" , 
        password = "123456" , 
        database = "email_client"
    )

    mycursor = connection.cursor()

    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    return myresult


def change_Email():
    e = enter_key.get()
    e1 = change_email.get()
    if "@gmail.com" not in e1 or len(e) == 0:
        if len(e) == 0 and len(e1) == 0:
            messagebox.showerror(title = "SOMETHING WENT WRONG" , message = "Please Enter Index of Email Address And New Email Address To Change Email Address!")
            # print("working")
        elif len(e) == 0:
            messagebox.showerror(title = "SOMETHING WENT WRONG" , message = "Please Enter New Email Address To Change!")
            # print("working1")
        elif len(e1) == 0:
            messagebox.showerror(title = "SOMETHING WENT WRONG" , message = "Please Enter Index of Email Address And New Email Address To Change Email Address!")
            # print("working1")
        else:
            messagebox.showerror(title = "SOMETHING WENT WRONG" , message = "Please Enter Valid Email Address")
    else:
        # a=int(enter_key.get())
        # b=change_email.get()
        # list[e]=e1
        key = int(e)
        # print("show")
        sql = "UPDATE bulkemail_entermanually SET email_list = %s WHERE id = %s"
        val = (e1 , key)
        mysql_connection(sql , val)
        
        if mysql_connection.connection_bool == True:
            messagebox.showinfo("showinfo" , "Email Changed Successfully!")
        else:
            messagebox.showinfo(title = "SOMETHING WENT WRONG!" , message = mysql_connection.error)
        # enter_key.config(text = " ")
        # change_email.config(text = " ")
        show.focus_force()
    
def show_email():
    text_box.configure(state = "normal")
    sql = "SELECT email_list FROM bulkemail_entermanually"
    list = mysql_selection(sql)
    # print(list) 
    for i in range(len(list)):
        for j in range(len(list[i])):
            # print(i ,j)
            if i<10:
                text_box.insert(END , i+1 )
                text_box.insert(END , "  |\t\t")
                text_box.insert(END , list[i][j])
                text_box.insert(END , "\n")


            else:
                text_box.insert(END , i+1)
                text_box.insert(END , " |\t\t")
                text_box.insert(END , list[i])
                text_box.insert(END , "\n")
            text_box.insert(END , "   |\t\t\n")

    text_box.clipboard_clear()
    text_box.configure(state="disabled")

def refresh():
    text_box.configure(state = "normal")
    text_box.delete('1.0' , 'end')
    show_email()
    
def back():
    show.destroy()
    import Emailmainframe
    


text_box = tk.Text(show , bd = 10 , background = "black" , fg = "white")
text_box.place(x=200 , y=50)
change = tk.Button(show , text = "Change Email", bd = 3 , fg="blue" , command = change_Email)
change.place(width = 100 , x=370 , y=700)
enter_key = tk.Entry(show , bd=2 , highlightbackground="red")
enter_key.place(height = 30 , width = 200 , x=600 , y=550)
l = tk.Label(show , text = "Enter Index of List \n To Change" , bd=2)
l.place(height = 30 , width = 150 , x=420 , y=550)
l1 = tk.Label(show , text = "Enter New Email Address ")
l1.place(height = 30 , width = 150 , x=420 , y=600)
change_email = tk.Entry(show , bd=2 , highlightbackground="red")
change_email.place(height = 30 , width = 200 , x=600 , y=600)
next = tk.Button(show , text = "Back To Main Page" , fg="Blue" , bd = 3 , command = back)
next.place(width = 150 , x=510 , y=700)
label = tk.Label(show , text = "To Modify\nEmail Addresses :" , background = "blue")
label.place(width = 150 , x=200 , y=550)
show_email_button = tk.Button(show , text = "SHOW EMAILS" , bd = 3 , command = show_email)
show_email_button.place(width = 150 , x=530 , y=460)
refresh_btn = tk.Button(show , text = "REFRESH" , bd = 3 , command = refresh)
refresh_btn.place(width = 150 , x=350 , y=460)
text_box.configure(state = "disabled")

show.resizable(False, False)
show.mainloop()

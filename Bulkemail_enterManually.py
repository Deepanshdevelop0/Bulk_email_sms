import smtplib , ssl
import tkinter as tk
from types import NoneType
import pandas as pd
from tkinter import filedialog as fd
import mysql.connector
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from tkinter import messagebox
import os
import time
from datetime import datetime

frame = tk.Tk()
frame.geometry('1000x1000')
frame.config(background = "slateblue")
frame.title("Bulk Email Client")
frame.focus_force()
frame.pack_propagate(0)
# photo = tk.PhotoImage(file = "bulk_email_service.png")
# frame.iconphoto(False , photo)
messagebox.showinfo(title = "Important Message!" , message = "Please Click Next After Entering Every Email Address ,\nAnd After Finished Entering Email Addresses Click Finish!\n-------------------------------------------------------------------------\n\t     Now, You Are All Set To Go!")

# global name_list 
name_list = []
name_list1 = []

msg = MIMEMultipart()

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
        mysql_connection.connection_bool = True

    except mysql.connector.Error as err:
        messagebox.showerror(title = "SOMETHING WENT WRONG!" , message = err)
        mysql_connection.error = 1
    finally:
        if connection.is_connected():
            mycursor.close()
            connection.close()    # Closing the connection after executing the query

def mysql_selection(sql):
    try:
        connection = mysql.connector.connect(
        host = "localhost" , 
        user = "root" , 
        password = "123456" , 
        database = "email_client"
        )

        mycursor = connection.cursor()

        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        
        for i in myresult:
            # print(i)
            return i   
        

    except mysql.connector.Error as err:
        messagebox.showerror(title = "SOMETHING WENT WRONG!" , message = err)
    finally:
        if connection.is_connected():
            mycursor.close()
            connection.close()    # Closing The Connection
            
def mysql_selection1(sql):

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
        messagebox.showerror(title = "STATUS" , message = err)
    finally:
        if connection.is_connected():
            mycursor.close()
            connection.close()    # Closing the connection
global i
i = 0
def id():
    global i
    i+=1
    return i

def next():
    # makes the variable global and prevents the error 'variable refrenced before assignment'
    name = e.get()
    # if "," in name:
    #     name1 = name.split(",")
    #     name2 = name1[0]
    # else:
    #     name2 = name 
    global name_list1
    if "@gmail.com" in name:
        if "," in name:
            messagebox.showinfo(title = "STATUS" , message = "Please Enter Single Email Address!")
        elif ";" in name:
            messagebox.showinfo(title = "STATUS" , message = "Please Enter Single Email Address!")
        else:
            name_list.append(name)
            name_list1.append(name)
            e.delete(0 , 'end')
            status_entry.config(text = "Email Address Added Successfully!")
    else:
        status_entry.config(text = "Please Enter Valid Email Address!")
    # print(name_list1)
    
    
    

def finish():
    for i in range(len(name_list)):   
        sql = "INSERT INTO bulkemail_entermanually(id , email_list , date , time) VALUES (%s , %s , %s , %s)"
        id1 = id()
        # print(id1)
        current_time = datetime.now()
        # date = current_time.strftime("%d-%m-%Y")
        time = current_time.strftime("%H:%M:%S")
        # print(date)
        val = (id1 , name_list[i] , current_time , time)
        mysql_connection(sql , val)
        sql2 = "SELECT email_address FROM admin_details"
        email_address = mysql_selection(sql2)
        if email_address is None:
            messagebox.showerror(title = "SOMETHING WENT WRONG" , message = "Couldn't Found Admin Details")
        elif email_address is not None:
            sender_email = email_address[0]

            sql3 = "SELECT id FROM recent_details"
            val3 = mysql_selection1(sql3)     
            if val3 is None:
                val1 = ("1" , "" , current_time  , time , name_list[i])
            elif val3 is not None:
                length = len(val3)
                if length == 0:
                    val1 = ("1" , sender_email , current_time  , time , name_list[i])
                else:
                    index = val3[length - 1][0]
                    val1 = (index , sender_email , current_time  , time , name_list[i])
            else:
                messagebox.showerror(title = "WARNING" , message = "SOMETHING WENT WRONG!")
            sql1 = "INSERT INTO recent_details(id , admin_email , date , time , sent_to) VALUES (%s , %s , %s , %s , %s)"

            mysql_connection(sql1 , val1)
        else:
            messagebox.showerror(title = "WARNING" , message = "SOMETHING WENT WRONG!")
        
        
        # print("working 1")
    name_list[:] = []
   

def attach_file():
    file = fd.askopenfilenames()
    # path = f.name
    if file is not None:
        file_path = list(file)
        a = []
        for i in range(len(file_path)):
            a.append(os.path.getsize(file_path[i]))
            # print(a)
            if((a[i]) > 1.6e+7):
                messagebox.showwarning(title = "WARNING!" , message = "File Selected Is Too Large ! \nPlease Attach File Under 16MB")
            else:
                attach_files = open(file_path[i] , 'rb')
                attach_file = attach_files.read()
                
                sql = "INSERT INTO bulkemail_attachment (id , attachment) VALUES (%s , %s)"
                val = (i+1 , attach_file)
                mysql_connection(sql , val)

                if(mysql_connection.connection_bool == True):
                    messagebox.showinfo(title = "STATUS" , message = "File Uploaded Successfully !")

                    sql = "SELECT attachment FROM bulkemail_attachment"
                    attachment_file = mysql_selection1(sql)

                    for f in file_path:
                        # print("1")
                        attachment_file_name = f
                        attachment_file_name1 = attachment_file_name.split('/')    # spliting the attached file and extracting only file name
                        # print(list)
                        # print(attachment_file_name1[len(attachment_file_name1)-1])
                        try:
                            attachment_file1 = attachment_file[1][0]
                        except IndexError as err:
                            messagebox.showinfo(title = "SOMETHING WENT WRONG" , message = "Please Attach Files Once Again!")

                        payload = MIMEBase("application" , "octate-stream" , Name = attachment_file_name1[len(attachment_file_name1)-1])
                        payload.set_payload(attachment_file1)
                        encoders.encode_base64(payload)
                        payload.add_header("Content-Decomposition" , "attachment")
                        msg.attach(payload)



def back():
    # frame.quit()
    # exit()
    frame.destroy()
    import Emailmainframe
    sql4 = "DELETE FROM bulkemail_entermanually"
    mysql_connection1(sql4)


def index():
    sql3 = "SELECT id FROM recent_details"
    val3 = mysql_selection1(sql3)     
    if val3 is None:
        messagebox.showerror(title = "WARNING" , message = "No Record Found In Database")
    elif val3 is not None:
        length = len(val3)
        if length == 0:
            val1 = ("1")
        else:
            index = val3[length - 1][0] + 1
            val1 = (index)
    else:
        messagebox.showerror(title = "WARNING" , message = "SOMETHING WENT WRONG!")

    sql1 = "INSERT INTO recent_details(id , sent_to) VALUES (%s , %s)"
    val2 = (val1 , "")
    mysql_connection(sql1 , val2)

def send():
    server = "smtp.gmail.com"
    port = 465
    sql = "SELECT email_address FROM admin_details"
    email_address = mysql_selection(sql)
    if email_address is not None:
        sender_email = email_address[0]
    # print(sender_email)
    sql1 = "SELECT password FROM admin_details" 
    admin_password = mysql_selection(sql1)
    if admin_password is not None:
        sender_password = admin_password[0]
    # print(sender_password)

    message = msg_text.get("1.0" , 'end')  # "1.0" means read from the line one and character zero and 'end' means read till end of the text box
    
    msg['From'] = email_address[0]
    msg['To'] = ','.join(name_list1)
    msg['Subject'] = (subject_entry.get())
    msg.attach(MIMEText(message , 'plain'))
    
    text = msg.as_string()

    
    
    # Create a secured SSL Context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(server , port , context=context) as Server:
        Server.login(sender_email , sender_password)
        Server.sendmail(sender_email , name_list1 , text)
        status_entry.config(text = "Email Sent Successfully!")

    index()

def show_Email():
    import Show_Email

def close_frame():
   
    exit = messagebox.askyesno(title = "STATUS" , message = "Are You Sure You Want To Exit?")
    if exit == True:
        a = messagebox.showinfo(title = "STATUS" , message = "Press Ok to Exit In 5 Seconds.....")
        sql = "DELETE FROM bulkemail_entermanually"
        mysql_connection1(sql)
        sql1 = "DELETE FROM admin_details"
        mysql_connection1(sql1)
        time.sleep(5)
        frame.destroy()
    else:
        pass



    

l = tk.Label(frame , text = "Enter Email Addresses \n Manually and Click \n'NEXT' to Enter Next Email\n Address: :" , background="blue" , bd=0)
l.place(width = 150 , x = 100 , y = 100)
e = tk.Entry(frame , bd=2)
e.place(height = 50 , width = 400 , x=300 , y=100)
btn = tk.Button(frame , text = "NEXT" , width = 10 , command = next)
btn.place(x = 530 , y = 160)
status = tk.Label(frame , text = "STATUS" , bd = 5 , background="blue")
status.place(width = 150 , x=100 , y = 620)
status_entry = tk.Label(frame , bd = 5 , width = 40)
status_entry.place(x=300 , y=620)
finish = tk.Button(frame , text = "FINISH" , width = 10 , command = finish)
finish.place(x=620 , y=160)
subject_label = tk.Label(frame , text = "Enter Subject" , background = "blue")
subject_label.place(height = 30 , width = 150 , x=100 , y=210)
subject_entry = tk.Entry(frame , bd=2)
subject_entry.place(height = 30 , width = 600 , x=300 , y=210)
message_label = tk.Label(frame , text = "Enter \n Message" , background="blue" , bd=0)
message_label.place(width = 150 , x=100 , y=260)
msg_text = tk.Text(frame , bd = 2)
msg_text.place(height = 200  , width = 600 , x=300 , y=260)
show = tk.Button(frame , text = "Show Email Addresses" , command = show_Email)
show.place(width = 150 , x=350 , y=520)
send = tk.Button(frame , text = "SEND" , command = send)
send.place(width = 100 , x=520 , y=520)
back = tk.Button(frame , text = "BACK" , command = back)
back.place(width = 100 , x=640 , y=520)
photo = tk.PhotoImage(file = r"C:\Users\Deepanshu\OneDrive\Documents\Email_Sender\Email_smtp\attachment11.png")
add_attachment = tk.Button(frame , text = "Add Attachment" , background="red" ,  image = photo , command = attach_file)
add_attachment.place(height = 30 , width = 30 , x=870 , y=465)




frame.protocol("WM_DELETE_WINDOW" , close_frame)

frame.mainloop()
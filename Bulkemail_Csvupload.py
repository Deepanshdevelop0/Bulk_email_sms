from errno import errorcode
from http import HTTPStatus
import tkinter as tk
from flask import Response
import pandas as pd
from tkinter import Canvas, filedialog as fd
from tkinter import messagebox
import smtplib,ssl
import time
import mysql.connector
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import speech_recognition as sr

frame = tk.Tk()
frame.geometry('1000x1000')
frame.config(background="slateblue")
frame.title("Bulk Email Client")
frame.focus_force()
frame.pack_propagate(0)

messagebox.showinfo(title="Important Message!", message='''   Please Note that The File You Are Selecting To Attach,\nShould Have the Email Addresses Column With Column \t\t\t\t  Heading as\n\t\t     "Emails"\n\t----------------------------------------------\n\n\t\tIf Already Done!\n\t            You Are All Set To Go ''')

msg = MIMEMultipart()

def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def mysql_connection(sql, val):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="email_client"
        )

        mycursor = connection.cursor()

        # Retrieve the Values sql and val from function attach_file
        mycursor.execute(sql, val)
        connection.commit()
    except mysql.connector.Error as error:
        messagebox.showerror(title="SOMETHING WENT WRONG!", message=error)
    finally:
        if connection.is_connected():
            mycursor.close()    # Closing the Connection
            connection.close()
            mysql_connection.connection_bool = True

def mysql_connection1(sql):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="email_client"
        )

        mycursor = connection.cursor()

        # Retrieve the Values sql and val from function attach_file
        mycursor.execute(sql)
        connection.commit()
    except mysql.connector.Error as error:
        messagebox.showerror(title="SOMETHING WENT WRONG!", message=error)
    finally:
        if connection.is_connected():
            mycursor.close()    # Closing the Connection
            connection.close()
            


def mysql_selection(sql):
    connection = mysql.connector.connect(
        host="localhost",
        username="root",
        password="123456",
        database="email_client"
    )

    mycursor = connection.cursor()

    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for i in myresult:
        # print(i)
        return i


def mysql_selection1(sql):
    connection = mysql.connector.connect(
        host="localhost",
        username="root",
        password="123456",
        database="email_client"
    )

    mycursor = connection.cursor()

    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    # for i in myresult:
    #     # print(i)
    #     return i
    return myresult


def attach_file():
    global email_list
    email_list = []
    i = 0
    a = i
    try:
        f = fd.askopenfile(title="Select File To Upload", filetypes=(
            ('Excel File', ('*.xlsx', '*.xls')), ('Csv File', '*.csv')))
        if f is not None:
            # Convert File path To String
            path = f.name
            if(path.endswith(".csv")):
                dframe = pd.read_csv(path)
                # Creating a list of Email Addresses taken from csv file given By User
                email_list = dframe['Emails'].tolist()
                # print(email_list)
                # print(dframe)
            elif(path.endswith(".xlsx") or path.endswith(".xls")):
                dframe1 = pd.read_excel(path)
                # Creating a list of Email Addresses taken from Excel file given by User
                email_list = dframe1['Emails'].tolist()
            else:
                status_lbl1.config("Please Select Valid File!")
            
            b = a+1
            # Convert Email File To Binary Data To Store In Database
            email_file = convertToBinaryData(path)

            # Insert Query For Database with Function mysql_connection
            # Passing Query to mysql_connection to Insert Email file in Database
            sql = "INSERT INTO bulkemail_csvupload(id , email_file) VALUES (%s , %s)"
            # Passing index and Email Addresses list to mysql_connection function
            val = (b, email_file)
            mysql_connection(sql, val)    # Calling Function
            if (mysql_connection.connection_bool == True):
                messagebox.showinfo(
                title="STATUS", message="File Uploaded Successfully!")

        else:
            status_lbl1.config(text="Please Select A File!")
    except ValueError:
        status_lbl1.config(text="Please Select A Valid File Type!")
    except FileNotFoundError:
        status_lbl1.config(text="File Not Found!")
    


global file_attached
file_attached = False

global i
i = 0
def id():
    global i
    i+=1
    return i


global file
def attach_attachment():
    # file = fd.askopenfile(title = "Select File To Add" , filetypes = (('All Types' , '*.*') , ('Word File' , '*.docx')))
    file = fd.askopenfilenames()
    ind = 0
    if file is not None:
        global file_path
        file_path = list(file)
        # print(file_path)
        a = []
        for i in range(len(file_path)):
            a.append(os.path.getsize(file_path[i]))
            # print(a)
            if ((a[i]) > 1.6e+7):
                messagebox.showwarning(
                    title="Warning!", message="File Selected Is Too Large !\nPLease Attach File Under 16MB")
            else:
                # attach_file = convertToBinaryData(file_path[i])
                attach_files= open(file_path[i] , 'rb')
                attach_file = attach_files.read()
                
                id1 = id()
                sql = "INSERT INTO bulkemail_attachment(id , attachment) VALUES (%s , %s)"
                val = (id1, attach_file)
                mysql_connection(sql, val)
                # file_attached = True
                if (mysql_connection.connection_bool == True):
                    messagebox.showinfo(
                    title="STATUS", message="File Uploaded Successfully!")

                sql = "SELECT attachment FROM bulkemail_attachment"
                binary_file = mysql_selection1(sql)

                for f in file_path:
                    # print("1")
                    attachment_file_name = f
                    attachment_file_name1 = attachment_file_name.split('/')    # spliting the attached file and extracting only file name
                    try:
                        attach_file = binary_file[1][0]
                        ind = 1
                    except IndexError as err:
                        # messagebox.showerror(title = "Something Went Wrong" , message = err)
                        pass
                    if (ind == 1):
                        payload = MIMEBase("application" , "octate-stream" , Name = attachment_file_name1[len(attachment_file_name1)-1])
                        payload.set_payload(attach_file)
                        encoders.encode_base64(payload)
                        payload.add_header("Content-Decomposition" , "attachment")
                        msg.attach(payload)
                        ind = 0


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
            index1 = val3[length - 1][0] + 1
            val1 = (index1)
    else:
        messagebox.showerror(title = "WARNING" , message = "SOMETHING WENT WRONG!")

    sql1 = "INSERT INTO recent_details(id , sent_to) VALUES (%s , %s)"
    val2 = (val1 , "")
    mysql_connection(sql1 , val2)

def recent_details():
    current_time = datetime.now()
    time = current_time.strftime("%H:%M:%S")
    sql2 = "SELECT email_address FROM admin_details"
    email_address = mysql_selection(sql2)
    if email_address is None:
        messagebox.showerror(title = "SOMETHING WENT WRONG" , message = "Couldn't Found Admin Details")
    elif email_address is not None:
        sender_email = email_address[0]
        sql3 = "SELECT id FROM recent_details"
        val3 = mysql_selection1(sql3)
        for i in range(len(email_list)):     
            if val3 is None:
                val1 = ("1" , "" , current_time  , time , email_list[i])
            elif val3 is not None:
                length = len(val3)
                if length == 0:
                    val1 = ("1" , sender_email , current_time  , time , email_list[i])
                else:
                    index = val3[length - 1][0]
                    val1 = (index , sender_email , current_time  , time , email_list[i])
            else:
                messagebox.showerror(title = "WARNING" , message = "SOMETHING WENT WRONG!")
            sql1 = "INSERT INTO recent_details(id , admin_email , date , time , sent_to) VALUES (%s , %s , %s , %s , %s)"
            mysql_connection(sql1 , val1)
    else:
        messagebox.showerror(title = "WARNING" , message = "SOMETHING WENT WRONG!")
        

global email_address
email_address = []
def send_msg():
    message = enter_msg_text.get('1.0', 'end')
    
    sql = "SELECT email_address FROM admin_details"
    email_address = mysql_selection(sql)
    # print(email_address)
    sql = "SELECT password FROM admin_details"
    admin_password = mysql_selection(sql)
    # print(admin_password)
    sentSuccess = False

    if email_address is None:
        messagebox.showerror(title = "SOMETHING WENT WRONG" , message = "Couldn't Found Admin Details")
    elif email_address is not None:
        server = "smtp.gmail.com"
        port = 465
        sender_email = email_address[0]
        # print(sender_email)
        password = admin_password[0]
        # print(password) 


        msg['From'] = email_address[0]
        msg['To'] = ','.join(email_list)
        msg['Subject'] = (enter_subject_entry.get())
        msg.attach(MIMEText(message , 'plain'))

        text = msg.as_string()


        refused = {}
        # Create a SSL context
        context = ssl.create_default_context()
        # Login and Send Email
        with smtplib.SMTP_SSL(server, port, context=context) as Server:
            Server.login(sender_email, password)
            for addresses in email_list:
                try:
                    Server.sendmail(sender_email, addresses, text)
                
                except smtplib.SMTPResponseException:
                    error_code = smtplib.SMTPResponseException.smtp_code
                    error_message = smtplib.SMTPResponseException.smtp_error
                    if (error_code==422):
                        print("Recipient Mailbox Full")
                    elif(error_code==431):
                        print ("Server out of space")
                    elif(error_code==447):
                        print("Timeout. Try reducing number of recipients")
                    elif(error_code==510 or error_code==511):
                        print("One of the addresses in your TO, CC or BBC line doesn't exist. Check again your recipients' accounts and correct any possible misspelling.")
                    elif(error_code==512):
                        print("Check again all your recipients' addresses: there will likely be an error in a domain name (like mail@domain.coom instead of mail@domain.com)")
                    elif(error_code==541 or error_code==554):
                        print("Your message has been detected and labeled as spam. You must ask the recipient to whitelist you")
                    elif(error_code==550):
                        print("Though it can be returned also by the recipient's firewall (or when the incoming server is down), the great majority of errors 550 simply tell that the recipient email address doesn't exist. You should contact the recipient otherwise and get the right address.")
                    elif(error_code==553):
                        print("Check all the addresses in the TO, CC and BCC field. There should be an error or a misspelling somewhere.")
                    else:
                        print(error_code+": "+error_message)
                except smtplib.SMTPRecipientsRefused:
                    print("Error wit recipient mail address " + addresses)

                
                
            
            status_lbl1.config(text="Email Sent Successfully!")
            
        index()
        recent_details()
    else:
        messagebox.showerror(title = "WARNING" , message = "SOMETHING WENT WRONG!")
    # if (sentSuccess == False):
    #     status_lbl1.config(text="Email Couldn't Be Sent Successfully!")


def back():
    time.sleep(2)
    frame.destroy()
    import Emailmainframe

def close_frame():
    
    exit = messagebox.askyesno(title = "STATUS" , message = "Are You Sure You Want To Exit?")
    if exit == True:
        messagebox.showinfo(title = "STATUS" , message = "Press OK To Exit In 5 Seconds.....")       
        sql = "DELETE FROM bulkemail_attachment"
        mysql_connection1(sql)
        sql1 = "DELETE FROM bulkemail_csvupload "
        mysql_connection1(sql1)
        sql2 = "DELETE FROM admin_details"
        mysql_connection1(sql2)
        time.sleep(5)
        frame.destroy()
    else:
        pass

def voice_recognition():
    
    lang = ""
    lan = input("Enter language to Recognize:")
    lan1 = messagebox.QUESTION()
    languages = ['en-Us' , 'hi-IN']
    if (lan == "English"):
        lang = languages[0]
    elif (lan == "Hindi"):
        lang = languages[1]
    else:
        print("Language not Supported!")
    if (lan == "English" or lan == "Hindi"):
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print('Clearing background noise..')
                recognizer.adjust_for_ambient_noise(source,duration=1)
                print("waiting for your message...")
                recordedaudio=recognizer.listen(source)
                print('Done recording..!')
                print(recordedaudio)
            try:
                print('Printing the message..')
                text=recognizer.recognize_google(recordedaudio,language = lang)
                print('Your message:{}'.format(text))
                # messagebox.showinfo(title = "Message" , message = text)
                return text
            except Exception as ex:
                print(ex)

l = tk.Label(
    frame, text="Attach Excel File To\n Import Email Addresses", background="blue")
l.place(width=200, x=50, y=100)
attach_file = tk.Button(frame, text="Attach Files",
                        bd=2, fg="blue", command=attach_file)
attach_file.place(width=200, x=350, y=100)
enter_subject_label = tk.Label(frame , text = "Enter Subject" , background="blue")
enter_subject_label.place(width=200 , x=50 , y=200)
enter_subject_entry = tk.Entry(frame , bd=2)
enter_subject_entry.place(height=30 , width=600 , x=350 , y=200)
enter_msg_label = tk.Label(frame, text="Enter Message", background="blue")
enter_msg_label.place(width=200, x=50, y=250)
enter_msg_text = tk.Text(frame, bd=2)
enter_msg_text.place(height=200, width=600, x=350, y=250)
voice_rec_photo = tk.PhotoImage(file = f"voice_rec.png")
voice_rec_btn = tk.Button(frame , background = "red" , image = voice_rec_photo , bd = 2 )
voice_rec_btn.place(height = 30 , width = 30 , x = 880 , y = 420)
pause_btn_photo = tk.PhotoImage(file = f"stop_btn1.png")
pause_btn = tk.Button(frame , background = "red" , image = pause_btn_photo , bd = 2)
pause_btn.place(height = 30 , width = 30 , x = 920 , y = 420)
photo = tk.PhotoImage(file=f"attachment11.png")
attach_file_btn = tk.Button(frame, background="red",
                            image=photo , command=attach_attachment)
attach_file_btn.place(height=30, width=30, x=920, y=450)
send_btn = tk.Button(frame, text="SEND", bd=2, command=send_msg)
send_btn.place(width=150, x=350, y=510)
back_btn = tk.Button(frame, text="BACK", bd=2, command=back)
back_btn.place(width=150, x=550, y=510)
status_lbl = tk.Label(frame, text="STATUS", background="blue")
status_lbl.place(width=200, x=50, y=610)
status_lbl1 = tk.Label(frame, bd=5)
status_lbl1.place(width=300, x=350, y=610)

frame.protocol('WM_DELETE_WINDOW' , close_frame)
frame.mainloop()

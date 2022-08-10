import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
from datetime import datetime

frame = tk.Tk()
frame.geometry('1400x1000')
frame.config(background = "slateblue")
frame.title("Recent Activity")
frame.focus_force()
frame.pack_propagate(1)

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
            connection.close()

def mysql_selection(sql , val):
    connection = mysql.connector.connect(
        host = "localhost" ,
        user = "root" , 
        password = "123456" , 
        database = "email_client"
    )

    mycursor = connection.cursor()
    
    mycursor.execute(sql , val)

    myresult = mycursor.fetchone()

    for i in myresult:
        return i

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

    # for i in myresult:
    #     return i
    return myresult


def back():
    frame.destroy()
    import Emailmainframe

def clear_history():
    ask = messagebox.askyesno(title = "STATUS" , message = "Are You Sure You Want To Clear All Records ?")
    if ask == 1:
        sql6 = "DELETE FROM recent_details"
        mysql_connection1(sql6)
    elif ask == 0:
        pass
    else:
        messagebox.showerror(title = "WARNING" , message = "Something Went Wrong!")

sql1 = "SELECT id FROM bulkemail_entermanually"
val1 = mysql_selection1(sql1)
print(val1)

def show_history():
    sql = "SELECT sent_to FROM recent_details"
    val = mysql_selection1(sql)
    print(val)
    sql1 = "SELECT id FROM recent_details"
    val1 = mysql_selection1(sql1)
    # print(val1)
    if val is not None:
        for i in range (len(val1)):
            sql2 = "SELECT admin_email FROM recent_details"
            val2 = mysql_selection1(sql2)
            # current_date = datetime.now()
            # date = current_date.strftime("%d/%m/%y")
            # time = current_date.strftime("%H:%M:%S")
            sql4 = "SELECT date FROM recent_details"
            val4 = mysql_selection1(sql4)
            sql5 = "SELECT time FROM recent_details"
            val5 = mysql_selection1(sql5)

            sql3 = "SELECT sent_to FROM recent_details"
            val3 = mysql_selection1(sql3)
            # print(i)
            j = val1[i][0]

            if (val3[i][0] == ""):
                pass
            elif val3[i][0] != "":
                tree.insert('' , 'end' , values = (val1[i] , val2[i] , val4[i] , val5[i] , val3[i]))
                tree.insert('' , 'end' , values = ())

            else:
                messagebox.showerror(title = "WARNING" , message = "Something Went Wrong!")
    elif val is None:
        messagebox.showinfo(title = "STATUS" , message = "No Record Found In Database!")
    else:
        messagebox.showerror(title = "WARNING" , message = "Something Went Wrong!")

columns = ('id' , 'Admin_Email' , 'Date' , 'Time' , 'Sent_To')
tree = ttk.Treeview(frame , columns = columns , show = "headings")
tree.place(height = 400 , width = 1300 , x=50 , y=200)
tree.column('id' , anchor = "center")
tree.column('Admin_Email' , anchor = "center")
tree.column('Date' , anchor = "center")
tree.column('Time' , anchor = "center")
tree.column('Sent_To' , anchor = "center")


label = tk.Label(frame , text = "Recent_Details" , background = "slateblue" , font = ("Algerian" , "56") , anchor = "center")
label.place(height = 100 , width = 1300 , x=50 , y=50)
clear_history = tk.Button(frame , text = "Clear History" , command = clear_history , bd = 2)
clear_history.place(width = 150 , x=600 , y=700)
back = tk.Button(frame , text = "Back" , command = back , bd = 2)
back.place(width = 150 , x=780 , y=700)
show_history = tk.Button(frame , text = "Show History" , command = show_history , bd = 2)
show_history.place(width = 150 , x=420 , y=700)
tree.heading('id' , text = "Record_Id")
tree.heading('Admin_Email' , text = "Admin_Email")
tree.heading('Date' , text = "Date")
tree.heading('Time' , text = "Time")
tree.heading('Sent_To' , text = "Sent_To")

# show_details = tk.Text(frame , background = "pink" , foreground = "red")
# show_details.place(height=200 , width=800 , x=100 , y=150)

frame.resizable(False, False)
frame.mainloop()


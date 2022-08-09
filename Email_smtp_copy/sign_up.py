import tkinter as tk 
from tkinter import *


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

background_img = PhotoImage(file = f"background_signup.png")
background = canvas.create_image(
    500.0, 300.0,
    image=background_img)
frame.focus_force()
frame.pack_propagate(0)


def login():
    name = enter_admin_name.get()
    email = enter_email_entry.get()
    contact = enter_contact_number.getint(0)
    password = enter_password.get()

def show_password():
    if (enter_password.cget('show') == '*'):
        enter_password.config(show = '')
    else:
        enter_password.config(show = "*")

enter_admin_name = tk.Entry(frame , bd = 2 , fg = "black" , highlightthickness= 1 , highlightbackground= "#884dff")
enter_admin_name.place(width = 240 , x=558 , y=270)
enter_email_entry = tk.Entry(frame , bd = 2 , fg = "black" , highlightthickness= 1 , highlightbackground= "#884dff")
enter_email_entry.place(width = 240 , x=558 , y=325)
enter_contact_number = tk.Entry(frame , bd = 2 , fg = "black" , highlightthickness= 1 , highlightbackground= "#884dff")
enter_contact_number.place(width = 240 , x=558 , y=382)
enter_password = tk.Entry(frame , bd = 2 , fg = "black" , highlightthickness= 1 , highlightbackground= "#884dff" , show = "*")
enter_password.place(width = 240 , x=558 , y=435)
check_button = tk.Checkbutton(frame , text = "Show Password" , activeforeground="purple" , command = show_password)
check_button.place(width = 100 , x = 700 , y = 460)
login = tk.Button(frame , text = "LOGIN" , bd = 1 , highlightthickness= 1 , highlightbackground= "#110033" , background = "#aa80ff" , command = login)
login.place(width = 100 , x=635 , y=495)






frame.mainloop()


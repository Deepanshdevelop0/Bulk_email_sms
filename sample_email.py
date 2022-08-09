# # # import tkinter as tk
# # # from tkinter import ttk
# # # import mysql.connector
# # # from tkinter import messagebox
# # # from datetime import datetime

# # # def mysql_selection1(sql):
# # #     connection = mysql.connector.connect(
# # #         host = "localhost" ,
# # #         user = "root" , 
# # #         password = "123456" , 
# # #         database = "email_client"
# # #     )

# # #     mycursor = connection.cursor()
    
# # #     mycursor.execute(sql)

# # #     myresult = mycursor.fetchall()

# # #     # for i in myresult:
# # #     #     return i
# # #     return myresult

# # # sql1 = "SELECT id FROM bulkemail_entermanually"
# # # val1 = mysql_selection1(sql1)
# # # print(val1)



# l = ["1" , "2" , "3" , "4" , "5" , "6"]
# # # length = len(l) - 1
# # # print(len(l))
# id = 1
# j = []
# # b=1
# # # print(len(l))
# # # print(l[5])
# for i in l:
#     print(i)
#     if (i == 1):
#         print(i)
#         j.append(i)
#         print(j)
#     for a in range(len(j)):
#         if a == 0:
#             print("0")
#         elif a>=1:
#             print("1")
#         else:
#             print("Something Went Wrong")
#     id+=1
# # id = ["1" , "1" , "1" , "1" , "2" , "2" , "2" , "2" , "3" , "4" , "5" , "6"]
# # a = []
# # for i in range(len(id)):
# #     for j in range(i,len(id)):
# #         if (id[i] == id[j]):
# #             a.append(id[j])

# #         print(a)
        


# list = []
# val = ["1" , "2" , "3" , "4"]
# list.append(val)
# val = ["5" , "6" , "7" , "8"]
# list.append(val)
# val = ["1" , "2" , "3" , "4"]
# list.append(val)
# val = ["5" , "6" , "7" , "8"]
# list.append(val)
# print(list)

# print(list[0])

source = "C:/Users/Deepanshu/AppData/Local/Programs/Python/Python310/python.exe"
list = source.split('/')
# print(list)
print(list[len(list)-1])

l = [("1" , "2" , "3" , "4" , "5") , ("1" , "2")]
print(l[0][5])

a=[]
print(len[a])
from tkinter import *
from tkinter.ttk import Combobox
import time
import math
import sqlite3


class Login(object):
    def __init__(self,master):
        self.master = master
        self.master.geometry("400x400")
        self.master.wm_title("Login Window") # initialises menu window

        self.Username = StringVar()
        self.Password = StringVar()

        windowtitle = "Tkinter Weight on a spring oscillator"
        self.TitleLabel = Label(self.master, text=windowtitle).grid(row=0,column=0,columnspan=2)
        self.UsernameLabel = Label(self.master, text="Username").grid(row=1,column=0)
        self.PasswordLabel = Label(self.master, text="Password").grid(row=2,column=0)
        
        self.UsernameEntry = Entry(self.master, textvariable=self.Username).grid(row=1,column=1)
        self.PasswordEntry = Entry(self.master, textvariable=self.Password).grid(row=2,column=1)

        self.LoginButton = Button(self.master,text="Login").grid(row=4,column=0)#,command=self.Save)
        self.RegisterButton = Button(self.master,text="Register",command=self.Register).grid(row=4,column=1)#,command=self.Run)

    def Register(self):
        Username = self.Username.get() ####HELLO?????
        Password = self.Password.get()
        
        self.usernamelist = []
        with sqlite3.connect("UserInfo.db") as db:
            cursor = db.cursor()
            print("Connected successfully")
            sql = """select Username from Login"""
            cursor.execute(sql)
            self.allfiledetails = cursor.fetchall()
        for index in self.allfiledetails:
            self.usernamelist.append(index[0])
##            print(index[0])
        db.commit()
        print(self.usernamelist)


        


        
if __name__ == "__main__":
    root = Tk()
    menu = Login(root)

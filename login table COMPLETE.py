from tkinter import *
import tkinter.messagebox
from tkinter.ttk import Combobox
import time
import math
import sqlite3
import base64




class Login(object):
    def __init__(self,master):
        self.master = master
        self.master.geometry("400x400")
        self.master.wm_title("Login Window") # initialises menu window

        self.Username = StringVar()
        self.Password = StringVar()

##        self.Username.set("io")
##        self.Password.set("biggerbanana")


        windowtitle = "Tkinter Weight on a spring oscillator"
        notificationtext = "Enter your username and password"
        self.Title = Label(self.master, text=windowtitle).grid(row=0,column=0,columnspan=3)
        self.UsernameLabel = Label(self.master, text="Username").grid(row=1,column=0)
        self.PasswordLabel = Label(self.master, text="Password").grid(row=2,column=0)
        self.NotificationLabel = Label(self.master, text=notificationtext).grid(row=5,column=0,columnspan=3)
        
        self.UsernameEntry = Entry(self.master, textvariable=self.Username).grid(row=1,column=1,columnspan=2)
        self.PasswordEntry = Entry(self.master, textvariable=self.Password).grid(row=2,column=1,columnspan=2)

        self.LoginButton = Button(self.master,text="Login",command=self.Login).grid(row=4,column=0)
        self.RegisterButton = Button(self.master,text="Register",command=self.Register).grid(row=4,column=1)
        self.CloseButton = Button(self.master,text="Close",command=self.close).grid(row=4,column=2)


        self.regError = "This user already registered in the database" # error codes
        self.loginError = "This user is not registered in the database"
        self.unError = "Username box cannot be blank"
        self.pwError = "Password box cannot be blank"
        self.pwError2 = "Password incorrect!"

        self.createLoginTable()



    def createLoginTable(self):
        db_name = "UserInfo.db"
        try:
            table_name = "UserInfo"
            sql = """create table Login
                                (UserID integer,
                                Username string,
                                Password string,
                                primary key (UserID))"""
            with sqlite3.connect(db_name) as db:
                cursor = db.cursor()
                cursor.execute("drop table if exists {}".format(table_name))
                cursor.execute("select name from sqlite_master where name = ?",(table_name,))
                cursor.execute(sql)
                db.commit()
                
        except sqlite3.OperationalError:
            print("Why do i work???")
            pass
        
    def close(self):
        quit()
    
    def generateUserID(self):
        with sqlite3.connect("UserInfo.db") as db:
            cursor = db.cursor()
            cursor.execute("""select * from Login""")
            self.allfiledetails = cursor.fetchall()
        newUserID = len(self.allfiledetails) +1
        return newUserID


    def encryptPassword(self,password):
        encryptedPassword = str(base64.b64encode(password.encode("utf-8")))
        passwordlen = len(encryptedPassword)
        encryptedPassword = encryptedPassword[2:passwordlen-1]
        return encryptedPassword

    def decryptPassword(self,password):
        decryptedPassword = base64.b64decode(password).decode("utf-8")
        return decryptedPassword

        

    def Register(self):
        #call input username and password
        Username = self.Username.get()
        Password = self.Password.get()

        #call all usernames currently in table Login for check
        self.usernamelist = []
        with sqlite3.connect("UserInfo.db") as db:
            cursor = db.cursor()
            sql = """select Username from Login"""
            cursor.execute(sql)
            self.allfiledetails = cursor.fetchall()
        for index in self.allfiledetails:
            self.usernamelist.append(index[0])
        db.commit()

        #error handling input
        if Username == "":
            tkinter.messagebox.showinfo('Error!',self.unError)
        elif Password == "":
            tkinter.messagebox.showinfo('Error!',self.pwError)
        elif Username in self.usernamelist:
            tkinter.messagebox.showinfo('Error!',self.regError)    
        else: # Username and password have passed the checks, can be committed to database

            newUserID = self.generateUserID()
            encryptedpassword = self.encryptPassword(Password)
            
            #username and password are input into table
            with sqlite3.connect("UserInfo.db") as db:
                cursor = db.cursor()
                sql = """insert into Login values (?,?,?)"""
                temp = (newUserID,Username,encryptedpassword)
                #uses the length of usernamelist so the new record is appended to the end of the table
                cursor.execute(sql,temp)
                db.commit()
            tkinter.messagebox.showinfo('Success!',"User committed to database")
            ###ENTER MENU


    def Login(self):
        #call input username and password
        Username = self.Username.get()
        Password = self.Password.get()

        #call all usernames currently in table Login for check
        self.usernamelist = []
        with sqlite3.connect("UserInfo.db") as db:
            cursor = db.cursor()
            sql = """select Username from Login"""
            cursor.execute(sql)
            self.allfiledetails = cursor.fetchall()
        for index in self.allfiledetails:
            self.usernamelist.append(index[0])
        db.commit()

        #error handling input
        if Username == "":
            tkinter.messagebox.showinfo('Error!',self.unError)
        elif Password == "":
            tkinter.messagebox.showinfo('Error!',self.pwError)
        elif Username not in self.usernamelist:
            tkinter.messagebox.showinfo('Error!',self.loginError)
            
        else: #decrypt password in db
            with sqlite3.connect("UserInfo.db") as db:
                cursor = db.cursor()
                cursor.execute("select * from Login where Username= ?", (Username,)) #########
                userRecord = cursor.fetchone()
                
                userID = userRecord[0]
                username = userRecord[1]
                encryptedpassword = userRecord[2]
                decryptedpassword = self.decryptPassword(encryptedpassword)

                if decryptedpassword != Password:
                   tkinter.messagebox.showinfo('Error!',self.pwError2)
                else:
                   tkinter.messagebox.showinfo("Success!","Password correct!")



                   



if __name__ == "__main__":
    root = Tk()
    login = Login(root)

from tkinter import *
import tkinter.messagebox
from tkinter.ttk import Combobox
import time
import math
import sqlite3
import base64




class Login(object): # class which establishes the login window
    def __init__(self,master):
        self.master = master
        self.master.geometry("400x400")
        self.master.wm_title("Login Window") # initialises menu window

        self.Username = StringVar()
        self.Password = StringVar()

        windowtitle = "Tkinter Weight on a spring oscillator"
        notificationtext = "Enter your username and password"
        self.Title = Label(self.master,text=windowtitle,font=40,padx=20,pady=50).grid(row=0,column=0,columnspan=3)
        self.UsernameLabel = Label(self.master,text="Username",fg="blue").grid(row=1,column=0)
        self.PasswordLabel = Label(self.master,text="Password",fg="blue",pady=20).grid(row=2,column=0)
        self.NotificationLabel = Label(self.master, text=notificationtext).grid(row=5,column=0,columnspan=3)
        
        self.UsernameEntry = Entry(self.master, textvariable=self.Username).grid(row=1,column=1,columnspan=2)
        self.PasswordEntry = Entry(self.master, textvariable=self.Password).grid(row=2,column=1,columnspan=2)

        self.LoginButton = Button(self.master,text="Login",command=self.Login).grid(row=4,column=0)
        self.RegisterButton = Button(self.master,text="Register",command=self.Register).grid(row=4,column=1)
        self.CloseButton = Button(self.master,text="Close",command=self.close).grid(row=4,column=2)

        #error codes
        self.regError = "This user already registered in the database"
        self.loginError = "This user is not registered in the database"
        self.unError = "Username box cannot be blank"
        self.pwError = "Password box cannot be blank"
        self.pwError2 = "Password incorrect!"

        self.createLoginTable()



    def createLoginTable(self): #initialises the login table
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
                
        except sqlite3.OperationalError: #if the table exists, this errors flags up and the initialisation is skipped
            pass


        #preset initialisation
        try:
            userid = 1
            username = "admin"
            passwordraw = "H00kesLaw"
            password = self.encryptPassword(passwordraw)
            temp = [userid,username,password]
            sql = """insert into Login values (?,?,?)"""

            with sqlite3.connect("UserInfo.db") as db:
                cursor = db.cursor()
                cursor.execute(sql,temp)
                db.commit()
        except sqlite3.IntegrityError: #if these values are already present in the db this process is skipped
            pass

        
    def close(self):
        quit()

    
    def generateUserID(self): 
        with sqlite3.connect("UserInfo.db") as db:
            cursor = db.cursor()
            cursor.execute("""select UserID from Login""")
            userids = cursor.fetchall()
        #find id of last user in UserInfo and add one
        lastvalue = len(userids)
        newUserID = userids[lastvalue-1][0] +1
        #The new user is added to the bottom of the DB
        return newUserID


    def encryptPassword(self,password):
        #password is encoded using base64
        encryptedPassword = str(base64.b64encode(password.encode("utf-8")))
        passwordlen = len(encryptedPassword)
        encryptedPassword = encryptedPassword[2:passwordlen-1]
        #the password is saved in its encrypted form to the DB
        return encryptedPassword

    def decryptPassword(self,password):
        decryptedPassword = base64.b64decode(password).decode("utf-8")
        return decryptedPassword

        

    def Register(self):
      try:
          print(self.menu)
      except AttributeError:
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

               self.openMenu(Username,newUserID)



    def Login(self):
       try:
          print(self.menu)
       except AttributeError:
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
                  cursor.execute("select * from Login where Username= ?", (Username,))
                  userRecord = cursor.fetchone()
                  db.commit()
                   
                  userID = userRecord[0]
                  username = userRecord[1]
                  encryptedpassword = userRecord[2]
                  decryptedpassword = self.decryptPassword(encryptedpassword)

                  if decryptedpassword != Password:
                      tkinter.messagebox.showinfo('Error!',self.pwError2)
                  else:
                      if username == "admin":
                          self.openAdmin()
                      else:
                          self.openMenu(username,userID)
                      self.Username.set("")
                      self.Password.set("")


    def openMenu(self,username,userid):
      #this subroutine is called if the user has entered the correct credentials
      root1 = Toplevel(self.master)
      self.menu = Menu(root1,userid,username)
      self.master.wm_state('iconic')

    def openAdmin(self):
      #this subroutine is called if the user has entered the admin credentials
      self.master.destroy()
      menu = Admin()


####################################


class Admin(object):
   def __init__(self):
        print("WELCOME ADMIN USER\n")
        #The admin page will run as long as the variable run is true
        run = True
        while run:
            #admin selects user to interact with
            print("\nWhich user would you like to interact with?\n~~~~")
            self.usernamelist = []
            #the name's of every user in the UserInfo db are called.
            with sqlite3.connect("UserInfo.db") as db:
                cursor = db.cursor()
                sql = "select Username from Login"
                cursor.execute(sql)
                rawusernamelist = cursor.fetchall()
            for index in rawusernamelist:
                self.usernamelist.append(index[0])
                print(index[0])
            db.commit()

            user = self.acceptValidInput(self.usernamelist)
            #once the name of the user is successfully called
            #the admin can decide what do do with that user
            print("\nWhat would you like to do with user {}?\n~~~~".format(user))
            print("""Modify user (m)
Delete user (d)
Add new user (a)
View user details (v)
Quit (q)""")
            inputlist = ["m","d","a","v","q"]
            option = self.acceptValidInput(inputlist)

            if option == "m":
                self.modifyUser(user)
            elif option == "d":
                self.deleteUser(user)
            elif option == "a":
                self.addUser()
            elif option == "v":
                self.viewUser(user)
            elif option == "q":
                quit()

   def acceptValidInput(self,newlist):
       #takes a list of valid inputs and only returns selected when selected matches one of those inputs
       invalid = True
       while invalid:
          selected = input("> ").lower()
          if selected not in newlist:
              print("Invalid input! Please try again")
          else:
              return selected


   def generateUserID(self):
      #Takes the last saved user id and sets the new id as that plus 1
      with sqlite3.connect("UserInfo.db") as db:
         cursor = db.cursor()
         cursor.execute("""select UserID from Login""")
         userids = cursor.fetchall()
         db.commit()
      lastvalue = len(userids)
      newUserID = userids[lastvalue-1][0] +1
      return newUserID


   def encryptPassword(self,password):
      #password is encoded using base64
      encryptedPassword = str(base64.b64encode(password.encode("utf-8")))
      passwordlen = len(encryptedPassword)
      encryptedPassword = encryptedPassword[2:passwordlen-1]
      #the password is saved in its encrypted form to the DB
      return encryptedPassword         


   def modifyUser(self,user):
      #The record in userinfo corresponding with the selected user is called
      with sqlite3.connect("UserInfo.db") as db:
         cursor = db.cursor()
         cursor.execute("""select * from Login where Username =?""", (user,))
         record = cursor.fetchall()
         db.commit()
      userid = record[0][0]
      print("\nUserID = {}".format(userid))
      print("Modify username or password? (u/p) ")
      
      inputlist = ["u","p"]
      selected = self.acceptValidInput(inputlist)

      Invalid = True
      while Invalid:
         #the admin chooses to change the username
         if selected == "u":
            Username = input("Change username to what?\n> ")
            if Username == "" or Username in self.usernamelist:
               print("Invalid input!")
            else:
               Invalid = False
         #the admin chooses to change the username
         elif selected == "p":
            Password = input("Change password to what?\n> ")
            if Password == "":
               print("Invalid input!")
            else:
               Invalid = False
               #the new password is encrypted
               encryptedpassword = self.encryptPassword(Password)
            
      with sqlite3.connect("UserInfo.db") as db:
         cursor = db.cursor()
         #the admin chooses to change the username
         if selected == "u":
            sql = "update Login set Username = ? where UserID = ?"
            cursor.execute(sql,(Username,userid))
         #the admin chooses to change the username
         elif selected == "p":
            sql = "update Login set Password = ? where UserID = ?"
            cursor.execute(sql,(encryptedpassword,userid))
         db.commit()
         


   def deleteUser(self,user):
      #user is deleted from the database
      with sqlite3.connect("UserInfo.db") as db:
         cursor = db.cursor()
         sql = "delete from Login where Username=?"
         user = [user]
         cursor.execute(sql,user)
         db.commit()
      print("\nUser deleted from database\n##############\n")
      

   def addUser(self):
      Invalid = True
      while Invalid:
         Username = input("Enter new user's username\n> ")
         Password = input("Enter new user's password\n> ")
         if Username == "" or Password == "" or Username in self.usernamelist:
            print("Invalid input!")
         else:
            Invalid = False

      #the new user's id and encryped password are generated  
      newUserID = self.generateUserID()
      encryptedpassword = self.encryptPassword(Password)
            
      with sqlite3.connect("UserInfo.db") as db:
         cursor = db.cursor()
         sql = """insert into Login values (?,?,?)"""
         temp = (newUserID,Username,encryptedpassword)
         #new user is appended to the db
         cursor.execute(sql,temp)
         db.commit()
      print("\nUser added to database\n##############\n")


   def viewUser(self,user):
      #UserId and Username are displayed by calling the relevant record
      with sqlite3.connect("UserInfo.db") as db:
         cursor = db.cursor()
         cursor.execute("""select * from Login where Username =?""", (user,))
         record = cursor.fetchall()
         db.commit()
      userid = record[0][0]
      username = record[0][1]
      print("\nUserID = {0}\nUsername = {1}".format(userid,username))





####################################



class Menu(object):  # class which establishes the menu window
    def __init__(self,master,userid,username): # initialises the contents of the window

        self.UserID = userid
        self.Username = username

        self.master = master
        self.master.geometry("400x600")
        self.master.wm_title("Input Window") # initialises menu window

        self.SimulationName = StringVar()
        self.Amplitude = DoubleVar()
        self.Mass = DoubleVar()
        self.SpringConstant = DoubleVar() # initialises input variables
        self.Damping = BooleanVar()

        self.Amplitude.set(0.5)

        #table visuals
        titletext = "Welcome user {}!".format(self.Username)
        self.TitleMenu = Label(self.master, text=titletext,pady=40,font=20).grid(row=0,column=1,columnspan=4)

        self.SimulationNameLabel = Label(self.master, text="Simulation name",pady=20,padx=50,fg="red").grid(row=1,column=1,columnspan=3)
        self.AmplitudeLabel = Label(self.master, text="Amplitude in metres",pady=20,fg="red").grid(row=2,column=1,columnspan=3)
        self.MassLabel = Label(self.master, text="Mass in kilogram",pady=20,fg="red").grid(row=3,column=1,columnspan=3)
        self.SpringConstantLabel = Label(self.master, text="Spring Constant in metres",pady=20,fg="red").grid(row=4,column=1,columnspan=3)
        self.PresetValuesLabel = Label(self.master, text="Preset Values",pady=20,fg="red").grid(row=5,column=1,columnspan=3)

        self.SimulationNameEntry = Entry(self.master,textvariable=self.SimulationName)
        self.SimulationNameEntry.grid(row=1,column=4)
        self.AmplitudeScale = Scale(self.master, from_=0, to=2, resolution=0.1, orient=HORIZONTAL,variable=self.Amplitude)
        self.AmplitudeScale.grid(row=2,column=4)
        self.MassScale = Scale(self.master, from_=0.1, to=2.5, resolution=0.05, orient=HORIZONTAL,variable=self.Mass)
        self.MassScale.grid(row=3,column=4)
        self.SpringConstantScale = Scale(self.master, from_=0.5, to=2.5, resolution=0.1, orient=HORIZONTAL,variable=self.SpringConstant)
        self.SpringConstantScale.grid(row=4,column=4)

        self.PresetValuesCombobox = Combobox(self.master,values = "presets")
        self.PresetValuesCombobox.current(0)
        self.PresetValuesCombobox.grid(row=5,column=4)

        self.SaveButton = Button(self.master,text="Save", command=self.Save).grid(row=6,column=1)
        self.RunButton = Button(self.master,text="Run", command=self.Run).grid(row=6,column=2)
        self.CloseButton = Button(self.master,text="Close", command=self.Close).grid(row=6,column=3)
        self.DampingCheckBox = Checkbutton(self.master,text="Damping",variable=self.Damping,pady=20).grid(row=6,column=4)

        self.initaliseTables()
        self.loadCombobox()


    def initaliseTables(self):
        #this subroutine establishes the DBs used by the simulation
        preset_DB = "Preset.db"
        preset_table = "Preset"
        preset_sql = """create table PresetValues
                  (SpringID      integer,
                  SimulationName string,
                  Amplitude      float,
                  Mass           float,
                  SpringConstant float,
                  Damping        boolean,
                  primary key (SpringID))"""
        

        pendulums_DB = "Pendulums.db"
        pendulums_table = "Pendulums.db"
        pendulums_sql = """create table """+self.Username+"""
                  (SpringID      integer,
                  SimulationName string,
                  Amplitude      float,
                  Mass           float,
                  SpringConstant float,
                  Damping        boolean,
                  primary key (SpringID))"""

        self.createTable(preset_DB,preset_table,preset_sql)
        self.createTable(pendulums_DB,pendulums_table,pendulums_sql)

        #preset initialisation
        try:
            newSpringID = 0
            SimulationName = "test"
            Amplitude = 2.0
            Mass = 1.5
            SpringConstant = 1.0
            Damping = True
            Values = [newSpringID,SimulationName,Amplitude,Mass,SpringConstant,Damping]
            sql2 = """insert into PresetValues values(?,?,?,?,?,?)"""

            #the preset values are input into the preset db
            with sqlite3.connect("Preset.db") as db:
                cursor = db.cursor()
                cursor.execute(sql2,Values)
                db.commit()
        except sqlite3.IntegrityError: #if these values are already present in the db this process is skipped
            pass

        with sqlite3.connect("Pendulums.db") as db:
            cursor = db.cursor()
            cursor.execute("select * from {}".format(self.Username))
            allfiledetails = cursor.fetchall()
            db.commit()
            
        #if the user's table is empty, the preset values are input      
        if len(allfiledetails) == 0:
            Values = []
            with sqlite3.connect("Preset.db") as db:
               cursor = db.cursor()
               cursor.execute("select * from PresetValues")
               presetrecord = cursor.fetchone()
               
            for x in range(6):
               Values.append(tuple(presetrecord)[x])
               db.commit()
               
            with sqlite3.connect("Pendulums.db") as db:
               cursor = db.cursor()
               cursor.execute("insert into "+self.Username+" values(?,?,?,?,?,?)",Values)
               db.commit()
        


    def createTable(self,db_name,table_name,sql):
        try: 
            with sqlite3.connect(db_name) as db:
                cursor = db.cursor()
                cursor.execute("drop table if exists {}".format(table_name))
                cursor.execute("select name from sqlite_master where name = ?",(table_name,))
                cursor.execute(sql)
                db.commit()
        except sqlite3.OperationalError: #if the table already exists, this process is skipped
            pass

    def generateSpringID(self):
        with sqlite3.connect("Pendulums.db") as db:
            cursor = db.cursor()
            cursor.execute("select * from {}".format(self.Username))
            allfiledetails = cursor.fetchall()
            db.commit()
        #spring id is generated from counting the number of springs in the user's table and then adding one
        newSpringID = len(allfiledetails) +1
        return newSpringID


    def click(self, event):
        filename = self.currentFile.get()     
        for x in self.allfiledetails:
            if filename == x[1]:
                break

        #when the subroutine finds the record which corresponds with filename, those values are loaded
        self.SimulationName.set(x[1])
        self.AmplitudeScale.set(x[2])
        self.MassScale.set(x[3])
        self.SpringConstantScale.set(x[4])
        self.Damping.set(x[5])


    def loadCombobox(self):
        self.currentFile = StringVar()
        self.PresetValuesCombobox["textvariable"] = self.currentFile
        self.allfiledetails = []
        self.pendulumlist = []
        
        with sqlite3.connect("Pendulums.db") as db:
            cursor = db.cursor()
            cursor.execute("select * from {}".format(self.Username))
            self.allfiledetails = cursor.fetchall()
        for x in self.allfiledetails:
            self.pendulumlist.append(x[1]) #the simulation names are saved as their own list so they can be displayed by the combobox
            db.commit()
        
        finalspring = len(tuple(self.pendulumlist))
        self.reducedlist = tuple(self.pendulumlist)[finalspring-8:finalspring] #combobox only displays the last 8 saved values
        
        self.PresetValuesCombobox["values"] = self.reducedlist
        self.PresetValuesCombobox.bind("<<ComboboxSelected>>", self.click) #registers a selection of data in the combo box

        ##########################################################




    def Close(self):
        quit()

    def Save(self):
        #call input spring values
        newSpringID = self.generateSpringID()
        SimulationName = self.SimulationName.get()
        Amplitude = self.Amplitude.get()
        Mass = self.Mass.get()
        SpringConstant = self.SpringConstant.get()
        Damping = self.Damping.get()

        #save spring values as one list
        Values = [newSpringID,SimulationName,Amplitude,
                  Mass,SpringConstant,Damping]

        #values are comitted to DB
        with sqlite3.connect("Pendulums.db") as db:
            cursor = db.cursor()
            sql = "insert into "+self.Username+" values(?,?,?,?,?,?)"
            cursor.execute(sql,Values)
        db.commit()
        print("values saved successfully")
        
        #combobox is loaded again so its list is updated
        self.loadCombobox()


    def Run(self):
        #call input spring values
        SpringID = self.generateSpringID()
        SimulationName = self.SimulationName.get()
        Amplitude = self.Amplitude.get()
        Mass = self.Mass.get()
        SpringConstant = self.SpringConstant.get()
        Damping = self.Damping.get()

        #create window the simulation will be run in
        root2 = Toplevel(self.master)
        root2.resizable(0,0)
        root2.title(SimulationName)
        root2.wm_attributes("-topmost", 1)
        canvas = Canvas(root2, width=600, height=800)
        canvas.pack()
        root2.update()

        if Damping == 0:
            spring = Simulation(root2,canvas,Amplitude,Mass,SpringConstant,Damping)
        #If the user has selected for the simulation to have damping, the Damped Simulation is loaded
        elif Damping == 1:
            spring = SimulationDamped(root2,canvas,Amplitude,Mass,SpringConstant,Damping)






####################################
####################################
        

class Simulation:
    def __init__(self,master,canvas,
                 amplitude, mass, springConstant, damping):
        #receive input from menu
        self.canvas = canvas
        self.amplitude = amplitude
        self.mass = mass
        self.spring_constant = springConstant
        self.damping = damping

        self.mainloop()

    def calculateStringValues(self):
        #initialise spring values
        self.initial_displacement = self.amplitude * 150
        self.time_period = (2*math.pi) * math.sqrt(self.spring_constant / self.mass)
        self.frequency = 1 / self.time_period
        self.angular_vel = (2*math.pi) * self.frequency

        #initalise spring
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.center_x = self.canvas_width / 2
        self.top_y = 20
        self.originbase_y = (self.canvas_height/ 2)
        self.line_width = self.spring_constant *4 #adjusts the width of the spring's line based on spring constant
        self.radius = 8*(self.mass+2)

        #the visual components of the simulation are saved inside a dictionary
        self.visuals = {}
        

    def createSpring(self,counter,i):
        state = self.initial_displacement * math.cos(self.angular_vel*counter)
        self.base_y = self.originbase_y + state

        #initalise spring text
        displacement = self.amplitude * math.cos(self.angular_vel*counter)
        
        #speed
        speed = round(self.angular_vel * math.sqrt(self.amplitude**2 - displacement**2), 2)
        speed_str = "speed = " + str(speed) + " m/s"
        self.visuals["v"] = self.canvas.create_text(90, self.originbase_y-120,
                                                    text=speed_str, font=("Comic Sans MS",12))
        #acceleration
        acceleration = round(-(self.angular_vel**2)* displacement, 2)
        acceleration_str = "acceleration = " + str(acceleration) + " m/s^2"
        self.visuals["a"] = self.canvas.create_text(120, self.originbase_y-60,
                                                    text=acceleration_str, font=("Comic Sans MS",12))
        #max speed
        maxspeed = round(self.angular_vel * self.amplitude, 2)
        maxspeed_str = "max speed = " + str(maxspeed) + " m/s"
        self.visuals["mv"] = self.canvas.create_text(100, self.originbase_y-90,
                                                    text=maxspeed_str, font=("Comic Sans MS",12))
        #max acceleration
        maxacceleration = round((self.angular_vel**2)*self.amplitude, 2)
        maxacceleration_str = "max acc = " + str(maxacceleration) + " m/s^2"
        self.visuals["ma"] = self.canvas.create_text(100, self.originbase_y-30,
                                                    text=maxacceleration_str, font=("Comic Sans MS",12))
        
        

        #create string
        gap = (self.base_y - self.radius - self.top_y)/i
        num_list = list(range(1,i,2)) + [i]
        string_num = 1
        
        for x in num_list:
           a = x
           prev_a = a-2
           b = round(math.sin(a*math.pi/2))
           prev_b = round(math.sin(prev_a*math.pi/2))
            
           if a == 1:
               x1 = self.center_x
               y1 = self.top_y

           elif a == i:
               x1 = self.center_x + self.radius
               y1 = self.top_y + ((a-1)*gap)

           else:
               x1 = self.center_x + prev_b*self.radius
               y1 = self.top_y + (prev_a*gap)
               
           x2 = self.center_x + b*self.radius
           y2 = self.top_y + (a*gap)
               
           self.visuals["line%s" % string_num] = self.canvas.create_line(x1, y1, x2, y2,
                                                                       width=self.line_width,
                                                                       fill="black")
           string_num = string_num + 1


        #create weight
        if self.base_y <= self.originbase_y:
            self.visuals["w"] = self.canvas.create_rectangle(self.center_x-self.radius, self.base_y-self.radius,
                                                  self.center_x+self.radius, self.base_y+self.radius,
                                                  outline="red", fill="red")
        elif self.base_y > self.originbase_y:
            self.visuals["w"] = self.canvas.create_rectangle(self.center_x-self.radius, self.base_y-self.radius,
                                                  self.center_x+self.radius, self.base_y+self.radius,
                                                  outline="blue", fill="blue")
           
        self.canvas.update()

        

    def destroySpring(self,i):
        num_list = list(range(1,i,2)) + [i]
        
        self.canvas.delete(self.visuals["w"])
        self.canvas.delete(self.visuals["v"])
        self.canvas.delete(self.visuals["mv"])
        self.canvas.delete(self.visuals["a"])
        self.canvas.delete(self.visuals["ma"])
        for x in range(1,len(num_list)+1):
            self.canvas.delete(self.visuals["line%s" % x])

        

    def staticVisuals(self):
        #initial string values are calculated
        self.calculateStringValues()
        state = self.initial_displacement * math.cos(0)
        self.base_y = self.originbase_y + state

        #visuals which remain static are generated
        self.originline = self.canvas.create_line(0,               self.originbase_y,
                                             self.canvas_width,    self.originbase_y,
                                             width=2,fill="green")
        
        self.maxdispline = self.canvas.create_line(0,              self.base_y,
                                             self.canvas_width,    self.base_y,
                                             width=2,fill="gray")
        
        amplitude_str = "amplitude = " + str(self.amplitude) + " m"
        self.visuals["ma"] = self.canvas.create_text(100, self.base_y+30,
                                                    text=amplitude_str, font=("Comic Sans MS",12))


    def mainloop(self):
        self.staticVisuals()
        t = self.time_period/200
        counter = 0
        i = 14
        while 1:
            self.createSpring(counter,i)
            time.sleep(t)
            counter = counter + 2*t
            self.destroySpring(i)



class SimulationDamped(Simulation):

    def mainloop(self):
        self.staticVisuals()
        t = self.time_period/200
        counter = 0
        i = 14
        while 1:
            self.createSpring(counter,i)
            time.sleep(t)
            counter = counter + 2*t
            self.destroySpring(i)
            self.Damping()
    
    def Damping(self):
        self.Dampingnumber = 0.99995
        self.initial_displacement = self.initial_displacement * self.Dampingnumber






if __name__ == "__main__":
    root0 = Tk()
    menu = Login(root0)


  

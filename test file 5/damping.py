from tkinter import *
from tkinter.ttk import Combobox
import time
from math import pi,cos,sin,sqrt
import sqlite3


class Layout(object):
    def __init__(self,master): 
        self.master = master
        self.master.geometry('500x500+100+200')
        self.master.title('menu')
        self.Angle = IntVar()
        self.Length = DoubleVar()
        self.Mass = IntVar()
        self.SimulationName = StringVar()
        self.Box_Values = StringVar()
        self.DampingChoice = IntVar()
        #Simulation Name entry
        
        self.TitleLabel=Label(self.master,text='Pendulum',fg='red',font=30).pack()
        self.SimuationNameLabel=Label(self.master,text='Simulation Name',fg='midnightblue',font=30).pack()
        self.SimulationNameEntry=Entry(self.master,textvariable=self.SimulationName).pack()

        #Scale bars for Angle,length and mass
        
        self.AngleLabel=Label(self.master,text='Angle',fg='midnightblue',font=30).pack()
        self.AngleScale=Scale(self.master,from_=0,to=40,orient=HORIZONTAL, command=self.Angle)
        self.AngleScale.pack()
        self.LengthLabel=Label(self.master,text='Length(m)',fg='midnightblue',font=30).pack()
        self.LengthScale=Scale(self.master,from_=0.1,to=2,orient=HORIZONTAL, resolution=0.1, command=self.Length)
        self.LengthScale.pack()
        self.MassLabel=Label(self.master,text='Mass(kg)',fg='midnightblue',font=30).pack()
        self.MassScale=Scale(self.master,from_=0,to=40,orient=HORIZONTAL, command=self.Mass)
        self.MassScale.pack()

        #Buttons for deleting, loading, running and saving
        
        self.Save=Button(self.master,text="Save",width = 20, pady=5,padx=5,fg='midnightblue',command=self.SaveSettings).pack(pady=4)
        self.Run1=Button(self.master,text="Run",width = 20, pady=5,padx=5, fg="midnightblue",command=self.Run).pack()
        self.Deletesave=Button(self.master,text="Delete",width = 20, pady=5, padx=5, fg="midnightblue",command=self.Delete).pack()
        self.LoadButton=Button(self.master,text="Load",width = 20, pady=5, padx=5, fg="midnightblue",command=self.LoadCombo).pack()
        Checkbutton(master, text="Damping", variable=self.DampingChoice).pack()

    def SaveSettings(self):
        #Save to database subroutine
        
        try: #Tests whether a Combo box exists, using get command because it doesn't edit the data
            test=self.Combo.get()
            print(test)
        except AttributeError:
            self.LoadCombo()
            
        
        SimulationName = self.SimulationName.get()
        Angle = self.AngleScale.get()
        Length = self.LengthScale.get()
        Mass = self.MassScale.get()
        SimulationName = self.SimulationName.get()
        Values = (SimulationName,int(Angle),float(Length),int(Mass))
        with sqlite3.connect("Pendulum.db") as db:
            cursor = db.cursor()
            sql = """insert into PendulumOptions(SimulationName,Angle,Length,Mass) values(?,?,?,?)"""
            cursor.execute(sql,Values)
            db.commit()
        self.LoadSettings()
        
            

    def Delete(self):
        #delete from database subroutine
        selected=self.SimulationName.get(),
        print(selected, "Deleted")
        with sqlite3.connect("Pendulum.db") as db:
            cursor=db.cursor()
            sql="delete from PendulumOptions where SimulationName=?"
            cursor.execute(sql,selected,)
            db.commit()
        #Clears values
        self.SimulationName.set("")
        self.Angle.set(0)
        self.Length.set(0)
        self.Mass.set(0)
        self.Combo.set("")

        
    def LoadCombo(self):
        #Combo box load subroutine
        try:    #makes sure dupelicate combo boxes doesn't occur
            self.Combo.get()
        except AttributeError:
            self.currentFile=StringVar()
            self.Combo = Combobox(self.master,textvariable=self.currentFile)
            self.allfiledetails=[]
            self.Combo["values"] = ("SimulationName")
            self.Combo.current(0)
            self.Combo.pack()
            self.LoadSettings()

    def LoadSettings(self):
        #load from database to combo box
        self.pendulumlist = []

        with sqlite3.connect("Pendulum.db") as db:
            cursor=db.cursor()
            cursor.execute("select * from PendulumOptions") #Loads everything from PendulumOptions table
            self.allfiledetails = cursor.fetchall()
        for index in self.allfiledetails: #Gets every SimulationName and only adds these to combo-box
            self.pendulumlist.append(index[1])
        db.commit()
        self.Combo["values"]=tuple(self.pendulumlist)
        self.Combo.bind("<<ComboboxSelected>>", lambda event: self.Click(event)) #registers a selection of data in the combo box

    def Click(self, event): #When data is in the combo box is clicked
        print(self.currentFile.get())
        filename=self.currentFile.get()
        #currentFile the tuple of values stored in the combo
        for index in self.allfiledetails: #Breaks up the tuple into simulationname,angle,length and mass.
            if filename == index[1]:
                break
        #sets values of entries and sliders to specific loaded data that was loaded from combo box
        self.SimulationName.set(index[1])
        self.AngleScale.set(index[2])
        self.LengthScale.set(index[3])
        self.MassScale.set(index[4])
        
    def Run(self):
        Length = self.LengthScale.get() #in metres
        Mass = self.MassScale.get() #not used at moment
        Angle = self.AngleScale.get() # angle pendulum starts at - right of vertical - in degrees
        DampingBoolean = self.DampingChoice.get()
        print(DampingBoolean)
        Radius = 10.0 # this is not related to any specific real size just size of bob in pixels
        Colour = "red"
        root2=Toplevel(self.master) 
        root2.title("Pendulum")
        root2.resizable(0, 0)
        root2.wm_attributes("-topmost", 1)
        canvas = Canvas(root2, width=500, height=500, bd=0, highlightthickness=0)
        canvas.pack()
        root2.update()
        #canvas, colour,length,mass,angle,r=10,startx=None,starty=10,g=9.81  - Parameters for Pendulum class, last three given default values
        if DampingBoolean == 0:
            pen1 = Pendulum(root2,canvas,Colour,Length,Mass,Angle,Radius)
            pen1.mainloop(3)
        else:
            pen2 = DampedPendulum(root2,canvas,Colour,Length,Mass,Angle,Radius)
            pen2.mainloop(3)

class Pendulum:
    def __init__(self,master, canvas, colour,length,mass,angle,r,startx=None,
                 starty=10,g=9.81):
        #r - radius of bob in pixels
        self.mass=mass
        self.r=r
        self.colour=colour
        self.canvas = canvas
        self.canvas_height = self.canvas.winfo_height()
        print(self.canvas_height)
        self.canvas_width = self.canvas.winfo_width()
        if startx==None:
            self.top_x = self.canvas_width//2 # top point of pendulum
        else:
            self.top_x =startx
        self.top_y = starty#top point of pendulum
        self.angle = angle*pi*2/360 #radians
        self.start_angle = self.angle
        self.end_angle = -angle*pi*2/360
        self.degreesangle=(self.angle*(180/pi))
        self.length = length
        print(length)
        value = length / 9.81
        print(value)
        self.period = 2*pi*sqrt(value)
        print(self.period)


        self.Scaled_Length = 300/self.length #Scales the pendulum's size
        
        self.x = self.top_x + self.length*self.Scaled_Length *cos(self.angle)
        self.y = self.top_y - self.length*self.Scaled_Length *sin(self.angle)#radians
        #self.increment  = 1

        self.line = canvas.create_line(self.top_x, self.top_y, self.x, self.y,width=1,fill="white")
        
        self.BobId = canvas.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r, fill=self.colour,outline=self.colour)     


        string0= "Pendulum Period = " + str(self.period)[:8] + " s"
        self.period_text = canvas.create_text(123,400,text=string0,font=('Times',15))
        
        string1="Pendulum Length = "+ str(self.length)+" m"
        self.length_text = canvas.create_text(93,420,text=string1,font=('Times',15))

        string2 ="X Position:" + str(self.x)[:8]
        self.XPosition_text =canvas.create_text(83,440,text= string2,font=('Times',15))

        string3 ="Angle" + "=" + str(self.degreesangle)[:8]
        self.degreesangle_text =canvas.create_text(75,380,text= string3,font=('Times',15))

        self.canvas.update()
        
        
    def CurrentAngle(self,StartAngle,Period,Time):
         
        Angle = StartAngle*cos(2*pi*Time/Period)
        
        return Angle
        

    def mainloop(self,timeperiod):
        t=timeperiod/100.0
        self.counter = 0
        self.time = 0
        while 1:
            time.sleep(t)
            self.time += t
            self.NewPosition()
            self.canvas.update_idletasks()
            self.canvas.update()
        
        
    def NewPosition(self):
        self.counter += 1
        self.angle = self.CurrentAngle(self.start_angle,self.period,self.time)
        self.degreesangle=(self.angle*(180/pi))
        x = self.top_x + self.length*self.Scaled_Length *cos(self.angle + 2*pi*3/4)
        y = self.top_y - self.length*self.Scaled_Length *sin(self.angle+ 2*pi*3/4)
        diffx=x-self.x
        diffy=y-self.y
        self.canvas.move(self.BobId, diffx,diffy)#move bob
        self.x=x # need to remember last position to calculate difference in position
        self.y=y
        self.canvas.delete(self.line)#delete line as no simple way to rotate
        self.line = self.canvas.create_line(self.top_x, self.top_y, self.x, self.y,width=1,fill=self.colour) # redraw line
        
        self.canvas.delete(self.XPosition_text)
        self.canvas.delete(self.degreesangle_text)
        
        string2 ="X Position:" + str(self.x)[:8]
        self.XPosition_text =self.canvas.create_text(83,440,text= string2,font=('Times',15))
        if self.degreesangle < 0:
            string3 ="Angle " + "=" + str(self.degreesangle)[:8]
        else:
            string3 ="Angle " + "=" + "+"+str(self.degreesangle)[:8]
        self.degreesangle_text =self.canvas.create_text(75,380,text= string3,font=('Times',15))

        #self.Damping()

class DampedPendulum(Pendulum):
    
    def NewPosition(self):
        self.counter += 1
        self.angle = self.CurrentAngle(self.start_angle,self.period,self.time)
        self.degreesangle=(self.angle*(180/pi))
        x = self.top_x + self.length*self.Scaled_Length *cos(self.angle + 2*pi*3/4)
        y = self.top_y - self.length*self.Scaled_Length *sin(self.angle+ 2*pi*3/4)
        diffx=x-self.x
        diffy=y-self.y
        self.canvas.move(self.BobId, diffx,diffy)#move bob
        self.x=x # need to remember last position to calculate difference in position
        self.y=y
        self.canvas.delete(self.line)#delete line as no simple way to rotate
        self.line = self.canvas.create_line(self.top_x, self.top_y, self.x, self.y,width=1,fill=self.colour) # redraw line
        
        self.canvas.delete(self.XPosition_text)
        self.canvas.delete(self.degreesangle_text)
        
        string2 ="X Position:" + str(self.x)[:8]
        self.XPosition_text =self.canvas.create_text(83,440,text= string2,font=('Times',15))
        if self.degreesangle < 0:
            string3 ="Angle =" + str(self.degreesangle)[:8]
        else:
            string3 ="Angle =" + "+"+str(self.degreesangle)[:8]
        self.degreesangle_text =self.canvas.create_text(75,380,text= string3,font=('Times',15))

        self.Damping()
        
    def Damping(self):
        self.Dampingnumber = 0.995
        self.start_angle= self.start_angle*self.Dampingnumber
        
    
if __name__ == "__main__":
            
    root = Tk()
    myGui=Layout(root)
    #root.mainloop()

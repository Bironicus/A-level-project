from tkinter import *
from tkinter.ttk import Combobox
import time
import math
import sqlite3


################################################################################################################################################

class Menu(object):  # class which establishes the menu window
    def __init__(self,master): # initialises the contents of the window
        self.master = master
        self.master.geometry("400x600")
        self.master.wm_title("Input Window") # initialises menu window

        self.SimulationName = StringVar()
        self.Amplitude = DoubleVar()
        self.Mass = DoubleVar()
        self.SpringConstant = DoubleVar() # initialises input variables
        self.Damping = BooleanVar()

        self.Amplitude.set(0.5)
        self.Damping.set(True)
##        self.Mass.set(0.5)
##        self.SpringConstant.set(1.0)

        self.TitleMenu = Label(self.master, text="Menu").grid(row=0,column=1,columnspan=3)
        
        self.SimulationNameLabel = Label(self.master, text="Simulation name").grid(row=1,column=1,columnspan=3)
        self.AmplitudeLabel = Label(self.master, text="Amplitude in metres").grid(row=2,column=1,columnspan=3)
        self.MassLabel = Label(self.master, text="Mass in kilogram").grid(row=3,column=1,columnspan=3)
        self.SpringConstantLabel = Label(self.master, text="Spring Constant in metres").grid(row=4,column=1,columnspan=3)
        self.PresetValuesLabel = Label(self.master, text="Preset Values").grid(row=5,column=1,columnspan=3)

        self.SimulationNameEntry = Entry(self.master, textvariable=self.SimulationName).grid(row=1,column=4)
        self.AmplitudeScale = Scale(self.master, from_=0, to=2, resolution=0.1, orient=HORIZONTAL, variable=self.Amplitude)
        self.AmplitudeScale.grid(row=2,column=4)
        self.MassScale = Scale(self.master, from_=0.1, to=2.5, resolution=0.05, orient=HORIZONTAL, variable=self.Mass)
        self.MassScale.grid(row=3,column=4)
        self.SpringConstantScale = Scale(self.master, from_=0.5, to=2.5, resolution=0.1, orient=HORIZONTAL, variable=self.SpringConstant)
        self.SpringConstantScale.grid(row=4,column=4)
        
        self.PresetValuesCombobox = Combobox(self.master, values=["these","are","place","holders"])
        self.PresetValuesCombobox.grid(row=5,column=4)

        self.SaveButton = Button(self.master,text="Save", command=self.Save).grid(row=6,column=1)
        self.RunButton = Button(self.master,text="Run", command=self.Run).grid(row=6,column=2)
        self.CloseButton = Button(self.master,text="Close", command=self.Close).grid(row=6,column=3)
        self.DampingCheckBox = Checkbutton(self.master,text="Damping", variable=self.Damping).grid(row=6,column=4)

    def Close(self):
        quit()

    def Save(self):
####        SimulationName = self.SimulationName.get()
####        Amplitude = self.Amplitude.get()
####        Mass = self.Mass.get()
####        SpringConstant = self.SpringConstant.get()
####        Damping = self.Damping.get()
####        
####        with sqlite3.connect("Pendulum.db") as db:
####            cursor = db.cursor()
####            sql = """insert into PendulumOptions(SimulationName,Angle,Length,Mass) values(?,?,?,?)"""
####            cursor.execute(sql,Values)
####            db.commit()
####        ####You can do it!!!!!!!!!!!!!!
        print(self.PresetValuesCombobox.get())

    def Run(self):
        SimulationName = self.SimulationName.get()
        Amplitude = self.Amplitude.get()
        Mass = self.Mass.get()
        SpringConstant = self.SpringConstant.get()
        Damping = self.Damping.get()

        root2 = Toplevel(self.master)
        root2.resizable(0,0)
        root2.title(SimulationName)
        root2.wm_attributes("-topmost", 1)
        canvas = Canvas(root2, width=600, height=800)
        canvas.pack()
        root2.update()

##        print(Damping)

##        if Damping == True:
####            spring = DampedSimulation(root2,canvas,Amplitude,Mass,SpringConstant,Damping)
##        else:
        spring = Simulation(root2,canvas,Amplitude,Mass,SpringConstant,Damping)

        spring.mainloop()



################################################################################################################################################

class Simulation:
    def __init__(self,master,canvas,
                 amplitude, mass, springConstant, damping):
        #receive input
        self.canvas = canvas
        self.amplitude = amplitude
        self.mass = mass
        self.spring_constant = springConstant
        self.damping = damping

        #initialise spring values
        self.initial_displacement = self.amplitude * 150
        self.time_period = (2*math.pi) * math.sqrt(self.spring_constant / self.mass)
        self.frequency = 1 / self.time_period
        self.angular_vel = (2*math.pi) * self.frequency
##        self.t = self.time_period/200
##        self.t = self.frequency

        #initalise spring
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.center_x = self.canvas_width / 2
        self.top_y = 20
        self.originbase_y = (self.canvas_height/ 2)# + (10 * math.cos(0))
        self.line_width = self.spring_constant *4 #adjusts the width of the spring's line based on spring constant
        self.radius = 8*(self.mass+2)
        
        self.visuals = {}


    def dampMotion(self):
        dampingVar = (1-(1/10000))
##        dampingVar = 1.1
        self.initial_displacement = self.initial_displacement * dampingVar


    def createSpring(self,counter,i):
##        print("egg")
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

        if self.damping == True:
           self.dampMotion()

        

    def destroySpring(self,i):
##        print("spam")
        num_list = list(range(1,i,2)) + [i]
        
        self.canvas.delete(self.visuals["w"])
        self.canvas.delete(self.visuals["v"])
        self.canvas.delete(self.visuals["mv"])
        self.canvas.delete(self.visuals["a"])
        self.canvas.delete(self.visuals["ma"])
        for x in range(1,len(num_list)+1):
            self.canvas.delete(self.visuals["line%s" % x])

        

    def mainloop(self):
        
        state = self.initial_displacement * math.cos(0)
        self.base_y = self.originbase_y + state
        self.originline = self.canvas.create_line(0,               self.originbase_y,
                                             self.canvas_width,    self.originbase_y,
                                             width=2,fill="green")
        
        self.maxdispline = self.canvas.create_line(0,              self.base_y,
                                             self.canvas_width,    self.base_y,
                                             width=2,fill="gray")
        
        amplitude_str = "amplitude = " + str(self.amplitude) + " m"
        self.visuals["ma"] = self.canvas.create_text(100, self.base_y+30,
                                                    text=amplitude_str, font=("Comic Sans MS",12))
        
        t = self.time_period/200
        counter = 0
        i = 14
##        print(self.t)
        while 1:
            self.createSpring(counter,i)
            time.sleep(t)
            counter = counter + 2*t
            self.destroySpring(i)


################################################################################################################################################

##class DampedSimulation(Simulation):
    

















if __name__ == "__main__":
    root = Tk()
    menu = Menu(root)







###https://github.com/Bironicus/A-level-project


    

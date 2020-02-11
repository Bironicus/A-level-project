from tkinter import *
from tkinter.ttk import Combobox
import time
import math


class Login(object):
    def __init__(self,master): # initialises the contents of the window
        self.master = master
        self.master.geometry("400x600")
        self.master.wm_title("Login Window") # initialises

        

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

        self.TitleMenu = Label(self.master, text="Menu").grid(row=0,column=1,columnspan=3)
        
        self.SimulationNameLabel = Label(self.master, text="Simulation name").grid(row=1,column=1,columnspan=2)
        self.AmplitudeLabel = Label(self.master, text="Amplitude in metres").grid(row=2,column=1,columnspan=2)
        self.MassLabel = Label(self.master, text="Mass in kilogram").grid(row=3,column=1,columnspan=2)
        self.SpringConstantLabel = Label(self.master, text="Spring Constant in metres").grid(row=4,column=1,columnspan=2)
        self.PresetValuesLabel = Label(self.master, text="Preset Values").grid(row=5,column=1,columnspan=2)

        self.SimulationNameEntry = Entry(self.master).grid(row=1,column=3)
        self.AmplitudeButton = Scale(self.master, from_=0, to=5, resolution=0.1, orient=HORIZONTAL)
        self.AmplitudeButton.grid(row=2,column=3)
        self.MassButton = Scale(self.master, from_=0.1, to=10, resolution=0.1, orient=HORIZONTAL)
        self.MassButton.grid(row=3,column=3)
        self.SpringConstantButton = Scale(self.master, from_=1, to=5, resolution=0.1, orient=HORIZONTAL)
        self.SpringConstantButton.grid(row=4,column=3)
        self.PresetValuesCombobox = Combobox(self.master, values=["these","are","place","holders"])
        self.PresetValuesCombobox.grid(row=5,column=3)

        self.SaveButton = Button(self.master,text="Save", command=self.Save).grid(row=6,column=1)
        self.RunButton = Button(self.master,text="Run", command=self.Run).grid(row=6,column=2)
        self.DampingCheckBox = Checkbutton(self.master,text="Damping").grid(row=6,column=3)

    def Save(self):
        print("###")

    def Run(self):
        root2 = Toplevel(self.master)
        canvas = Canvas(root2)
        spring = Simulation(root2, canvas)
        spring.mainloop(canvas)
            

class Simulation:
    def __init__(self,master,canvas): # initialises the contents of the window
        self.master = master
        self.master.geometry("680x700")
        self.master.wm_title("Simulation Window") # initialises

        self.canvas_width = 680 #############
        self.canvas_height = 700

        self.x = self.canvas_width / 2
        self.top_y = 20
        self.base_y = (self.canvas_height/ 2) + (10 * math.cos(0))
        self.originbase_y = self.base_y

        self.linew = 2
        self.r = 20

        #temporary variable initialisation (read that again and tell me I don't sound like star trek)
        
        self.mass = 3 #mass in kilogrammes
        self.springConstant = 2 #spring constant in meters
        self.intDispla = 2 #initial displacement
        self.timePeriod = (2 * math.pi) * math.sqrt(self.springConstant / self.mass)
        self.frequency = 1 / self.timePeriod
        self.angularVel = (2 * math.pi) * self.frequency


        self.OriginLine = canvas.create_line(0, self.originbase_y, self.canvas_width, self.originbase_y,
                                               width=self.linew,fill="green")
##        self.weight = canvas.create_rectangle(self.x-self.r, self.base_y, self.x+self.r,
##                                              self.base_y+(2*self.r), fill="black")

        line1, line2, line3, line4 = self.setSpring(canvas)
        
        if self.base_y <= self.originbase_y:
            weight = canvas.create_rectangle(self.x-self.r, self.base_y, self.x+self.r, self.base_y+(2*self.r),
                                             outline="red", fill="red")
        elif self.base_y > self.originbase_y:
            weight = canvas.create_rectangle(self.x-self.r, self.base_y, self.x+self.r, self.base_y+(2*self.r),
                                             outline="blue", fill="blue")

    def setSpring(self,canvas):##,top_y,base_y,x,r):
        b = (self.base_y - self.top_y)/6

        y1 = self.top_y + b
        x1 = self.x + self.r

        y2 = self.top_y + (3*b)
        x2 = self.x - self.r

        y3 = self.top_y + (5*b)
        x3 = self.x + self.r

        y4 = self.top_y + (6*b)
        x4 = self.x

        line1 = canvas.create_line(self.x, self.top_y, x1, y1,width=self.linew,fill="black")
        line2 = canvas.create_line(x1, y1, x2, y2,width=self.linew,fill="black")
        line3 = canvas.create_line(x2, y2, x3, y3,width=self.linew,fill="black")
        line4 = canvas.create_line(x3, y3, x4, y4,width=self.linew,fill="black")
        return line1, line2, line3, line4

    def mainloop(self,canvas):
        counter = 0
        time.sleep(self.timePeriod/200)
        state = self.intDispla * math.cos(counter * (math.pi/64))
        base_y = self.originbase_y + state

        canvas.delete(weight) ###############################
        canvas.delete(line1)
        canvas.delete(line2)
        canvas.delete(line3)
        canvas.delete(line4)
        canvas.update()

        line1, line2, line3, line4 = self.setSpring(canvas)
        
        if base_y <= self.originbase_y:
            weight = canvas.create_rectangle(self.x-self.r, base_y, self.x+self.r, base_y+(2*self.r),
                                             outline="red", fill="red")
        elif base_y > self.originbase_y:
            weight = canvas.create_rectangle(self.x-self.r, base_y, self.x+self.r, base_y+(2*self.r),
                                             outline="blue", fill="blue")
        canvas.update()
        
        counter = counter+1
        



if __name__ == "__main__":
    root = Tk()
##    root2 = Tk()
##    login = Login(root)
    menu = Menu(root)

















from tkinter import *
from tkinter.ttk import Combobox
import time
import math



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

        self.SimulationNameEntry = Entry(self.master, textvariable=self.SimulationName).grid(row=1,column=3)
        self.AmplitudeScale = Scale(self.master, from_=0, to=5, resolution=0.1, orient=HORIZONTAL, variable=self.Amplitude)
        self.AmplitudeScale.grid(row=2,column=3)
        self.MassScale = Scale(self.master, from_=0.1, to=10, resolution=0.1, orient=HORIZONTAL, variable=self.Mass)
        self.MassScale.grid(row=3,column=3)
        self.SpringConstantScale = Scale(self.master, from_=1, to=5, resolution=0.1, orient=HORIZONTAL, variable=self.SpringConstant)
        self.SpringConstantScale.grid(row=4,column=3)
        self.PresetValuesCombobox = Combobox(self.master, values=["these","are","place","holders"])
        self.PresetValuesCombobox.grid(row=5,column=3)

        self.SaveButton = Button(self.master,text="Save", command=self.Save).grid(row=6,column=1)
        self.RunButton = Button(self.master,text="Run", command=self.Run).grid(row=6,column=2)
        self.DampingCheckBox = Checkbutton(self.master,text="Damping", variable=self.Damping).grid(row=6,column=3)

    def Save(self):
        print("###")

    def Run(self):
        SimulationName = self.SimulationName.get()
        Amplitude = self.Amplitude.get()
        Mass = self.Mass.get()
        SpringConstant = self.SpringConstant.get()
        Damping = self.Damping.get()

        root2 = Toplevel(self.master)
        root2.resizable(width=False, height=False)
        canvas = Canvas(root2, width=680, height=700).pack()



class Simulation():
    def __init__(self,master,canvas,
                 simulationName, amplitude, mass, springConstant, damping):
        #receive input
        self.simulationName = simulationName
        self.amplitude = mass
        self.mass = mass
        self.springConstant = springConstant
        self.damping = damping

        #initialise spring values
        self.initalDisplac = self.amplitude
        self.timePeriod = (2 * math.pi) * math.sqrt(self.springConstant / self.mass)
        self.frequency = 1 / self.timePeriod
        self.angularVel = (2 * math.pi) * self.frequency
    











if __name__ == "__main__":
    root = Tk()
    menu = Menu(root)







###https://github.com/Bironicus/A-level-project


    
